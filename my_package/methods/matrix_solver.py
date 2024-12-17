import pandas as pd
import geopandas as gpd
from enum import Enum
from my_package.models.tag import Tag
from my_package.models.requirement import Requirement
from my_package.models.requirements_matrix import REQUIREMENTS_MATRIX

class MatrixSolver():

    def __init__(self, blocks_gdf : gpd.GeoDataFrame, gdfs : list[gpd.GeoDataFrame]):
        self.blocks_gdf = blocks_gdf.copy()
        self.gdfs = [gdf.copy() for gdf in gdfs]

    def _concatenate_tags(self, blocks_gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        blocks_gdf['tags'] = blocks_gdf.apply(lambda _ : [], axis=1)
        for gdf in self.gdfs:
            blocks_gdf['tags'] = blocks_gdf['tags'] + gdf['tags']
        return blocks_gdf
    
    @staticmethod
    def _get_requirements_submatrix(tags : list[Tag]) -> pd.DataFrame:
        return REQUIREMENTS_MATRIX.loc[tags]
    
    @staticmethod
    def _solve_requirements_series(series : pd.Series) -> bool | None:
        series = series[~series.isna()]
        if len(series) == 0:
            return None
        return series.all()
        
    def _solve_requirements_submatrix(self, submatrix : pd.DataFrame) -> dict[str, Requirement]:
        requirements_series = submatrix.apply(self._solve_requirements_series, axis=0)
        obligatory_requirements = requirements_series[requirements_series == True].index
        forbidden_requirements = requirements_series[requirements_series == False].index
        return {
            'obligatory_requirements': list(obligatory_requirements),
            'forbidden_requirements': list(forbidden_requirements)
        }
    
    def _get_requirements(self, tags : list[Tag]) -> list[Requirement]:
        submatrix = self._get_requirements_submatrix(tags)
        return self._solve_requirements_submatrix(submatrix)

    def run(self) -> gpd.GeoDataFrame:
        # prepare blocks_gdf with tags
        blocks_gdf = self.blocks_gdf.copy()
        blocks_gdf = self._concatenate_tags(blocks_gdf)
        # prepare requirements
        blocks_gdf['requirements'] = blocks_gdf['tags'].apply(self._get_requirements)
        requirements_gdf = pd.json_normalize(blocks_gdf['requirements'])
        return blocks_gdf[['geometry', 'tags']].merge(requirements_gdf, left_index=True, right_index=True)