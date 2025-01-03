from .tag import Tag
import pandas as pd

TRANSITION_PROBABILITIES : dict[Tag, dict[Tag, float]] = {
  Tag.RESIDENTIAL : {
    Tag.RESIDENTIAL : 1
  },
  Tag.PUBLIC_AND_BUSINESS : {
    Tag.PUBLIC_AND_BUSINESS : 0.5,
    Tag.RECREATION : 0.5
  },
  Tag.INDUSTRIAL : {
    Tag.INDUSTRIAL : 0.5
  },
  Tag.ENGINEERING_AND_TRANSPORTATION_INFRASTRUCTURE : {
    Tag.RECREATION : 0.5,
    Tag.SOCIAL : 0.5
  },
  Tag.AGRICULTURAL : {
    Tag.SOCIAL : 1
  },
  Tag.RECREATIONAL : {
    Tag.RECREATION : 1
  },
  Tag.SPETIAL_PURPOSE :{
    Tag.INDUSTRIAL : 0.5
  }
}


TRANSITION_MATRIX = pd.DataFrame(0.0, index=TRANSITION_PROBABILITIES.keys(), columns=TRANSITION_PROBABILITIES.keys())
for tag_a, tag_probs in TRANSITION_PROBABILITIES.items():
  for tag_b, probability in tag_probs.items():
    TRANSITION_MATRIX.loc[tag_a, tag_b] = probability