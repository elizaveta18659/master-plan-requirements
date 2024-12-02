from enum import Enum
from .group import Group, GROUP_CATEGORY

class Tag(Enum):
  # zoning
  RESIDENTIAL = 'Жилая'
  COMMERCIAL = 'Коммерческая'
  INDUSTRIAL = 'Промышленная'
  AGRICULTURE = 'Сельскохозяйственная'
  SOCIAL = 'Социальная'
  RECREATION = 'Водно-зеленый каркас'
  
  # relation
  CITY_SIGNIFICANCE = 'Общегородского значения'
  DISTRICT_SIGNIFICANCE = 'Районного значения'
  LOCAL_SIGNIFICANCE = 'Местного значения'
  
  MEDICAL_INSTITUTIONS = 'Медицинские учреждения'
  EDUCATIONAL_INSUTITIONS = 'Образовательные учреждения'
  SPORTS_FACILITIES = 'Спортивные объекты'
  COMMERCIAL_OBJECTS = 'Коммерческие объекты'
  CULTURAL_OBJECTS = 'Культурные объекты'
  RECREATIONAL_FACILITIES = 'Рекреационные объекты'

  WATER_OBJECT = 'Водный объект'
  CITY_EMBANKMENT = 'Городская набережная'
  BEACH = 'Пляж'

  DOMINANT = 'Доминанты и видовые объекты'
  CULTURAL_HERITAGE = 'Объекты культурного наследия'
  ATTRACTIONS = 'Городские достопримечательности'

  # zoning
  CENTRAL = 'Центральный'
  POTENTIALLY_CENTRAL = 'Потенциально-центральный'
  NON_CENTRAL = 'Не центральный'

  LIVING = 'Жилая'
  NON_LIVING = 'Нежилая'
  MIXED = 'Смешанная'

  DENSE = 'Плотная'
  LOW_DENSITY = 'Низкоплотная'

  HIGH_RISE = 'Высотная'
  MULTI_STOREY = 'Многоэтажная'
  MID_RISE = 'Среднеэтажная'
  LOW_RISE = 'Малоэтажная'

GROUPS_TAGS = {
  Group.FUNCTIONAL_ZONE : [
    Tag.RESIDENTIAL,
    Tag.COMMERCIAL,
    Tag.INDUSTRIAL,
    Tag.AGRICULTURE,
    Tag.SOCIAL,
    Tag.RECREATION,
  ],
  Group.TRANSPORT : [
    Tag.CITY_SIGNIFICANCE,
    Tag.DISTRICT_SIGNIFICANCE,
    Tag.LOCAL_SIGNIFICANCE,
  ],
  Group.INFRASTRUCTURE : [
    Tag.MEDICAL_INSTITUTIONS,
    Tag.EDUCATIONAL_INSUTITIONS,
    Tag.SPORTS_FACILITIES,
    Tag.COMMERCIAL_OBJECTS,
    Tag.CULTURAL_OBJECTS,
    Tag.RECREATIONAL_FACILITIES
  ],
  Group.COASTAL_OBJECTS : [
    Tag.WATER_OBJECT,
    Tag.CITY_EMBANKMENT,
    Tag.BEACH
  ],
  Group.ICONIC_OBJECTS : [
    Tag.DOMINANT,
    Tag.CULTURAL_HERITAGE,
    Tag.ATTRACTIONS
  ],
  Group.CENTRALITY : [
    Tag.CENTRAL,
    Tag.NON_CENTRAL,
    Tag.POTENTIALLY_CENTRAL,
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
    Tag.MULTI_STOREY,
    Tag.MID_RISE,
    Tag.LOW_RISE
  ]
}

TAG_GROUP = {tag : group for group, tags in GROUPS_TAGS.items() for tag in tags}

TAG_CATEGORY = {tag : GROUP_CATEGORY[group] for group, tags in GROUPS_TAGS.items() for tag in tags}