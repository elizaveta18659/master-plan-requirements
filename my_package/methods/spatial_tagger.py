import geopandas as gpd
import osmnx as ox
import numpy as np
import shapely
from loguru import logger
from tqdm import tqdm
from ..models.tag import Tag

DEFAULT_CRS = 4326

OSM_TAGS = {'building': True}

FLOORS_TAGS = {
    9: Tag.HIGH_RISE,
    5: Tag.MID_RISE,
    1: Tag.LOW_RISE
}

MXI_TAGS = {
    0.7: Tag.LIVING,
    0.3: Tag.MIXED,
    0: Tag.NON_LIVING
}

FLOOR_HEIGHT_METERS = 2.7
BUILD_FLOOR_AREA_COEFFICIENT = 0.95
LIVING_AREA_COEFFICIENT = 0.8

class SpatialTagger():

    def __init__(self, blocks_gdf : gpd.GeoDataFrame):
        self.blocks_gdf = blocks_gdf.copy()

    def _fetch_osm(self) -> gpd.GeoDataFrame:
        logger.info('Fetching OSM data')
        polygon = self.blocks_gdf.to_crs(DEFAULT_CRS).union_all().convex_hull
        osm_data = ox.features_from_polygon(polygon, tags=OSM_TAGS)
        osm_gdf = osm_data.reset_index(drop=True)[["geometry", "building", "building:levels", "height"]]
        osm_gdf = osm_gdf.to_crs(self.blocks_gdf.crs)
        logger.success('OSM data fetched')
        return osm_gdf
    
    @staticmethod
    def _get_number_of_floors(series : gpd.GeoSeries) -> float | None:
        height = series['height']
        levels = series['building:levels']
        # converting
        if isinstance(height, str):
            try:
                height = float(height)
            except ValueError:
                height = np.nan
        if isinstance(levels, str):
            try:
                levels = float(levels)
            except ValueError:
                levels = np.nan
        # get number of floors        
        if np.isnan(levels):
            if not np.isnan(height):
                levels = int(height / FLOOR_HEIGHT_METERS)
            else:
                return None
        return levels
    
    @staticmethod
    def _get_footprint_area(series : gpd.GeoSeries):
        building_area = series.geometry.area
        return building_area
    
    @staticmethod
    def _get_build_floor_area(series : gpd.GeoSeries):
        footprint_area = series['footprint_area']
        number_of_floors = series['number_of_floors']
        return footprint_area * number_of_floors * BUILD_FLOOR_AREA_COEFFICIENT
    
    @staticmethod
    def _get_living_area(series : gpd.GeoSeries) -> float | None:
        build_floor_area = series['build_floor_area']
        building_tag = series['building']
        is_living = building_tag in ["residential", "house", "apartments"]
        return (build_floor_area * LIVING_AREA_COEFFICIENT) if is_living else 0
    
    def _process_osm(self, osm_gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        logger.info('Processing OSM data')
        gdf = osm_gdf.copy()

        columns_functions = {
            'number_of_floors': self._get_number_of_floors,
            'footprint_area': self._get_footprint_area,
            'build_floor_area': self._get_build_floor_area,
            'living_area': self._get_living_area
        }

        for column, f in tqdm(columns_functions.items()):
            gdf[column] = gdf.apply(f, axis=1)

        gdf = gdf[gdf['number_of_floors']>0]
        gdf = gdf[gdf['footprint_area']>0]

        columns = ['geometry', *columns_functions.keys()]

        logger.success('OSM data processed')

        return gdf[columns]
    
    @staticmethod
    def _get_mxi(series : gpd.GeoSeries) -> float:
        return series['living_area'] / series['build_floor_area']

    @staticmethod
    def _get_fsi(series : gpd.GeoSeries) -> float:
        return series['build_floor_area'] / series['site_area']
    
    @staticmethod
    def _get_gsi(series : gpd.GeoSeries) -> float:
        return series['footprint_area'] / series['site_area']
    
    @staticmethod
    def _classify_living(mxi : float) -> Tag | None:
        for value, tag in MXI_TAGS.items():
            if mxi >= value:
                return tag
        return None
    
    @staticmethod
    def _classify_floors(number_of_floors : float) -> Tag | None:
        for value, tag in FLOORS_TAGS.items():
            if number_of_floors >= value:
                return tag
        return None
    
    @staticmethod
    def _classify_density(fsi : float, gsi : float) -> Tag:
        if fsi>=1.0 or gsi>=0.5:
            return Tag.DENSE
        return Tag.LOW_DENSITY
    
    def _get_tags(self, osm_gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        logger.info('Getting tags')
        blocks_gdf = self.blocks_gdf.copy()
        # sjoin both gdfs
        sjoin_gdf = blocks_gdf.sjoin(osm_gdf, how='left')
        sjoin_gdf['index_left'] = sjoin_gdf.index
        sjoin_gdf = sjoin_gdf.groupby('index_left').agg({
            'geometry': 'first',
            'number_of_floors': 'mean',
            'footprint_area': lambda values : sum(values, 0),
            'build_floor_area': lambda values : sum(values, 0),
            'living_area': lambda values : sum(values, 0)
        })
        sjoin_gdf = sjoin_gdf.set_geometry('geometry').set_crs(blocks_gdf.crs)
        # calculate additional properties
        sjoin_gdf['site_area'] = blocks_gdf.area
        columns_functions = {
            'mxi': self._get_mxi,
            'fsi': self._get_fsi,
            'gsi': self._get_gsi,
        }
        for column, f in tqdm(columns_functions.items()):
            sjoin_gdf[column] = sjoin_gdf.apply(f, axis=1)

        # interpret tags
        sjoin_gdf['living_tag'] = sjoin_gdf['mxi'].apply(self._classify_living)
        sjoin_gdf['floors_tag'] = sjoin_gdf['number_of_floors'].apply(self._classify_floors)
        sjoin_gdf['density_tag'] = sjoin_gdf.apply(lambda s : self._classify_density(s['fsi'], s['gsi']), axis=1)
        sjoin_gdf['tags'] = sjoin_gdf.apply(lambda s : [tag for tag in [s['living_tag'], s['floors_tag'], s['density_tag']] if tag is not None], axis=1)

        logger.success('Tags obtained')
        return sjoin_gdf
    
    def run(self):
        
        osm_gdf = self._fetch_osm()
        osm_gdf = self._process_osm(osm_gdf)
        blocks_gdf = self._get_tags(osm_gdf)

        return blocks_gdf