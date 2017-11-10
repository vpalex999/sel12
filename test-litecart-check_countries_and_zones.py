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
    for sub_menu in range(len(menu)):
        if menu[sub_menu].get_attribute("textContent") == "Countries":
            menu[sub_menu].click()

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
            menu = driver.find_elements_by_css_selector("span.name")

        # Stage 2
        elif menu[sub_menu].get_attribute("textContent") == "Geo Zones":
            menu[sub_menu].click()

            countries = driver.find_element_by_css_selector("h1").get_attribute("textContent").strip()
            assert countries == "Geo Zones"

            row_geo_country = driver.find_elements_by_css_selector(".row")

            for count in  range(len(row_geo_country)):
                country = row_geo_country[count]
                if country.find_elements_by_css_selector("td")[-2].get_attribute("textContent") != '0':
                    country.find_element_by_css_selector("a").click()
                    row_zones = driver.find_elements_by_css_selector("#table-zones tr")
                    row_zones = row_zones[1:-1]
                    zones = []
                    for row_zona in row_zones:
                        selects = row_zona.find_elements_by_css_selector("td:nth-child(3)>select option")
                        for is_select in selects:
                            if is_select.get_attribute("selected") == "true":
                                zones.append(is_select.get_attribute("textContent"))
                                break

                assert zones == sorted(zones)

                driver.find_element_by_css_selector('button[name=cancel]').click()
                row_geo_country = driver.find_elements_by_css_selector(".row")

            menu = driver.find_elements_by_css_selector("span.name")





