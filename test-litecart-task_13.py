import pytest
import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


from data.litecart import url
from data.litecart import path_to_nightly


@pytest.fixture
def driver(request):

    # wd = webdriver.Firefox(capabilities={"marionette": True}, firefox_binary=path_to_nightly)
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_litecart_task_13(driver):

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.title_is('Online Store | My Store'))
    wait = WebDriverWait(driver, 15)

    # count items
    cart = driver.find_element_by_css_selector('.quantity')
    count = int(cart.get_attribute('textContent'))

    # Add first item
    for items in range(3):
        driver.find_element_by_css_selector('#box-most-popular ul li:first-child').click()
        size = driver.find_elements_by_css_selector('.options select')
        if len(size):
            select_size = Select(size[0])
            select_size.select_by_index(1)

        driver.find_element_by_css_selector('[name=add_cart_product').click()

        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.quantity'), str(count + 1)))
        cart = driver.find_element_by_css_selector('.quantity')
        new_count = int(cart.get_attribute('textContent'))

        assert new_count > count
        count, new_count = new_count, 0

        driver.find_element_by_css_selector('.content #breadcrumbs li:first-child a:first-child').click()

    # Select Cart
    driver.find_element_by_css_selector('#cart a:last-child').click()

    order_summary = driver.find_element_by_css_selector('.dataTable')
    wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#customer-service-wrapper .title'), "Customer Service"))
    shortcut = driver.find_elements_by_css_selector('.shortcut a')
    assert len(shortcut) != 0

    while True:
        wait.until(EC.element_to_be_clickable((By.NAME, "remove_cart_item"))).click()
        wait.until(EC.staleness_of(order_summary))
        if len(driver.find_elements_by_css_selector('.dataTable tr .item')[1:]) == 0:
            break






