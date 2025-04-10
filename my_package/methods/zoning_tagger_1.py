import geopandas as gpd
from loguru import logger
from ..models.tag import Tag


ZONE_TO_TAG = {
    Tag.RESIDENTIAL: [
        'Т1Ж1', 'Т1Ж2-1', 'Т1Ж2-2', 'Т2Ж1', 'Т2ЖД2', 'Т3Ж1', 'Т3Ж2', 'Т3ЖД3',
        'ТР2/Т1Ж2-2', 'ТД1-2_1/Т1Ж2-2', 'Т3Ж2/Т1Ж2-2', 'Т3Ж2/ -', 'Т3Ж1/ -',
        'Т2Ж1/Т1Ж2-2', 'Т2Ж1/Т1Ж2-1', 'Т2Ж1/Т1Ж1', 'Т2Ж1/ -'
    ],
    Tag.PUBLIC_AND_BUSINESS: [
        'ТД1-1_1', 'ТД1-1_2', 'ТД1-2_1', 'ТД1-2_2', 'ТД1-3', 'ТД2_1', 'ТД2_2',
        'ТД3', 'ТР2/ТД1-2', 'ТД1-2_2/-'
    ],
    Tag.INDUSTRIAL: [
        'ТИП1', 'ТИП3', 'ТИП4', 'ТПД2_3', 'ТР2/ТП1', 'ТП4', 'ТП3', 'ТП2', 'ТП1',
        'ТОЭЗ', 'ТК1/ТС2', 'ТД1-2_2/ТП1', 'ТД1-2_1/ТП1', 'ТД1-1_1/ТП2',
        'ТД1-1_1/ТП1', 'Т3ЖД3/ТП1', 'Т3Ж2/ТП1'
    ],
    Tag.ENGINEERING_AND_TRANSPORTATION: [
        'ТИ1-1', 'ТИ1-2', 'ТИ2', 'ТИ3', 'ТИ4-1', 'ТИ4-2', 'ТПД2_2/Т1Ж1', 'ТПД2_2',
        'ТПД2_1', 'ТПД1_3', 'ТПД1_2', 'ТПД1_1', 'ТИ4_2', 'ТД1-2_2/ТПД1_1',
        'ТД1-2_2/ТИ3', 'ТД1-2_2/ТИ1-1', 'ТД1-1_1/ТИ1-1', 'Т3Ж2/ТИ1-1', 'Т2Ж1/ТИ1-1'
    ],
    Tag.AGRICULTURAL: [
        'ТС1', 'ТС2', 'ТР2/ТС2', 'ТР2/ТС1', 'ТПД1_2/ТС2', 'ТК1/ТС1',
        'ТД1-2_2/ТС1', 'ТД1-2_1/ТС1', 'Т3Ж2/ТС2', 'Т3Ж2/ТС1', 'Т3Ж1/ТС1',
        'Т1Ж2-2/ТС2', 'Т1Ж2-2/ТС1', 'Т1Ж2-1/ТС1'
    ],
    Tag.RECREATIONAL: [
        'ТР0-1', 'ТР0-2', 'ТР0-2/ -', 'ТР1', 'ТР2', 'ТР2/ -', 'ТР2/ТР1',
        'ТР2/ТР0-1', 'ТР3-1', 'ТР3-2', 'ТР3-2/-', 'ТР3-3', 'ТР4', 'ТР5-1', 'ТР5-2',
        'ТР2/ТР5-1', 'ТР2/ТР3-2', 'ТПД1_2/ТР1', 'ТД1-2_2/ТР3-2', 'ТД1-2_2/ТР2',
        'ТД1-2_2/ТР1', 'ТД1-2_2/ТР0-1', 'ТД1-2_1/ТР5-1', 'ТД1-2_1/ТР3-2',
        'Т3Ж2/ТР1', 'Т2Ж1/ТР3-2', 'Т2Ж1/ТР0-1', 'Т1Ж2-2/ТР1'
    ],
    Tag.SPECIAL_PURPOSE: [
        'ТК1', 'ТК2', 'ТК3', 'ТР2/ТК3', 'ТПД2_1/ТК3', 'ТПД1_2/ТК3', 'ТПД1_1/ТК3',
        'ТК1/ТР1', 'ТД1-2_2/ТК2', 'ТД1-1_2/ТК3', 'Т3Ж2/ТК3', 'Т3Ж2/ТК2',
        'Т2ЖД2/ТК3', 'Т1Ж2-2/ТК3'
    ],
}


class ZoneTagger:
    def __init__(self, gdf: gpd.GeoDataFrame, zone_column: str = 'Зона', mapping: dict[Tag, list[str]] = ZONE_TO_TAG):
        self.gdf = gdf.copy()
        self.zone_column = zone_column
        self.mapping = mapping

    def _get_tag(self, zone_value: str) -> Tag | None:
        for tag, values in self.mapping.items():
            if zone_value in values:
                return tag
        return None

    def run(self) -> gpd.GeoDataFrame:
        logger.info("Assigning zoning tags from column '{}'", self.zone_column)

        # Назначаем теги
        self.gdf['zoning_tag'] = self.gdf[self.zone_column].apply(self._get_tag)

        # Удаляем геометрии без соответствующего тега
        initial_count = len(self.gdf)
        self.gdf = self.gdf[self.gdf['zoning_tag'].notna()]
        removed_count = initial_count - len(self.gdf)
        logger.info("Removed {} geometries without zoning tag", removed_count)

        # Удаляем исходный столбец с обозначениями зоны
        if self.zone_column in self.gdf.columns:
            self.gdf.drop(columns=[self.zone_column], inplace=True)

        logger.success("Zoning tags assigned")
        return self.gdf