import requests
import allure

BASE_URL = "https://fstravel.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",  # noqa: E501
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",  # noqa: E501
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1"
}


@allure.step("Получить главную страницу")
def get_main_page():
    return requests.get(BASE_URL, headers=HEADERS)


@allure.step("Получить страницу About")
def get_about_page():
    url = BASE_URL + "about"
    return requests.get(url, headers=HEADERS)


@allure.step("Получить Content-Type главной страницы")
def get_response_content_type():
    response = requests.get(BASE_URL, headers=HEADERS)
    return response.headers.get("Content-Type", "")


@allure.step("Получить время ответа главной страницы")
def get_response_time():
    response = requests.get(BASE_URL, headers=HEADERS)
    return response.elapsed.total_seconds()


@allure.step("Получить содержимое главной страницы")
def get_homepage_content():
    response = requests.get(BASE_URL, headers=HEADERS)
    return response.text


@allure.step("Получить главную страницу с редиректами")
def get_main_page_with_redirects():
    return requests.get(BASE_URL, headers=HEADERS, allow_redirects=True)
