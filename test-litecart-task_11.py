import pytest
import re
import string
import random
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from data.litecart import url
from data.litecart import path_to_nightly


@pytest.fixture
def driver(request):

    wd = webdriver.Firefox(capabilities={"marionette": True}, firefox_binary=path_to_nightly)
    request.addfinalizer(wd.quit)
    return wd


def random_string(maxlen, fixed=None):
    symbols = f"{string.ascii_letters}"
    if fixed is None:
        count = range(random.randrange(maxlen)+1)
    else:
        count = range(maxlen)
    return "".join([random.choice(symbols) for i in count])


def random_number(maxlen, fixed=None):
    symbols = f"{string.digits}"
    if fixed is None:
        count = range(random.randrange(maxlen)+1)
    else:
        count = range(maxlen)
    return "".join([random.choice(symbols) for i in count])


def input_field(locator, text):
    locator.click()
    locator.clear()
    locator.send_keys(text)


def test_litecart_task_10(driver):

    driver.get(url)
    WebDriverWait(driver, 10).until(EC.title_is('Online Store | My Store'))

    # create new customer
    driver.find_element_by_css_selector("[name=login_form] a").click()

    #check page login
    WebDriverWait(driver, 10).until(EC.title_is('Create Account | My Store'))


    customer = {
        'first_name': random_string(10),
        'last_name': random_string(10),
        'address_1': random_string(10),
        'postcode': random_number(5, fixed=True),
        'city': random_string(6),
        'country': "United States",
        'zone': None,
        'email': f"{random_string(5)}@mail.ru",
        'phone': f"{random_number(10, fixed=True)}",
        'password': random_string(5, fixed=True)
    }

    input_field(driver.find_element_by_css_selector("[name=firstname]"), customer['first_name'])
    input_field(driver.find_element_by_css_selector("[name=lastname]"), customer['last_name'])
    input_field(driver.find_element_by_css_selector("[name=address1]"), customer['address_1'])
    input_field(driver.find_element_by_css_selector("[name=postcode]"), customer['postcode'])
    input_field(driver.find_element_by_css_selector("[name=city]"), customer['city'])

    # input country USA
    driver.find_element_by_css_selector(".select2-selection").click()
    driver.find_element_by_css_selector(".select2-search__field").send_keys(customer['country'] + Keys.ENTER)

    # input email
    input_field(driver.find_element_by_css_selector("[name=email]"), customer['email'])

    # imput phone
    phone = driver.find_element_by_css_selector("[name=phone]")
    input_field(phone, f"{phone.get_attribute('placeholder')}{customer['phone']}")

    # input password
    input_field(driver.find_element_by_css_selector("[name=password]"), customer['password'])
    input_field(driver.find_element_by_css_selector("[name=confirmed_password]"), customer['password'])

    # submit create account
    driver.find_element_by_css_selector('[name=create_account').click()

    #logout
    driver.find_element_by_css_selector('#box-account li:last-child a').click()

    #login
    input_field(driver.find_element_by_css_selector("[name=email]"), customer['email'])
    input_field(driver.find_element_by_css_selector("[name=password]"), customer['password'])
    driver.find_element_by_css_selector('[name=login]').click()

    # logout
    driver.find_element_by_css_selector('#box-account li:last-child a').click()




