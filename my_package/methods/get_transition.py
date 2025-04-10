import geopandas as gpd
import pandas as pd
from shapely.errors import TopologicalError
from loguru import logger
from ..models.transition_matrix import TRANSITION_MATRIX


# Функция для расчёта значений переходов на основе соседних кварталов
def compute_zone_transitions(row, gdf, transition_matrix):
    current_zone = row['zoning_tag']
    
    # Если у объекта нет тега зоны — возвращаем нули для всех
    if current_zone not in transition_matrix.index:
        return pd.Series({zone: 0 for zone in transition_matrix.index})

    # Базовые значения переходов для текущей зоны
    transition_values = {
        zone: transition_matrix.at[current_zone, zone]
        for zone in transition_matrix.index
    }

    # Получаем соседние объекты, попадающие в буфер и не совпадающие с самим объектом
    neighbors = gdf[
        gdf.geometry.intersects(row['buffered_geometry']) & (gdf.index != row.name)
    ]

    # Если соседей нет — возвращаем базовые значения
    if neighbors.empty:
        return pd.Series(transition_values)

    # Суммируем значения переходов по всем соседям
    for _, neighbor in neighbors.iterrows():
        neighbor_zone = neighbor['zoning_tag']
        if neighbor_zone in transition_matrix.index:
            transition_values[neighbor_zone] += transition_matrix.at[current_zone, neighbor_zone]

    return pd.Series(transition_values)


# Функция нормализации значений в transition-столбцах
def normalize_zoning_change(row):
    total = row.sum()
    if total > 0:
        return (row / total).round(4)  # Нормализация и округление до 4 знаков
    return row.round(4)  # Если сумма нулевая — просто округляем


# Основная функция обработки GeoDataFrame с применением переходной матрицы
def TRANSITION_RESULT(gdf: gpd.GeoDataFrame, transition_matrix: pd.DataFrame = TRANSITION_MATRIX) -> gpd.GeoDataFrame:
    # Шаг 1: Исправление геометрий (устранение топологических ошибок)
    logger.info("Fixing geometry...")
    try:
        gdf['geometry'] = gdf['geometry'].buffer(0)
    except TopologicalError as e:
        logger.error("Error fixing geometry: {}", e)

    # Шаг 2: Создание столбцов для каждой зоны на основе базовой матрицы переходов
    logger.info("Creating transition columns...")
    for zone in transition_matrix.index:
        gdf[f"{zone}_transition"] = gdf['zoning_tag'].map(
            lambda z: transition_matrix.at[z, zone] if z in transition_matrix.index else 0
        )

    # Шаг 3: Буферизация геометрий — создаём расширенные области вокруг кварталов
    logger.info("Buffering geometry to find neighbors...")
    gdf['buffered_geometry'] = gdf.geometry.buffer(100)

    # Шаг 4: Расчёт переходных значений с учётом соседей
    logger.info("Computing transition values using neighbors...")
    transition_results = gdf.apply(
        lambda row: compute_zone_transitions(row, gdf, transition_matrix), axis=1
    )

    # Шаг 5: Обновление значений переходов по результатам анализа соседей
    logger.info("Updating transition columns with neighborhood-adjusted values...")
    for zone in transition_matrix.index:
        gdf[f"{zone}_transition"] = transition_results[zone]

    # Шаг 6: Удаление вспомогательного буфера
    gdf.drop(columns=['buffered_geometry'], inplace=True)

    # Шаг 7: Нормализация значений (приведение к диапазону от 0 до 1) и округление
    logger.info("Normalizing and rounding transition values...")
    transition_columns = [col for col in gdf.columns if col.endswith('_transition')]
    gdf[transition_columns] = gdf[transition_columns].apply(normalize_zoning_change, axis=1)

    # Завершение
    logger.success("Transition matrix computation complete.")
    return gdf
