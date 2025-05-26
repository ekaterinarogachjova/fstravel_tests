from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from typing import Optional
import time


class Page:
    """Базовый класс страницы"""

    def __init__(self, driver: WebDriver) -> None:
        """
        Инициализация страницы.

        :param driver: экземпляр WebDriver
        """
        self.driver = driver

    def wait_for_element_clickable(self, selector: tuple[str, str], timeout: int = 20) -> Optional[object]:  # noqa: E501
        """
        Ожидание, что элемент кликабелен.

        :param selector: локатор элемента (By, строка)
        :param timeout: время ожидания в секундах
        :return: WebElement если найден, иначе None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(selector)
            )
            return element
        except TimeoutException:
            return None

    def wait_for_element_visible(self, selector: tuple[str, str], timeout: int = 20) -> Optional[object]:  # noqa: E501
        """
        Ожидание видимости элемента.

        :param selector: локатор элемента (By, строка)
        :param timeout: время ожидания в секундах
        :return: WebElement если найден, иначе None
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(selector)
            )
            return element
        except TimeoutException:
            return None

    def wait_for_url_contains(self, url_part: str, timeout: int = 20) -> bool:
        """
        Ожидание, что URL содержит заданную часть.

        :param url_part: часть URL для проверки
        :param timeout: время ожидания в секундах
        :return: True если URL содержит часть, иначе False
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(url_part)
            )
            return True
        except TimeoutException:
            return False


class MainPage(Page):
    """Класс для работы с главной страницей сайта"""

    POPUP_CLOSE_BUTTON = (
        By.CSS_SELECTOR, "#popmechanic-form-86751 > div.popmechanic-close")
    POPUP_FORM = (By.CSS_SELECTOR, "#popmechanic-form-86751")
    CITY_FROM_INPUT = (
        By.CSS_SELECTOR, "#app > div > div.v-main > div > div > div > div:nth-child(1) > div > div > div.tour-search__input-field-1.h-64 > div > div > input")  # noqa: E501
    CITY_TO_INPUT = (By.CSS_SELECTOR, "#app > div > div.v-main > div > div > div > div:nth-child(1) > div > div > div.tour-search__input-field-2.h-64.active-field > div > div.arrival-country-field__pinput.active > input")  # noqa: E501
    SEARCH_BUTTON = (
        By.CSS_SELECTOR, "#app > div > div.v-main > div > div > div > div:nth-child(1) > div > div > button")  # noqa: E501
    RESULTS_BLOCK = (
        By.CSS_SELECTOR, "#app > div > div.v-main > div.container > div > div > div.search-content")  # noqa: E501

    def close_popup_if_present(self) -> bool:
        """
        Закрыть popup форму, если она появилась.

        :return: True если форма была закрыта, False если форма не появилась
        """
        close_button = self.wait_for_element_clickable(
            self.POPUP_CLOSE_BUTTON, timeout=20)
        if close_button:
            close_button.click()
            # Ждём, что форма исчезнет
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located(self.POPUP_FORM)
            )
            return True
        return False

    def set_city_from(self, city_name: str) -> None:
        """
        Установить город 'Откуда'.

        :param city_name: название города
        :return: None
        """
        input_field = self.wait_for_element_clickable(self.CITY_FROM_INPUT)
        if not input_field:
            raise TimeoutException("Поле 'Откуда' не доступно для ввода")
        input_field.clear()
        input_field.send_keys(city_name)
        input_field.send_keys(Keys.ARROW_DOWN)
        input_field.send_keys(Keys.ENTER)

    def set_city_to(self, city_name: str) -> None:
        """
        Установить город 'Куда'.

        :param city_name: название города
        :return: None
        """
        input_field = self.wait_for_element_clickable(self.CITY_TO_INPUT)
        if not input_field:
            raise TimeoutException("Поле 'Куда' не доступно для ввода")
        input_field.click()
        input_field.send_keys(Keys.CONTROL + "a")
        input_field.send_keys(Keys.BACKSPACE)
        input_field.send_keys(city_name)
        # input_field.send_keys(Keys.ARROW_DOWN)
        # input_field.send_keys(Keys.ENTER)
        time.sleep(5)
        input_field.click()

    def double_click_search_button(self) -> None:
        """
        Выполнить двойной клик по кнопке поиска.

        :return: None
        """
        button = self.wait_for_element_clickable(self.SEARCH_BUTTON)
        if not button:
            raise TimeoutException("Кнопка поиска не доступна для клика")
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", button)
        actions = ActionChains(self.driver)
        actions.double_click(button).perform()

    def wait_for_results(self) -> bool:
        """
        Ожидать загрузки страницы с результатами поиска.

        :return: True если результаты видны, иначе False
        """
        url_ok = self.wait_for_url_contains("https://fstravel.com/searchtour/")
        if not url_ok:
            return False
        results_visible = self.wait_for_element_visible(self.RESULTS_BLOCK)
        return results_visible is not None
