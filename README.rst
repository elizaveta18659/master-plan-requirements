ВКР на тему "Разработка подхода по формированию расширенных требований к мастер-планированию с учётом места территории в городе"
----------

За последние несколько лет в России активно развивается создание мастер-планов различного масштаба, формируется методологическая база, меняются устоявшиеся методы работы с градостроительной документацией. В представленной научной работе предложена разработка подхода, который позволяет определить требования к территории с учетом ее расположения. Необходимость составления подобного списка объясняется тем, что требования:

а) образуют основу плана проекта; 

б) используются для того, чтобы избежать либо решить спорные вопросы; 

в) делают процесс распределения приоритетов легче;

г) помогают проанализировать величину проектных преобразований. 

Мастер-план как документ стратегического планирования определяет цели и задачи развития города на основе миссии. В современной архитектурно-градостроительной практике сложился средовой подход, основой которого является стремление к изучению и сохранению особенностей места, созданию разнообразной и гуманной среды. Документ может быть гибким в применении: в зависимости от задач раскрывается тот или иной аспект более подробно. Именно поэтому важным этапом для обоснования принятых решений по преобразованию генерального плана, ПЗЗ и т.д. проводится комплексный анализ территории.

Examples
--------
Подход реализуется в 4 этапа: 

- сбор и подготовка исходных данных, формирование матрицы требований

данные  используемые в работе расположены в папке examples/data 
матрица требований загружена как csv файл

- определение места территории в городе 
кварталам записывается значения по тегам, методы в .py файлах представлены в папке my_pakcage/methods, а пример расчёта в локальных блокнотах в папке examples 

- формирование подматрицы требований 
.csv файл преобразуется  в dataframe из которого выбираются значения требований в соответствии с тегами

- формирование требований 
производятся дополнительные расчёты, объединение отдельных геодатафреймов. результат иллюстрируется при помощи метода  .explore()


В итоге у каждого полигона записаны атрибуты ID квартала, теги, количество тегов, возможность перехода в другую зону, укрупненные технико-экономические показатели, нерекомендуемые требования (ограничения), потенциал развития территории, дополнительные параметры, количество требований общее, количество дополнительных параметров, процент выполненных требований 

License
-------

The project has `BSD-3-Clause license <./LICENSE>`__


Контакты
--------

Вы можете связаться с:

-  `ELizaveta Tumanova <https://t.me/elizaveta18659>`__ - исследователь  

-  `Vasilii Starikov <https://t.me/vasilstar>`__ - научный консультант

.. readme-end
