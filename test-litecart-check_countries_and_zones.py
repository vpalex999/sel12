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

    # Stage 1
    # Check sorting of countries and their zones alphabetically
    for sub_menu in menu:
        if sub_menu.get_attribute("textContent") == "Countries":
            sub_menu.click()
            break

    countries = driver.find_element_by_css_selector("h1").get_attribute("textContent").strip()
    assert countries == "Countries"

    row = driver.find_elements_by_css_selector("table .row")
    assert len(row) != 0

    # source unsorted list
    country_a = []

    for count in  range(len(row)):
        country = row[count]
        country_a.append(country.find_elements_by_css_selector("a")[0].text)

        if country.find_elements_by_css_selector("td")[-2].get_attribute("textContent") != '0':
            country.find_elements_by_css_selector("a")[-1].click()
            row_zones = driver.find_elements_by_css_selector("#table-zones tr")

            assert len(row_zones) > 2

            row_zones = row_zones[1:-1]
            country_zones = []

            for row_zona in row_zones:
                country_zones.append(row_zona.find_elements_by_css_selector("td")[2].text)

            assert country_zones == sorted(country_zones)

            driver.find_element_by_css_selector('button[name=cancel]').click()
            row = driver.find_elements_by_css_selector("table .row")

    assert country_a == sorted(country_a)

    # Stage 2



