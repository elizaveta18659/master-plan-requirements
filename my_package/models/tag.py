from enum import Enum
import pandas as pd
from .group import Group, GROUP_CATEGORY

class Tag(Enum):
  # zoning
  RESIDENTIAL = "Жилая зона"
  PUBLIC_AND_BUSINESS = "Общественно-деловая"
  INDUSTRIAL = "Производственная"
  ENGINEERING_AND_TRANSPORTATION = "Инженерная и транспортная инфраструктура"
  AGRICULTURAL = "Сельскохозяйсвенного использования"
  RECREATIONAL = "Рекреационная"
  SPECIAL_PURPOSE = "Специального назначения"
  
  # relation
  CITY_LEVEL = 'Городского уровня'
  DISTRICT_LEVEL = 'Районного уровня'
  LOCAL_LEVEL = 'Местного уровня'
  
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
  LINEAR_GREENERY = 'Линейное озеленение'

  DOMINANT = 'Доминанты'
  CULTURAL_HERITAGE = 'Объекты культурного наследия'
  CITY_LANDMARK = 'Городские достопримечательности'

  # spatial
  LIVING = 'Жилая'
  NON_LIVING = 'Нежилая'
  MIXED = 'Смешанная'

  DENSE = 'Плотная'
  LOW_DENSITY = 'Низкоплотная'

  HIGH_RISE = 'Многоэтажная (9-16+)'
  MID_RISE = 'Среднеэтажная (5-8)'
  LOW_RISE = 'Малоэтажная (1-4)'


GROUPS_TAGS = {
  Group.FUNCTIONAL_ZONE : [
    Tag.RESIDENTIAL,
    Tag.PUBLIC_AND_BUSINESS,
    Tag.INDUSTRIAL,
    Tag.ENGINEERING_AND_TRANSPORTATION,
    Tag.AGRICULTURAL,
    Tag.RECREATIONAL,
    Tag.SPECIAL_PURPOSE,
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
  Group.GREENERY_OBJECTS : [
    Tag.CITY_FOREST,
    Tag.PARK,
    Tag.LINEAR_GREENERY,
  ],
  Group.ICONIC_OBJECT : [
    Tag.DOMINANT,
    Tag.CULTURAL_HERITAGE,
    Tag.CITY_LANDMARK,
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