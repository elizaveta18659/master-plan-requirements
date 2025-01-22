import geopandas as gpd
import osmnx as ox
import shapely
from loguru import logger
from ..models.tag import Tag

DEFAULT_CRS = 4326

OSM_TAGS = {'landuse': True}

OSM_TO_TAG = {
    "residential": Tag.RESIDENTIAL,
    "commercial": Tag.PUBLIC_AND_BUSINESS,
    "retail": Tag.PUBLIC_AND_BUSINESS,
    "industrial": Tag.INDUSTRIAL,
    "railway": Tag.ENGINEERING_AND_TRANSPORTATION,
    "farmland": Tag.AGRICULTURAL,
    "park": Tag.RECREATIONAL,
    "forest": Tag.RECREATIONAL,
    "military": Tag.SPECIAL_PURPOSE
}

class ZoningTagger():

    def __init__(self, blocks_gdf : gpd.GeoDataFrame, lu_to_tag : dict[str, Tag] = OSM_TO_TAG):
        self.blocks_gdf = blocks_gdf.copy()
        self.lu_to_tag = lu_to_tag

    def fetch_osm(self) -> gpd.GeoDataFrame:
        logger.info('Fetching OSM data')
        polygon = self.blocks_gdf.to_crs(DEFAULT_CRS).geometry.unary_union.convex_hull
        osm_data = ox.features_from_polygon(polygon, tags=OSM_TAGS)
        osm_gdf = osm_data.reset_index(drop=True)[['geometry', 'landuse']]
        osm_gdf = osm_gdf[osm_gdf.geom_type.isin(['Polygon', 'MultiPolygon'])]
        logger.success('OSM data fetched')
        return osm_gdf
    
    def _process_data(self, lu_gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        logger.info('Processing data')
        lu_gdf = lu_gdf.copy()
        lu_gdf['landuse'] = lu_gdf['landuse'].apply(self.lu_to_tag.get)
        lu_gdf = lu_gdf[~lu_gdf['landuse'].isna()]
        lu_gdf = lu_gdf.to_crs(self.blocks_gdf.crs)
        logger.success('Data processed')
        return lu_gdf
    
    def _get_probabilities(self, blocks_gdf : gpd.GeoDataFrame, lu_gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        logger.info('Calculating probabilities') 
        blocks_gdf = blocks_gdf.copy()
        sjoin_gdf = blocks_gdf.sjoin(lu_gdf, predicate='intersects')

        def _get_tags_probabilities(series):
            block_i = series.name
            block_geometry = series.geometry
            block_area = block_geometry.area
            gdf = sjoin_gdf[sjoin_gdf.index == block_i]
            probabilities = {}
            for lu_i in gdf['index_right']:
                lu_tag = lu_gdf.loc[lu_i, 'landuse']
                lu_geometry = lu_gdf.loc[lu_i, 'geometry']
                intersection_geometry = shapely.intersection(lu_geometry, block_geometry)
                intersection_area = intersection_geometry.area
                probabilities[lu_tag] = intersection_area/block_area
            return probabilities
        
        blocks_gdf['tags_probabilities'] = blocks_gdf.apply(_get_tags_probabilities, axis=1)
        blocks_gdf['zoning_tag'] = blocks_gdf['tags_probabilities'].apply(lambda probs : max(probs, key=probs.get) if len(probs)>0 else None)
        blocks_gdf['tags'] = blocks_gdf['zoning_tag'].apply(lambda tag : [] if tag is None else [tag])
        logger.success('Probabilities calculated')
        return blocks_gdf
    
    def run(self, lu_gdf : gpd.GeoDataFrame | None = None):
        
        if lu_gdf is None:
            logger.warning('No landuse data is provided')
            lu_gdf = self.fetch_osm()
        else:
            assert 'landuse' in lu_gdf.columns, 'landuse gdf must contain "landuse" column'
        lu_gdf = self._process_data(lu_gdf)
        blocks_gdf = self._get_probabilities(self.blocks_gdf, lu_gdf)

        return blocks_gdf