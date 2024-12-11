from .tag import Tag
from .requirement import Requirement
import pandas as pd
import random

# TODO placeholder values

REQUIREMENTS = {tag : {req : random.choice([True, False, None]) for req in list(Requirement)} for tag in list(Tag)}

REQUIREMENTS_MATRIX = pd.DataFrame.from_dict(REQUIREMENTS, orient='index')