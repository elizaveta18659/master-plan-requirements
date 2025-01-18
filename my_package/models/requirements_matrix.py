import os
import numpy as np
import pandas as pd
from pathlib import Path
from .tag import Tag
from .requirement import Requirement

CURRENT_DIRECTORY = Path(__file__).parent
CSV_FILENAME = 'requirements_matrix.csv'
CSV_PATH = CURRENT_DIRECTORY / CSV_FILENAME

REPLACEMENT_MAPPING = {
    1 : True,
    -1 : False, 
    np.nan : None,
    0 : None,
}

_df = pd.read_csv(CSV_PATH, delimiter=';').set_index('Теги', drop=True)

REQUIREMENTS_MATRIX = pd.DataFrame(_df.values, index=[Tag(i) for i in _df.index], columns=[Requirement(c) for c in _df.columns]).replace(REPLACEMENT_MAPPING)
