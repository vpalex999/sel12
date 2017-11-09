import pytest
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.litecart import url
from data.litecart import path_to_nightly


@pytest.fixture
def driver(request):

    wd = webdriver.Firefox(capabilities={"marionette": True}, firefox_binary=path_to_nightly)
    request.addfinalizer(wd.quit)
    return wd


def test_litecart_check_stickers(driver):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.title_is('Online Store | My Store'))


    products = driver.find_elements_by_css_selector(".box li.product")

    assert len(products) != 0

    for item in products:
        sticker = item.find_elements_by_css_selector(".sticker")
        assert len(sticker) == 1


