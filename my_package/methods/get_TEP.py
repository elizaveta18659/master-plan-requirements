import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.errors import TopologicalError
from loguru import logger


def TEP_RESULT(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    # Шаг 1: Исправление геометрий (устранение топологических ошибок)
    logger.info("Fixing geometry...")
    try:
        gdf['geometry'] = gdf['geometry'].buffer(0)
    except TopologicalError as e:
        logger.error("Error fixing geometry: {}", e)

    # Шаг 2: Добавляем столбец с площадью каждого квартала (в квадратных метрах)
    logger.info("Calculating area for each block...")
    gdf['area'] = gdf.geometry.area

    # Шаг 3: Вычисляем общую площадь города
    logger.info("Calculating total city area...")
    total_city_area = gdf['area'].sum()

    # Шаг 4: Вычисляем площадь каждой зоны (преобразуем zoning_tag в строку для избежания ошибки сортировки)
    logger.info("Calculating total area for each zoning tag...")
    gdf['zoning_tag_str'] = gdf['zoning_tag'].astype(str)
    zone_areas = gdf.groupby('zoning_tag_str')['area'].sum().to_dict()

    # Шаг 5: Вычисляем долю площади квартала от площади всего города (в процентах) и округляем
    logger.info("Computing block area as percentage of city...")
    gdf['area_city'] = ((gdf['area'] / total_city_area) * 100).round(4)

    # Шаг 6: Вычисляем долю площади квартала от своей зоны (в процентах) и округляем
    logger.info("Computing block area as percentage of its zone...")
    gdf['area_zone'] = gdf.apply(
        lambda row: round((row['area'] / zone_areas.get(str(row['zoning_tag']), np.nan)) * 100, 4),
        axis=1
    )

    # Шаг 7: Удаляем временный столбец с текстовыми значениями zoning_tag
    gdf.drop(columns=['zoning_tag_str'], inplace=True)

    # Завершение
    logger.success("TEP indicators successfully calculated.")
    return gdf