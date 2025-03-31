import os
import geopandas as gpd
import pandas as pd
from loguru import logger
from tqdm import tqdm
from ..models.tag import Tag

DEFAULT_CRS = 4326

OBJECT_TYPES = {
    # TRANSPORT
    Tag.CITY_LEVEL: {
    'aerodrome':1500, 
    'heliport':1500, 
    'train_station':1500,
    'bus_station':1500, 
    'marina':1500
    },
    Tag.DISTRICT_LEVEL : {
    'parking':500, 
    'bus_stop':500, 
    'subway_entrance':1500,
    'tram':500, 
    'change_dist_tr':500
    },
    Tag.LOCAL_LEVEL : {
    'cycleway':500,
    'bicycle_parking':100, 
    'kick-scooter_parking':1, 
    'change_local_tr':500
    },
    # INFRASTRUCTURE
    Tag.MEDICAL_FACILITIES : {
        'child_hospital': 500, 
        'child_polyclinic': 500, 
        'dentist': 500,
        'hospital': 500, 
        'polyclinic': 500,
        'roddom': 500, 
        'trauma': 500, 
        'morgue': 500,
        'ambulance_station': 1500
    },
    Tag.EDUCATIONAL_FACILITIES : {
        'kindergarten': 300, 
        'school': 500,
        'college': 1500,
        'university': 1500,
        'research_institute': 500, 
        'change_education':500
    },
    Tag.SPORTS_FACILITIES : {
        'grandstand': 500,
        'sports_hall': 500, 
        'stadium': 500, 
        'fitness_centre': 500, 
        'pitch_centroids': 500, 
        'swimming_pool': 500, 
        'change_sport':500
    }, 
    Tag.COMMERCIAL_FACILITIES : {  
        'office': 500,
        'retail': 500,
        'bank': 500,
        'marketplace': 500,
        'convenience': 500,
        'supermarket': 500,
        'shop_pets': 500,
        'books': 500,
        'clothes': 500,
        'craft': 500,
        'electronic': 500,
        'florist': 500,
        'houseware': 500,
        'shop_sport': 500,
        'pharmacy': 500,
        'bakery':500,
        'cafe':500, 
        'restaurant':500, 
        'bar':500, 
        'shop_car':500
    },

    Tag.CULTURAL_FACILITIES : {
        'museum':500,
        'arts_centre':500,
        'cinema':500,
        'community_centre':500,
        'exhibition_centre':500, 
        'planetarium':500,
        'theatre':500,  
        'gallery':500, 
        'place_of_worship':500, 
        'religion':500
    }, 

    Tag.RECREATIONAL_FACILITIES : {
        'dog_park':500, 
        'resort':500, 
        'sauna':500, 
        'water_park':500, 
        'theme_park':500, 
        'zoo':500,
        'playground':500, 
        'mall':500, 
        'circus':500 
    },

    Tag.TOURISTIC_FACILITIES : {
        'hostel':500,
        'hotel':500
    },

    # COASTAL
    Tag.WATER_OBJECT: {
        'water':500
    },
    Tag.CITY_EMBANKMENT : {
        'embankment':500
    },
    Tag.BEACH : {
        'beach':500, 

    },
    # GREENERY
    Tag.CITY_FOREST: {
        'forest':500,
        'nature_reserve':500
    },
    Tag.PARK: {
        'city_park':500, 
        'park':500,
        'garden':500
    },
    Tag. LINEAR_GREENERY: {
        'shrubbery':1,
        'grass':1,
        'wetland':1
    },
    # LANDMARK
    Tag.CULTURAL_HERITAGE: {
        'historic':500,
        'ZON_OKN':1 
    },
    Tag.CITY_LANDMARK: {
        'artwork':500,
        'attraction':500,
        'viewpoint':500
    }
}

class RelationTaggerCHANGE():

    def __init__(self, blocks_gdf : gpd.GeoDataFrame, objects_gdfs : dict[Tag, gpd.GeoDataFrame]):
        self.blocks_gdf = blocks_gdf.copy()
        self.objects_gdfs = {tag : self._process_objects_gdf(objects_gdf, tag) for tag, objects_gdf in objects_gdfs.items() if objects_gdf is not None}

    def _process_objects_gdf(self, gdf : gpd.GeoDataFrame, tag : Tag) -> gpd.GeoDataFrame:
        gdf = gdf.copy()
        gdf = gdf[~gdf.geometry.isna()]
        gdf = gdf.to_crs(self.blocks_gdf.crs)
        gdf.geometry = gdf.apply(lambda s : s.geometry.buffer(OBJECT_TYPES[tag][s.object_type]), axis=1)
        return gdf

    @staticmethod
    def _read_objects_gdf(data_path : str, object_types : list[str]) -> gpd.GeoDataFrame:
        gdfs = []
        for object_type in object_types:
            file_path = os.path.join(data_path, f"{object_type}.geojson")
            try:
                gdf = gpd.read_file(file_path)
                gdf['object_type'] = object_type
                gdfs.append(gdf[['geometry', 'object_type']])
                logger.success(f'File read {file_path}')
            except Exception:
                logger.error(f" Can't read file {file_path}")

        if len(gdfs)>0:
            return pd.concat(gdfs)
        return None

    @classmethod
    def read_objects_gdfs(cls, data_path : str) -> dict[Tag, gpd.GeoDataFrame]:
        return {tag : cls._read_objects_gdf(data_path, ot_dict.keys()) for tag, ot_dict in OBJECT_TYPES.items()}
    
    def run(self) -> gpd.GeoDataFrame:
        blocks_gdf = self.blocks_gdf.copy()
        for tag, gdf in tqdm(self.objects_gdfs.items()):
            if gdf is None :
                continue
            intersection_gdf = blocks_gdf.sjoin(gdf, predicate='intersects')
            blocks_gdf[tag] = blocks_gdf.apply(lambda s : s.name in intersection_gdf.index, axis=1)

        def get_tags(series) -> list[Tag]:
            return [column for column, value in series.items() if (isinstance(column, Tag) and value)]

        blocks_gdf['tags'] = blocks_gdf.apply(get_tags, axis=1)
        return blocks_gdf