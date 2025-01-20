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
    'aerodrome':3000, 
    'heliport':3000, 
    'helipad':3000, 
    'railway':3000,
    'train_building':3000, 
    'train_station':3000
    'bus_station':1500, +
    'marina':3000
    },
    Tag.DISTRICT_LEVEL : {
    'parking':1, +
    'bus_stop':500, +
    'subway_entrance':1500+
    'transportation':500, 
    'platform':500, 
    'subway':1500, 
    'tram':500, 
    'tram_stop':500,
    'monorail':1
    },
    Tag.LOCAL_LEVEL : {
    'cycleway':1,
    'bicycle_parking':300, 
    'kick-scooter_parking':300, 
    'aerialway':500
    },
    # INFRASTRUCTURE
    Tag.MEDICAL_FACILITIES : {
        'child_hospital': 1000, 
        'child_polyclinic': 1000, 
        'dentist': 1000,
        'hospital': 1000, 
        'polyclinic': 1000,
        'roddom': 1000, 
        'trauma': 1000, 
        'women_clinic': 1000,
        'clinic': 1000, 
        'veterinary': 1500, 
        'laboratory': 1500,
        'child_rehabilitation_center': 1000,
        'child_hospis': 1000,
        'diagnostic_centre': 1000,
        'dispensary': 1000,
        'psychologist': 1000,
        'crisis_centre': 1000,
        'morgue': 1000,
        'optician': 1000,
        'psychiatry': 1000, 
        'neuropsychiatric_dispensary': 1000,
        'vaccination': 1000,
        'rehabilitation_center': 1000,
        'ambulance_station': 6000,
    },
    Tag.EDUCATIONAL_FACILITIES : {
        'kindergarten': 500, 
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
        'grandstand': 500,
        'riding_hall': 500, 
        'sports_hall': 500, 
        'sports_centre': 500, 
        'stadium': 1500, 
        'disc_golf_course': 1500, 
        'fitness_centre': 500, 
        'fitness_station': 500, 
        'golf_course': 1500, 
        'horse_riding': 1500, 
        'ice_rink': 1500, 
        'miniature_golf': 1500, 
        'pitch_centroids': 500, 
        'swimming_pool': 3000, 
        'track_centroids': 500, 
        'dive_centre': 1500, 
        'trampoline_park': 1500,
    }, 
    Tag.COMMERCIAL_FACILITIES : {  
        'commercial': 1500,
        'kiosk': 500,
        'office': 1500,
        'retail': 1500,
        'tanning_salon': 500,
        'atm': 500,
        'payment_terminal': 500,
        'bank': 1500,
        'bureau_de_change': 500,
        'money_transfer': 500,
        'payment_centre': 500,
        'studio': 500,
        'internet_cafe': 500,
        'marketplace': 1500,
        'outpost': 1500,
        'convenience': 500,
        'supermarket': 1500,
        'shop_pets': 500,
        'books': 500,
        'clothes': 500,
        'craft': 500,
        'electronic': 500,
        'florist': 500,
        'houseware': 500,
        'shop_sport': 500,
        'tobacco': 500,
        'сopyshop': 500,
        'estate_agent': 1500
        'insurance': 500,
        'lawyer': 500,
        'notary': 500,
        'shoemaker': 500,
        'hairdresser': 500,
        'public_bath': 500,
        'money_lender': 500,
        'pharmacy': 500,
        'bakery':500, 
        'barpub':500, 
        'cafe':500, 
        'restaurant':1500, 
        'bakehouse':500, 
        'bar':500, 
        'fast_food':500, 
        'food_court':500, 
        'pub':500, 
        'post_office':1500, 
        'car_repair':500, 
        'fuel':500
    },

    Tag.CULTURAL_FACILITIES : {
        'museum':3000,
        'bandstand':1500,
        'arts_centre':1500,
        'cinema':3000,
        'community_centre':3000,
        'conference_centre':1500, 
        'events_venue':1500, 
        'exhibition_centre':3000, 
        'music_venue':1500, 
        'planetarium':1500,
        'theatre':3000, 
        'aquarium':1500, 
        'gallery':3000, 
        'adult_gaming_centre':1500, 
        'amusement_arcade':1500, 
        'bathing_place':1500, 
        'bowling_alley':1500, 
        'dance':1500, 
        'escape_game':1500, 
        'fountain':1, 
        'place_of_worship':3000, 
        'religion':3000
    }, 

    Tag.RECREATIONAL_FACILITIES : {
        'bird_hide':1500, 
        'dog_park':600, 
        'fishing':1500, 
        'resort':1500, 
        'sauna':1500, 
        'water_park':1500, 
        'theme_park':1500, 
        'zoo':1500, 
        'playground':1, 
        'mall':1500, 
        'night_club':1500, 
        'water_park':1500, 
        'circus':1500
    },

    Tag.TOURISTIC_FACILITIES : {
        'guest_house':1500, 
        'hostel':1500, 
        'hotel':1500, 
        'apartment':1500, 
        'information':1500, 
        'motel':1
    },
    Tag.ADMINISTRATIVE_FACILITIES: {
        'fire_station':12000,
        'government':1500, 
        'gatehouse':1500, 
        'public':1500, 
        'military':1500, 
        'social_facility':3000, 
        'social_centre':3000, 
        'stage':1, 
        'ambulance_station':6000, 
        'courthouse':1, 
        'mfz':1500, 
        'ministry':1500, 
        'register_office':1500, 
        'police':1, 
        'prison':1, 
        'prosecutor':1, 
        'tax':1, 
        'nursing_home':3000
    }

    # COASTAL
    Tag.WATER_OBJECT: {
        'water':1500, 
        'salt_pond':1500
    },
    Tag.CITY_EMBANKMENT : {
        'embankment':1500
    },
    Tag.BEACH : {
        'beach':1500, 
        'beach_resort':1500
    },
    # GREENERY
    Tag.CITY_FOREST: {
        'forest':1500, 
        'nature_reserve':1500,
        'wood':1500, 
    },
    Tag.PARK: {
        'park':800, 
        'garden':300, 
        'recreation_ground':300,
        'orchad':300
    },
    Tag.LOCAL_GREENERY: {
        'shrubbery':1, 
        'grass':1,
        'wetland':1, 
    },
    # LANDMARK
    Tag.CULTURAL_HERITAGE: {
        'historic':1500, 
        'OKN':1
    },
    Tag.CITY_LANDMARK: {
        'artwork':1500, 
        'attraction':1500, 
        'viewpoint':1500
    }
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