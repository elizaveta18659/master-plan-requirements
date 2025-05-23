from .tag import Tag
import pandas as pd

# Словарь: Tag -> множество ВРИ
ZONES = {
    Tag.RESIDENTIAL: { "для индивидуального жилищного строительства", "малоэтажная многоквартирная жилая застройка", "для ведения личного подсобного хозяйства",
        "блокированная жилая застройка", "передвижное жилье", "среднеэтажная жилая застройка", "многоэтажная жилая застройка", "обслуживание жилой застройки",
        "хранение автотранспорта", "служебные гаражи", "коммунальное обслуживание", "предоставление коммунальных услуг",
        "административные здания организаций, обеспечивающих предоставление коммунальных услуг", "социальное обслуживание", "дома социального обслуживания",
        "оказание социальной помощи населению", "оказание услуг связи", "общежития", "бытовое обслуживание", "здравоохранение", "амбулаторно-поликлиническое обслуживание",
        "стационарное медицинское обслуживание", "медицинские организации особого назначения", "дошкольное, начальное и среднее общее образование",
        "культурное развитие", "объекты культурно-досуговой деятельности", "парки культуры и отдыха", "цирки и зверинцы", "религиозное использование",
        "осуществление религиозных обрядов", "религиозное управление и образование", "амбулаторное ветеринарное обслуживание", "деловое управление", "рынки",
        "магазины", "общественное питание", "обеспечение занятий спортом в помещениях", "площадки для занятий спортом", "общее пользование водными объектами",
        "земельные участки (территории) общего пользования", "благоустройство территории", "ритуальная деятельность", "общее пользование водными объектами",
        "заготовка лесных ресурсов", "историко-культурная деятельность", "внеуличный транспорт", "водный транспорт", "стоянки транспорта общего пользования",
        "связь", "недропользование", "причалы для маломерных судов", "туристическое обслуживание", "спортивные базы", "оборудование площадки для занятий спортом",
        "выставочно-ярмарочная деятельность", "автомобильные мойки", "развлекательные мероприятия", "гостиничное обслуживание", "приюты для животных",
        "представительская деятельность", "государственное управление", "общественное управление", "религиозное управление и образование",
        "садоводство", "скотоводство", "птицеводство", "свиноводство", "пчеловодство", "ведение личного подсобного хозяйства на полевых участках"},

    Tag.PUBLIC_AND_BUSINESS: {"общественное использование объектов капитального строительства", "коммунальное обслуживание", "предоставление коммунальных услуг",
        "административные здания организаций, обеспечивающих предоставление коммунальных услуг", "социальное обслуживание", "дома социального обслуживания",
        "оказание социальной помощи населению", "оказание услуг свзязи", "общежития", "бытовое обслуживание", "здравоохранение", "амбулаторно-поликлиническое обслуживание",
        "стационарное медицинское обслуживание", "медицинские организации особого назначения", "образование и просвещение", "дошкольное, начальное и среднее общее образование",
        "среднее и высшее профессиональное образование", "культурное развитие", "объекты культурно-досуговой деятельности", "парки культуры и отдыха",
        "цирки и зверинцы", "религиозное использование", "осуществление религиозных обрядов", "религиозное управление и образование", "общественное управление",
        "государственное управление", "представительская деятельность", "обеспечение научной деятельности",
        "обеспечение деятельности в области гидрометеорологии и смежных с ней областях", "проведение научных исследований", "проведение научных испытаний",
        "ветеринарное обслуживание", "амбулаторное ветеринарное обслуживание", "приюты для животных", "предпринимательство", "деловое управление",
        "объекты торговли (торговые центры, торгово-развлекательные центры (комплексы)", "рынки", "магазины", "банковская и страховая деятельность",
        "общественное питание", "гостиничное обслуживание", "развлечения", "развлекательные мероприятия", "проведение азартных игр", "служебные гаражи",
        "объекты дорожного сервиса", "заправка транспортных средств", "обеспечение дорожного отдыха", "автомобильные мойки", "ремонт автомобилей",
        "выставочно-ярмарочная деятельность", "земельные участки (территории) общего пользования", "благоустройство территории", "ритуальная деятельность",
        "общее пользование водными объектами", "водные объекты", "историко-культурная деятельность", "санаторная деятельность", "курортная деятельность",
        "внеуличный транспорт", "водный транспорт", "стоянки транспорта общего пользования", "обслуживание перевозок пассажиров", "автомобильный транспорт",
        "размещение автомобильных дорог", "научно-производственная деятельность", "целлюлозно-бумажная промышленность", "обеспечение космической деятельности",
        "связь", "строительная промышленность", "пищевая промышленность", "легкая промышленность", "поля для гольфа или конных прогулок",
        "причалы для маломерных судов", "туристическое обслуживание", "природно-познавательный туризм", "спортивные базы", "авиационный спорт",
        "водный спорт", "оборудование площадки для занятий спортом", "площадки для занятий спортом", "обеспечение занятий спортом в помещениях",
        "обеспечение спортивно-зрелищных мероприятий", "спорт", "отдых(рекреация)", "банковская страховая деятельность", "приюты для животных",
        "религиозное управление и образование", "оказание услуг связи", "хранение автотранспорта"},

    Tag.INDUSTRIAL: {"производственная деятельность", "недропользование", "тяжелая промышленность", "автомобилестроительная промышленность",
        "легкая промышленность", "фармацевтическая промышленность", "пищевая промышленность", "нефтехимическая промышленность",
        "строительная промышленность", "энергетика", "атомная энергетика", "связь", "склады", "складские площадки", "обеспечение космической деятельности",
        "целлюлозно-бумажная промышленность", "научно-производственная деятельность", "коммунальное обслуживание", "предоставление коммунальных услуг",
        "административные здания организаций, обеспечивающих предоставление коммунальных услуг", "оказание услуг связи", "использование лесов",
        "заготовка древесины", "лесные плантации", "заготовка лесных ресурсов", "специальное пользование водными объектами", "гидротехнические сооружения",
        "запас", "специальная деятльность", "трубопроводный транспорт", "воздушный транспорт", "водный транспорт", "стоянки транспорта общего пользования",
        "обслуживание перевозок пассажиров", "автомобильный транспорт", "размещение автомобильных дорог", "обслуживание железнодорожных перевозок",
        "железнодорожный транспорт", "транспорт", "обеспечение космической деятельности", "ремонт автомобилей", "автомобильные мойки", "заправка транспортных средств",
        "объекты дорожного сервиса", "служебные гаражи", "общественное питание", "магазины", "объекты торговли (торговые центры, торгово-развлекательные центры (комплексы)",
        "деловое управление", "предпринимательство", "проведение научных испытаний", "проведение научных исследований",
        "обеспечение деятельности в области гидрометеорологии и смежных с ней областях", "обеспечение научной деятельности", "общежития",
        "хранение автотранспорта", "обеспечение сельскохозяйственного производства", "хранение и переработка сельскохозяйственной продукции",
        "научное обеспечение сельского хозяйства"},

    Tag.ENGINEERING_AND_TRANSPORTATION: { "транспорт", "железнодорожный транспорт", "железнодорожные пути", "обслуживание железнодорожных перевозок",
        "автомобильный транспорт", "размещение автомобильных дорог", "обслуживание перевозок пассажиров", "стоянки транспорта общего пользования",
        "водный транспорт", "воздушный транспорт", "трубопроводный транспорт", "внеуличный транспорт", "земельные участки (территории) общего пользования", 
        "улично-дорожная сеть", "запас", "благоустройство территории", "коммунальное обслуживание", "энергетика", "связь", "гидротехнические сооружения",
        "специальная деятельность", "специальное пользование водными объектами", "лесные плантации", "заготовка древесины", "стоянки трансопрта общего пользования",
        "обеспечение космической деятельности", "складские площадки", "склады", "атомная энергетика", "втомобилестроительная промышленность",
        "недропользование", "причалы для маломерных судов", "ремонт автомобилей", "автомобильные мойки", "обеспечение дорожного отдыха", "заправка транспортных средств",
        "объекты дорожного сервиса", "служебные гаражи", "деловое управление", "стационарное медицинское обслуживание", "бытовое обслуживание", "оказание услуг связи",
        "предоставление коммунальных услуг", "административные здания организаций, обеспечивающих предоставление коммунальных услуг", "хранение автотранспорта"},

    Tag.RECREATIONAL: {"отдых(рекреация)", "спорт", "обеспечение спортивно-зрелищных мероприятий", "обеспечение занятий спортом в помещениях", "площадки для занятий спортом",
        "оборудованные площадки для занятий спортом", "водный спорт", "авиационный спорт", "спортивные базы", "природно-познавательный туризм", "туристическое обслуживание",
        "охота и рыбалка", "причалы для маломерных судов", "поля для гольфа или конных прогулок", "деятельность по особой охране и изучению природы",
        "охрана природных территорий", "курортная деятельность", "санаторная деятельность", "историко-культурная деятельность", "использование лесов",
        "резервные леса", "водные объекты", "общее пользование водными объектами", "земельные участки (территории) общего пользования", "благоустройство территории",
        "внеуличный транспорт", "водный транспорт", "стоянки трансопрта общего пользования", "научно-производственная деятельность", "связь",
        "выставочно-ярмарочная деятельность", "обеспечение дорожного отдыха", "проведение азартных игр", "развлекательные мероприятия", "гостиничное обслуживание",
        "общественное питание", "магазины", "рынки", "проведение научных исследований", "проведение научных испытаний", "обеспечение научной деятельности",
        "религиозное управление и образование", "осуществление религиозных обрядов", "религиозное использование", "парки культуры и отдыха",
        "объекты культурно-досуговой деятельности", "амбураторно-поликлиническое обслуживание", "оказание социальной помощи населению", "научное обеспечение сельского хозяйства"},

    Tag.AGRICULTURAL: {"питомники", "обеспечение сельскохозяйственного производства", "сенокошение", "сельскохозяйственное использование", 
        "растениеводство", "выращивание зерновых и иных сельскохозяйственных культур", "овощеводство", "выращивание тонизирующих, лекарственных, цветочных культур",
        "садоводство", "выращивание льна и конопли", "животноводство", "скотоводство", "звероводство", "птицеводство", "свиноводство", "пчеловодство", 
        "рыбоводство", "хранение и переработка сельскохозяйственной продукции", "научное обеспечение сельского хозяйства", "лесные плантации", "запас",
        "ведение огородничества", "ведение садоводства", "для индивидуального жилищного строительства", "земельные участки общего пользования", "специальная деятельность",
        "специальное пользование водными объектами", "водные объекты", "резервные леса", "заготовка лесных ресурсов", "заготовка древесины", "охрана природных территорий",
        "научно-производственная деятельность", "складские площадки", "склады", "связь", "пищевая промышленность", "охота и рыбалка", "туристическое обслуживание",
        "выставочно-ярмарочная деятельность", "служебные гаражи", "магазины", "рынки", "объекты торговли (торговые центры, торгово-развлекательные центры (комплексы)",
        "предпринимательство", "деловое управление", "общественное питание", "приюты для животных", "амбулаторное ветеринарное обслуживание",
        "ветеринарное обслуживание", "проведение научных испытаний", "проведение научных исследований",
        "обеспечение деятельности в области гидрометеорологии и смежных с ней областях", "обеспечение научной деятельности", "общежития",
        "оказание услуг связи", "предоставление коммунальных услуг", "административные здания организаций, обеспечивающих предоставление коммунальных услуг",
        "коммунальное обслуживание", "хранение автотранспорта", "выпас сельскохозйственных животных"},

    Tag.SPECIAL_PURPOSE: {"обеспечение обороны и безопасности", "обеспечение вооруженных сил", "охрана Государственной границы Российской Федерации",
        "обеспечение внутреннего правопорядка", "обеспечение деятельности по исполнению наказаний", "деятельность по особой охране и изучению природы",
        "ритуальная деятельность", "специальная деятельность", "специальное пользование водными объектами", "обеспечение космической деятельности",
        "складские площадки", "склады", "связь", "атомная энергетика", "энергетика", "служебные гаражи", "проведение азартных игр в игорных зонах",
        "проведение азартных игр", "медицинские организации особого назначения"},
}

# Функция для построения матрицы переходов зонирования
def calculate_transition_matrix(zones_dict: dict[Tag, set[str]]) -> pd.DataFrame:
    tags = list(zones_dict.keys())
    matrix = pd.DataFrame(index=tags, columns=tags, dtype=float)

    for from_tag in tags:
        for to_tag in tags:
            if from_tag == to_tag:
                matrix.loc[from_tag, to_tag] = 1.0
            else:
                common = zones_dict[from_tag] & zones_dict[to_tag]
                total_to = len(zones_dict[to_tag])
                matrix.loc[from_tag, to_tag] = len(common) / total_to if total_to > 0 else 0

    return matrix.round(4)

# Расчёт и экспорт матрицы под именем TRANSITION_MATRIX
TRANSITION_MATRIX = calculate_transition_matrix(ZONES)

# Функция для получения значения перехода
def get_transition_value(from_tag: Tag, to_tag: Tag) -> float:
    return TRANSITION_MATRIX.loc[from_tag, to_tag]