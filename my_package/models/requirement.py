from enum import Enum

class Requirement(Enum):
  COMMERCIAL_PLACEMENT = 'размещение коммерческих сервисов ежедневного использования'
  INFRASTRUCTURE_PLACEMENT = 'размещение инфраструктуры для основных соц групп'
  TRANSPORT_PLACEMENT = 'размещение транспортных узлов'
  SERVICE_PLACEMENT = 'размещение скопления точек обслуживания населения'
  PROTECTION_ZONE = 'устройство защитной зоны'
  RECREATION_ZONE = 'создание рекреационных зон'
  ICONIC_OBJECT = 'размещение знаковых объектов'
  NEW_OBJECT = 'размещение нового объекта  с учетом радиуса влияния'
  VIEW_CHARACTERISTICS = 'учет видовых характеристик'
  HEIGHT_CONTROL = 'регулирование высотности'
  PUBLIC_SPACE = 'обустройство общественных пространств'