from enum import Enum
import pandas as pd
from .group import Group, GROUP_CATEGORY

class Tag(Enum):
  # zoning
  RESIDENTIAL = "Жилая зона"
  PUBLIC_AND_BUSINESS = "Общественно-деловая"
  INDUSTRIAL = "Производственная"
  ENGINEERING_AND_TRANSPORTATION = "Инженерная и транспортная инфраструктуры"
  AGRICULTURAL = "Сельскохозяйсвенного использования"
  RECREATIONAL = "Рекреационная"
  SPETIAL_PURPOSE = "Специального назначения"
  
  # relation
  CITY_LEVEL = 'Общегородского значения'
  DISTRICT_LEVEL = 'Районного значения'
  LOCAL_LEVEL = 'Местного значения'
  
  MEDICAL_FACILITIES = 'Медицинские учреждения'
  EDUCATIONAL_FACILITIES = 'Образовательные учреждения'
  SPORTS_FACILITIES = 'Спортивные объекты'
  COMMERCIAL_FACILITIES = 'Коммерческие объекты'
  CULTURAL_FACILITIES = 'Культурные объекты'
  RECREATIONAL_FACILITIES = 'Рекреационные объекты'
  TOURISTIC_FACILITIES = 'Туристические объекты'

  WATER_OBJECT = 'Водный объект'
  CITY_EMBANKMENT = 'Городская набережная'
  BEACH = 'Пляж'
  
  CITY_FOREST = 'Городской лес'
  PARK = 'Скверы и парки'
  LINEAR_GREEN = 'Линейное озеленение'

  DOMINANT = 'Доминанты'
  CULTURAL_HERITAGE = 'Объекты культурного наследия'
  ATTRACTIONS = 'Городские достопримечательности'

  # spatial
  LIVING = 'Жилая'
  NON_LIVING = 'Нежилая'
  MIXED = 'Смешанная'

  DENSE = 'Плотная'
  LOW_DENSITY = 'Низкоплотная'

  HIGH_RISE = 'Многоэтажная'
  MID_RISE = 'Среднеэтажная'
  LOW_RISE = 'Малоэтажная'


GROUPS_TAGS = {
  Group.FUNCTIONAL_ZONE : [
    Tag.RESIDENTIAL,
    Tag.PUBLIC_AND_BUSINESS,
    Tag.INDUSTRIAL,
    Tag.ENGINEERING_AND_TRANSPORTATION,
    Tag.AGRICULTURAL,
    Tag.RECREATIONAL,
    Tag.SPETIAL_PURPOSE
  ],
  Group.TRANSPORT : [
    Tag.CITY_LEVEL,
    Tag.DISTRICT_LEVEL,
    Tag.LOCAL_LEVEL,
  ],
  Group.INFRASTRUCTURE : [
    Tag.MEDICAL_FACILITIES,
    Tag.EDUCATIONAL_FACILITIES,
    Tag.SPORTS_FACILITIES,
    Tag.COMMERCIAL_FACILITIES,
    Tag.CULTURAL_FACILITIES,
    Tag.RECREATIONAL_FACILITIES,
    Tag.TOURISTIC_FACILITIES
  ],
  Group.COASTAL_OBJECTS : [
    Tag.WATER_OBJECT,
    Tag.CITY_EMBANKMENT,
    Tag.BEACH
  ],
  Group.LANDMARK_OBJECTS : [
    Tag.DOMINANT,
    Tag.CULTURAL_HERITAGE,
    Tag.ATTRACTIONS
  ],

  Group.PURPOSE : [
    Tag.LIVING,
    Tag.NON_LIVING,
    Tag.MIXED
  ],
  Group.DENSITY : [
    Tag.DENSE,
    Tag.LOW_DENSITY,
  ],
  Group.STOREYS_NUMBER : [
    Tag.HIGH_RISE,
    Tag.MID_RISE,
    Tag.LOW_RISE
  ]
}

TAG_GROUP = {tag : group for group, tags in GROUPS_TAGS.items() for tag in tags}

TAG_CATEGORY = {tag : GROUP_CATEGORY[group] for group, tags in GROUPS_TAGS.items() for tag in tags}

TAGS_DF = pd.DataFrame([{
  'tag': tag, 
  'group': TAG_GROUP[tag], 
  'category': TAG_CATEGORY[tag]
} for tag in list(Tag)]).set_index('tag', drop=True)