import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.litecart import url_admin
from data.litecart import path_to_nightly

import time

@pytest.fixture
def driver(request):

    wd = webdriver.Firefox(capabilities={"marionette": True}, firefox_binary=path_to_nightly)
    request.addfinalizer(wd.quit)
    return wd


def test_litecart_check_menu_admin(driver):
    driver.get(url_admin)
    driver.find_element_by_name('username').send_keys("admin")
    driver.find_element_by_name('password').send_keys("admin")
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.title_is('My Store'))

    # open menu Appearence
    # vertical_menu = driver.find_element_by_class_name("list-vertical")
    # menu = vertical_menu.find_elements_by_tag_name("a")

    count_main_menu = driver.find_elements_by_id("app-")


    if len(count_main_menu):
        for iter in range(len(count_main_menu)):
            select_menu = driver.find_elements_by_id("app-")[iter]
            select_menu.click()

            h1 = driver.find_elements_by_css_selector("h1")
            assert h1 != 0

            # Check selected menu
            if driver.find_elements_by_id("app-")[iter].find_elements_by_class_name("selected"):
                # Update DOM
                select_menu = driver.find_elements_by_id("app-")[iter]

                # Cycle for submenu
                if select_menu.find_elements_by_class_name("docs"):
                    count_docs = len(select_menu.find_elements_by_css_selector(".docs li"))

                    for sub_menu in range(1, count_docs+1):
                        select_menu.find_element_by_css_selector(f".docs li:nth-child({sub_menu}) a").click()

                        # Update DOM
                        select_menu = driver.find_elements_by_id("app-")[iter]

                        # check teg H1
                        h1 = driver.find_elements_by_css_selector("h1")
                        assert  h1 != 0
