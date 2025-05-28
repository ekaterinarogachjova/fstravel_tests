import allure
from api import (
    get_main_page,
    get_about_page,
    get_response_content_type,
    get_response_time,
    get_homepage_content,
    get_main_page_with_redirects
)
from allure_commons.types import Severity


@allure.feature("Главная страница")
@allure.severity(Severity.CRITICAL)
@allure.title("Проверка статуса главной страницы")
@allure.description("Проверяем, что главная страница возвращает статус 200")
def test_main_page_status():
    with allure.step("Отправляем запрос на главную страницу"):
        response = get_main_page()
    with allure.step("Проверяем, что статус код равен 200"):
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"  # noqa: E501


@allure.feature("Страница About")
@allure.severity(Severity.NORMAL)
@allure.title("Проверка статуса страницы About")
@allure.description("Проверяем, что страница About возвращает статус 200")
def test_about_page_status():
    with allure.step("Отправляем запрос на страницу About"):
        response = get_about_page()
    with allure.step("Проверяем, что статус код равен 200"):
        assert response.status_code == 200, f"Expected 200 on About page, got {response.status_code}"  # noqa: E501


@allure.feature("Главная страница")
@allure.severity(Severity.MINOR)
@allure.title("Проверка Content-Type главной страницы")
@allure.description("Проверяем, что Content-Type главной страницы содержит 'text/html'")  # noqa: E501
def test_response_content_type():
    with allure.step("Получаем Content-Type главной страницы"):
        content_type = get_response_content_type()
    with allure.step("Проверяем, что Content-Type содержит 'text/html'"):
        assert "text/html" in content_type, f"Expected 'text/html' in Content-Type, got {content_type}"  # noqa: E501


@allure.feature("Главная страница")
@allure.severity(Severity.MINOR)
@allure.title("Проверка времени ответа главной страницы")
@allure.description("Проверяем, что время ответа главной страницы меньше 3 секунд")  # noqa: E501
def test_response_time():
    with allure.step("Получаем время ответа главной страницы"):
        response_time = get_response_time()
    with allure.step("Проверяем, что время ответа меньше 3 секунд"):
        assert response_time < 3, f"Response time is too long: {response_time} seconds"  # noqa: E501


@allure.feature("Главная страница")
@allure.severity(Severity.TRIVIAL)
@allure.title("Проверка наличия ключевого слова на главной странице")
@allure.description("Проверяем, что на главной странице есть ключевое слово 'travel'")  # noqa: E501
def test_homepage_contains_keyword():
    with allure.step("Получаем содержимое главной страницы"):
        content = get_homepage_content()
    with allure.step("Проверяем, что содержимое содержит 'travel'"):
        assert "travel" in content.lower(), "Keyword 'travel' not found in homepage content"  # noqa: E501


@allure.feature("Главная страница")
@allure.severity(Severity.NORMAL)
@allure.title("Проверка обработки редиректов главной страницы")
@allure.description("Проверяем, что при переходе по редиректам возвращается статус 200")  # noqa: E501
def test_redirects_handling():
    with allure.step("Отправляем запрос на главную страницу с редиректами"):
        response = get_main_page_with_redirects()
    with allure.step("Проверяем, что статус код равен 200"):
        assert response.status_code == 200, f"Expected 200 after redirects, got {response.status_code}"  # noqa: E501
