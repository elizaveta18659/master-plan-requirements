import os
import geopandas as gpd
import pandas as pd
from loguru import logger
from tqdm import tqdm
from ..models.tag import Tag

DEFAULT_CRS = 4326

OBJECT_TYPES = {
    # TRANSPORT
    Tag.CITY_LEVEL: {},
    Tag.DISTRICT_LEVEL : {},
    Tag.LOCAL_LEVEL : {},
    # INFRASTRUCTURE
    Tag.MEDICAL_FACILITIES : {
        'child_hospital': 500, 
        'child_polyclinic': 500, 
        'dentist': 10,
        'hospital': 1, 
        'polyclinic': 1,
        'roddom': 1, 
        'trauma': 1, 
        'women_clinic': 1,
        'clinic': 1, 
        'veterinary': 1, 
        'laboratory': 1,
        'child_rehabilitation_center': 1,
        'child_hospis': 1,
        'diagnostic_centre': 1,
        'dispensary': 1,
        'psychologist': 1,
        'crisis_centre': 1,
        'morgue': 1,
        'optician': 1,
        'psychiatry': 1, 
        'neuropsychiatric_dispensary': 1,
        'vaccination': 1,
        'rehabilitation_center': 1,
        'ambulance_station': 1,
    },
    Tag.EDUCATIONAL_FACILITIES : {
        'kindergarten': 300, 
        'private_kindergarten': 1500,
        'school': 500,
        'private_school': 1500, 
        'college': 1500,
        'language_school': 1500,
        'music_school': 1500,
        'prep_school': 1500,
        'university': 1500,
        'library': 1500,
        'training': 1500,
        'dop_education': 1500,
        'exam_centre': 1500,
        'children_dop_education': 1500,
        'dancing_school': 1500,
        'driving_school': 1500,
        'research_institute': 1500,
        'first_aid_school': 1500,
        'surf_school': 1500,
        'traffic_park': 1500
    },
    Tag.SPORTS_FACILITIES : {
        'grandstand': 1,
        'riding_hall': 1, 
        'sports_hall': 1, 
        'sports_centre': 1, 
        'stadium': 1, 
        'disc_golf_course': 1, 
        'fitness_centre': 1, 
        'fitness_station': 1, 
        'golf_course': 1, 
        'horse_riding': 1, 
        'ice_rink': 1, 
        'miniature_golf': 1, 
        'pitch_centroids': 1, 
        'swimming_pool': 1, 
        'track_centroids': 1, 
        'dive_centre': 1, 
        'trampoline_park': 1,
    }, 
    Tag.COMMERCIAL_FACILITIES : {  
        'commercial': 1,
        'kiosk': 1,
        'office': 1,
        'retail': 1,
        'tanning_salon': 1,
        'atm': 1,
        'payment_terminal': 1,
        'bank': 1,
        'bureau_de_change': 1,
        'money_transfer': 1,
        'payment_centre': 1,
        'studio': 1,
        'internet_cafe': 1,
        'marketplace': 1,
        'outpost': 1,
        'convenience': 1,
        'marketplace': 1,
        'supermarket': 1,
        'shop_pets': 1,
        'books': 1,
        'clothes': 1,
        'craft': 1,
        'electronic': 1,
        'florist': 1,
        'Houseware': 1,
        'shop_sport': 1,
        'tobacco': 1,
        'сopyshop': 1,
        'estate_agent': 1,
        'insurance': 1,
        'lawyer': 1,
        'notary': 1,
        'shoemaker': 1,
        'hairdresser': 1,
        'public_bath': 1,
        'money_lender': 1,
        'pharmacy': 1,
    },
    Tag.CULTURAL_FACILITIES : {
        'museum': 1,
        'bandstand': 1,
        'arts_centre': 1,
        'cinema': 1,
    },
    Tag.RECREATIONAL_FACILITIES : {
        'sanatorium': 1, 
        'bakehouse': 1, 
        'bar': 1,
        'cafe': 1,
        'fast_food': 1,
        'food_court': 1,
        'pub': 1,
        'restaurant': 1, 
        'nightclub': 1,
    },
    Tag.TOURISTIC_FACILITIES : {},
    # COASTAL
    Tag.WATER_OBJECT: {},
    Tag.CITY_EMBANKMENT : {},
    Tag.BEACH : {},
    # GREENERY
    Tag.CITY_FOREST: {},
    Tag.PARK: {},
    Tag.LINEAR_GREENERY: {},
    # ICONIC
    Tag.DOMINANT: {},
    Tag.CULTURAL_HERITAGE: {},
    Tag.CITY_LANDMARK: {},
}

class RelationTagger():

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