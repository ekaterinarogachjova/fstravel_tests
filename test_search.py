import pytest
import allure
from selenium.common.exceptions import TimeoutException
from ui_fun_and_sun import MainPage


@allure.feature("Открытие главной страницы")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест открытия главной страницы")
@allure.description("Проверка, что главная страница открывается и заголовок не пустой")  # noqa: E501
@pytest.mark.dependency(name="open_site")
def test_open_site(driver):
    page = MainPage(driver)  # noqa: F841
    with allure.step("Открываем https://fstravel.com/"):
        driver.get("https://fstravel.com/")
    with allure.step("Проверяем, что заголовок страницы не пустой"):
        title = driver.title
        allure.attach(title, name="Заголовок страницы", attachment_type=allure.attachment_type.TEXT)  # noqa: E501
        assert title != "", "Заголовок страницы пустой"


@allure.feature("Закрытие popup")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Тест закрытия popup формы")
@allure.description("Закрываем popup форму, если она появилась")
@pytest.mark.dependency(name="close_popup", depends=["open_site"])
def test_close_popup(driver):
    page = MainPage(driver)
    with allure.step("Пытаемся закрыть popup форму"):
        closed = page.close_popup_if_present()
        assert closed, "Форма popup не была закрыта или не появилась"


@allure.feature("Установка города 'Откуда'")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Тест установки города 'Откуда'")
@allure.description("Вводим город 'Минеральные Воды' в поле 'Откуда'")
@pytest.mark.dependency(name="set_city_from", depends=["close_popup"])
def test_set_city_from(driver):
    page = MainPage(driver)
    with allure.step("Устанавливаем город 'Минеральные Воды' в поле 'Откуда'"):
        try:
            page.set_city_from("Минеральные Воды")
        except TimeoutException as e:
            pytest.fail(f"Не удалось установить город 'Откуда': {e}")


@allure.feature("Установка города 'Куда'")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Тест установки города 'Куда'")
@allure.description("Вводим город 'Сочи' в поле 'Куда'")
@pytest.mark.dependency(name="set_city_to", depends=["close_popup"])
def test_set_city_to(driver):
    page = MainPage(driver)
    with allure.step("Устанавливаем город 'Сочи' в поле 'Куда'"):
        try:
            page.set_city_to("Сочи")
        except TimeoutException as e:
            pytest.fail(f"Не удалось установить город 'Куда': {e}")


@allure.feature("Нажатие кнопки и проверка перехода")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Тест нажатия кнопки поиска и проверки результатов")
@allure.description("Выполняем двойной клик по кнопке поиска и проверяем переход на страницу результатов")  # noqa: E501
@pytest.mark.dependency(name="click_button_and_check_results", depends=["set_city_from", "set_city_to"])  # noqa: E501
def test_click_button_and_check_results(driver):
    page = MainPage(driver)
    with allure.step("Выполняем двойной клик по кнопке поиска"):
        try:
            page.double_click_search_button()
        except TimeoutException as e:
            pytest.fail(f"Не удалось выполнить двойной клик по кнопке: {e}")

    with allure.step("Ожидаем загрузки страницы с результатами"):
        results_loaded = page.wait_for_results()
        assert results_loaded, "Страница с результатами не загрузилась или элемент не найден"  # noqa: E501

    with allure.step("Проверяем, что блок с результатами отображается"):
        results_element = driver.find_element(*page.RESULTS_BLOCK)
        assert results_element.is_displayed(), "Элемент с результатами не отображается"  # noqa: E501
