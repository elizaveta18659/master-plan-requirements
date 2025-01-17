from enum import Enum
from .category import Category

class Group(Enum):
  # zoning
  FUNCTIONAL_ZONE = 'Функциональная зона'
  # object relation
  TRANSPORT = 'Транспорт'
  INFRASTRUCTURE = 'Инфраструктура'
  COASTAL_OBJECTS = 'Прибрежные объекты'
  GREENERY_OBJECTS = 'Объекты озеленения'
  LANDMARK_OBJECTS = 'Знаковые объекты'
  # spatial parameters
  CENTRALITY = 'Центральность'
  PURPOSE = 'Назначение'
  DENSITY = 'Плотность'
  STOREYS_NUMBER = 'Этажность'

CATEGORIES_GROUPS = {
  Category.ZONING : [
    Group.FUNCTIONAL_ZONE,
  ],
  Category.OBJECT_RELATION : [
    Group.TRANSPORT,
    Group.INFRASTRUCTURE,
    Group.COASTAL_OBJECTS,
    Group.GREENERY_OBJECTS,
    Group.LANDMARK_OBJECTS,
  ],
  Category.SPATIAL_PARAMETERS : {
    Group.CENTRALITY,
    Group.PURPOSE,
    Group.DENSITY,
    Group.STOREYS_NUMBER
  }
}

GROUP_CATEGORY = {group : category for category, groups in CATEGORIES_GROUPS.items() for group in groups}