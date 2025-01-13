import geopandas as gpd
import osmnx as ox
import shapely
from loguru import logger
from ..models.tag import Tag

DEFAULT_CRS = 4326

OSM_TAGS = {'landuse': True}

OSM_TO_TAG = {
    "residential": Tag.RESIDENTIAL,
    "commercial": Tag.PUBLIC_BUSINESS,
    "retail": Tag.PUBLIC_BUSINESS,
    "industrial": Tag.INDUSTRIAL,
    "railway": Tag.ENGINEERING_TRANSPORT,
    "farmland": Tag.AGRICULTURAL,
    "park": Tag.RECREATIONAL,
    "forest": Tag.RECREATIONAL,
    "military": Tag.SPECIAL_PURPOSE
}

class ZoningTagger():

    def __init__(self, blocks_gdf : gpd.GeoDataFrame):
        self.blocks_gdf = blocks_gdf.copy()

    def _fetch_osm(self) -> gpd.GeoDataFrame:
        logger.info('Fetching OSM data')
        polygon = self.blocks_gdf.to_crs(DEFAULT_CRS).union_all().convex_hull
        osm_data = ox.features_from_polygon(polygon, tags=OSM_TAGS)
        osm_gdf = osm_data.reset_index(drop=True)[['geometry', 'landuse']]
        osm_gdf = osm_gdf[osm_gdf.geom_type.isin(['Polygon', 'MultiPolygon'])]
        osm_gdf = osm_gdf.to_crs(self.blocks_gdf.crs)
        logger.success('OSM data fetched')
        return osm_gdf
    
    def _process_osm(self, osm_gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        logger.info('Processing OSM data')
        osm_gdf = osm_gdf.copy()
        osm_gdf['landuse'] = osm_gdf['landuse'].apply(OSM_TO_TAG.get)
        osm_gdf = osm_gdf[~osm_gdf['landuse'].isna()]
        logger.success('OSM data processed')
        return osm_gdf
    
    def _get_probabilities(self, blocks_gdf : gpd.GeoDataFrame, osm_gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        logger.info('Calculating probabilities') 
        blocks_gdf = blocks_gdf.copy()
        sjoin_gdf = blocks_gdf.sjoin(osm_gdf, predicate='intersects')

        def _get_tags_probabilities(series):
            block_i = series.name
            block_geometry = series.geometry
            block_area = block_geometry.area
            gdf = sjoin_gdf[sjoin_gdf.index == block_i]
            probabilities = {}
            for lu_i in gdf['index_right']:
                lu_tag = osm_gdf.loc[lu_i, 'landuse']
                lu_geometry = osm_gdf.loc[lu_i, 'geometry']
                intersection_geometry = shapely.intersection(lu_geometry, block_geometry)
                intersection_area = intersection_geometry.area
                probabilities[lu_tag] = intersection_area/block_area
            return probabilities
        
        blocks_gdf['tags_probabilities'] = blocks_gdf.apply(_get_tags_probabilities, axis=1)
        blocks_gdf['zoning_tag'] = blocks_gdf['tags_probabilities'].apply(lambda probs : max(probs, key=probs.get) if len(probs)>0 else None)
        blocks_gdf['tags'] = blocks_gdf['zoning_tag'].apply(lambda tag : [] if tag is None else [tag])
        logger.success('Probabilities calculated')
        return blocks_gdf
    
    def run(self):
        
        osm_gdf = self._fetch_osm()
        osm_gdf = self._process_osm(osm_gdf)
        blocks_gdf = self._get_probabilities(self.blocks_gdf, osm_gdf)

        return blocks_gdf