from .tag import Tag
import pandas as pd

TRANSITION_PROBABILITIES : dict[Tag, dict[Tag, float]] = {
  Tag.RESIDENTIAL : {
    Tag.RESIDENTIAL : 1
  },
  Tag.COMMERCIAL : {
    Tag.COMMERCIAL : 0.5,
    Tag.RECREATION : 0.5
  },
  Tag.INDUSTRIAL : {
    Tag.INDUSTRIAL : 0.5,
    Tag.COMMERCIAL : 0.3,
    Tag.SOCIAL : 0.1,
    Tag.RESIDENTIAL : 0.1
  },
  Tag.AGRICULTURE : {
    Tag.RECREATION : 0.5,
    Tag.SOCIAL : 0.5
  },
  Tag.SOCIAL : {
    Tag.SOCIAL : 1
  },
  Tag.RECREATION : {
    Tag.RECREATION : 1
  }
}

TRANSITION_MATRIX = pd.DataFrame(0.0, index=TRANSITION_PROBABILITIES.keys(), columns=TRANSITION_PROBABILITIES.keys())
for tag_a, tag_probs in TRANSITION_PROBABILITIES.items():
  for tag_b, probability in tag_probs.items():
    TRANSITION_MATRIX.loc[tag_a, tag_b] = probability