Финальная_работа
Финальная работа по автоматизации
Задача проекта
Автоматизировать UI- и API-тесты из финальной работы по ручному тестированию
Библиотеки: 
•	pip install pytest
•	pip install selenium
•	pip install webdriver-manager
•	pip install allure-pytest

Шаги
1.	Склонировать проект https://github.com/ekaterinarogachjova/fstravel_tests.git
2.	Установить в зависимости
3.	Запустить тесты:
•	для запуска всех тестов 'pytest'
•	для запуска UI-тестов: 'test_search.py'
•	для запуска API-тестов: pytest 
4.	Сгенерировать отчет 'pytest --alluredir=allure-results'
5.	Открыть отчет  'allure serve allure-results'
