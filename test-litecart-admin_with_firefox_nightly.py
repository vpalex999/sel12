import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.litecart import url_admin


@pytest.fixture
def driver(request):
    patch_to_esr = "/home/vpalexdev/Downloads/firefox-nightly/firefox/firefox"

    wd = webdriver.Firefox(capabilities={"marionette": True}, firefox_binary=patch_to_esr)
    request.addfinalizer(wd.quit)
    return wd


def test_litecart_admin_with_firefox_nightly(driver):
    driver.get(url_admin)
    driver.find_element_by_name('username').send_keys("admin")
    driver.find_element_by_name('password').send_keys("admin")
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.title_is('My Store'))

