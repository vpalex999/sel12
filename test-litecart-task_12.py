import pytest
import os
import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from data.litecart import url_admin


@pytest.fixture
def driver(request):

    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def input_field(locator, text):
    locator.click()
    locator.clear()
    locator.send_keys(text)


def find_attribute(driver, pattern, attribute_text):
    for item in driver.find_elements_by_css_selector(pattern):
        if item.get_attribute('textContent') == attribute_text:
            item.click()
            break


def test_litecart_check_menu_admin(driver):
    driver.get(url_admin)
    driver.find_element_by_name('username').send_keys("admin")
    driver.find_element_by_name('password').send_keys("admin")
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.title_is('My Store'))

    menu = driver.find_elements_by_css_selector("span.name")
    assert len(menu) != 0

    for sub_menu in range(len(menu)):
        if menu[sub_menu].get_attribute("textContent") == "Catalog":
            menu[sub_menu].click()
            break

    countries = driver.find_element_by_css_selector("h1").get_attribute("textContent").strip()
    assert countries == "Catalog"

    # add new Product
    driver.find_element_by_css_selector('.button:last-child').click()
    assert driver.find_element_by_css_selector('h1').text == "Add New Product"

    ####################### select General ##################################

    driver.find_element_by_css_selector(".tabs li:nth-child(1)").click()

    # enabled Status
    driver.find_elements_by_css_selector('[name=status]')[0].click()

    # input name
    name = driver.find_elements_by_css_selector('.input-wrapper')[0].find_element_by_tag_name('input')
    input_field(name, "Test_Product")

    code = driver.find_elements_by_css_selector('#tab-general tr:nth-child(3)')[0].find_element_by_tag_name('input')
    input_field(code, "Test_Code")

    # select Categories
    categories_root_status = driver.find_element_by_css_selector('#tab-general tr:nth-child(4) tr:nth-child(1) td input')
    if categories_root_status.get_attribute('checked'):
        categories_root_status.click()

    categories_rubber_ducks_status = driver.find_element_by_css_selector('#tab-general tr:nth-child(4) tr:nth-child(2) td input')
    if categories_rubber_ducks_status.get_attribute('checked'):
        categories_rubber_ducks_status.click()

    categories_sub_status = driver.find_element_by_css_selector('#tab-general tr:nth-child(4) tr:nth-child(3) td input')
    if not categories_sub_status.get_attribute('checked'):
        categories_sub_status.click()

    # select Product Groups (select Female)
    p_g = driver.find_element_by_css_selector('#tab-general tr:nth-child(7) table tr:nth-child(2) input')
    if not p_g.get_attribute('checked'):
        p_g.click()

    # set Quantity
    quantity = driver.find_element_by_css_selector('#tab-general tr:nth-child(8) table tr:nth-child(1) input')
    input_field(quantity, "7")

    # upload Images

    base_dir = os.path.dirname(os.path.abspath(__file__))
    puth_to_img = os.path.join(base_dir, "data/img/red_duck.png")
    file = driver.find_element_by_css_selector('#tab-general tr:nth-child(9) table tr:nth-child(1) input')
    file.send_keys(puth_to_img)

    # Date from
    d_from = datetime.date.today().strftime("%d.%m.%Y")
    date_from = driver.find_element_by_css_selector('[name=date_valid_from')
    date_from.send_keys(Keys.HOME + d_from)

    # Date to
    d_to = (datetime.timedelta(days=10) + datetime.date.today()).strftime("%d.%m.%Y")
    date_to = driver.find_element_by_css_selector('[name=date_valid_to]')
    date_to.send_keys(d_to)

    ####################### select Information ##################################

    driver.find_element_by_css_selector(".tabs li:nth-child(2)").click()

    # Manufactured
    manufactured = driver.find_element_by_css_selector('[name=manufacturer_id]')
    select_manufacture = Select(manufactured)
    select_manufacture.select_by_value('1')

    # Keywords
    keywords = driver.find_element_by_css_selector("[name=keywords")
    input_field(keywords, "test keywords")

    # Short Decription
    descr = driver.find_element_by_css_selector("#tab-information tr:nth-child(4) input")
    input_field(descr, "test Short description")

    # Description
    description = driver.find_element_by_css_selector("#tab-information tr:nth-child(5) .trumbowyg-editor")
    input_field(description, "test Short description")

    # Head Title
    h_title = driver.find_element_by_css_selector("#tab-information tr:nth-child(6) input")
    input_field(h_title, "test Head title")

    # Meta Description
    m_descr = driver.find_element_by_css_selector("#tab-information tr:nth-child(7) input")
    input_field(m_descr, "test Meta Description")

    ####################### select Prices ##################################

    driver.find_element_by_css_selector(".tabs li:nth-child(4)").click()

    # Purchase Price
    p_price = driver.find_element_by_css_selector("[name=purchase_price]")
    input_field(p_price, '10.25')

    currency_code = driver.find_element_by_css_selector('[name=purchase_price_currency_code')
    select_c_code = Select(currency_code)
    select_c_code.select_by_value("EUR")

    # Price
    price_usd = driver.find_element_by_css_selector('#tab-prices table:nth-child(4) tr:nth-child(2) input[type=text]')
    input_field(price_usd, '20')

    price_eur = driver.find_element_by_css_selector('#tab-prices table:nth-child(4) tr:nth-child(3) input[type=text]')
    input_field(price_eur, '15')

    # Save Items
    driver.find_element_by_css_selector('[name=save]').click()

    # Chek add item
    menu = driver.find_elements_by_css_selector("span.name")
    assert len(menu) != 0

    for sub_menu in range(len(menu)):
        if menu[sub_menu].get_attribute("textContent") == "Catalog":
            menu[sub_menu].click()
            break

    find_attribute(driver, '.dataTable tr a', "Rubber Ducks")
    find_attribute(driver, '.dataTable tr a', "Subcategory")
    find_attribute(driver, '.dataTable tr a', "Test_Product")

    check_h1 = driver.find_element_by_css_selector('h1').get_attribute('textContent').strip()

    assert check_h1 == "Edit Product: Test_Product"

