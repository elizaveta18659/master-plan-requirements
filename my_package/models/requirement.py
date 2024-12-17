from enum import Enum

class Requirement(Enum):
  COMMERCIAL_PLACEMENT = 'Размещение коммерческих сервисов ежедневного использования'
  INFRASTRUCTURE_PLACEMENT = 'Размещение инфраструктуры для основных соц групп'
  TRANSPORT_PLACEMENT = 'Размещение транспортных узлов'
  SERVICE_PLACEMENT = 'Размещение скопления точек обслуживания населения'
  PROTECTION_ZONE = 'Устройство защитной зоны'
  RECREATION_ZONE = 'Создание рекреационных зон'
  ICONIC_OBJECT = 'Размещение знаковых объектов'
  NEW_OBJECT = 'Размещение нового объекта с учетом радиуса влияния'
  VIEW_CHARACTERISTICS = 'Учет видовых характеристик'
  HEIGHT_CONTROL = 'Регулирование высотности'
  PUBLIC_SPACE = 'Обустройство общественных пространств'