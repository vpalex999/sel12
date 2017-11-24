import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.litecart import url_admin
from data.litecart import path_to_nightly


@pytest.fixture
def driver(request):

    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_litecart_task_17(driver):
    driver.get(url_admin)
    driver.find_element_by_name('username').send_keys("admin")
    driver.find_element_by_name('password').send_keys("admin")
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.title_is('My Store'))

    wait = WebDriverWait(driver, 10)

    menu = driver.find_elements_by_css_selector("span.name")
    assert len(menu) != 0


    for sub_menu in range(len(menu)):
        if menu[sub_menu].get_attribute("textContent") == "Catalog":
            menu[sub_menu].click()
            break

    logs = driver.get_log("browser")
    if len(logs):
        print(logs)

    current_count = 1
    while True:
        main_item = driver.find_elements_by_css_selector('.dataTable .row')
        main_item[current_count].find_element_by_css_selector("a").click()
        h1 = driver.find_element_by_css_selector('h1').text
        if h1.startswith("Edit Product"):
            driver.find_element_by_css_selector('[name=cancel]').click()
            logs = driver.get_log("browser")
            if len(logs):
                print(logs)

        if (len(main_item) - 1) <= current_count:
            break
        current_count += 1

