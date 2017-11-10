import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.litecart import url_admin
from data.litecart import path_to_nightly


@pytest.fixture
def driver(request):

    wd = webdriver.Firefox(capabilities={"marionette": True}, firefox_binary=path_to_nightly)
    request.addfinalizer(wd.quit)
    return wd


def test_litecart_check_countries_and_zones(driver):
    driver.get(url_admin)
    driver.find_element_by_name('username').send_keys("admin")
    driver.find_element_by_name('password').send_keys("admin")
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.title_is('My Store'))

    menu = driver.find_elements_by_css_selector("span.name")

    assert len(menu) != 0

    for sub_menu in menu:
        if sub_menu.get_attribute("textContent") == "Countries":
            sub_menu.click()
            break

    # check sorted coubtries
    contries = driver.find_element_by_css_selector("h1").get_attribute("textContent").strip()
    assert contries == "Countries"

    row = driver.find_elements_by_css_selector("table .row")
    assert len(row) != 0

    # source unsorted list
    country_a = []

    for country in row:
        country_a.append(country.find_elements_by_css_selector("a")[0].text)

    # create sorted list by abc
    country_a_sorted = sorted(country_a)

    assert country_a == country_a_sorted

    # check zones in countries




    pass

