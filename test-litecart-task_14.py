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


def test_litecart_task_14(driver):
    driver.get(url_admin)
    driver.find_element_by_name('username').send_keys("admin")
    driver.find_element_by_name('password').send_keys("admin")
    driver.find_element_by_name('login').click()
    WebDriverWait(driver, 10).until(EC.title_is('My Store'))

    wait = WebDriverWait(driver, 10)

    menu = driver.find_elements_by_css_selector("span.name")
    assert len(menu) != 0

    for sub_menu in range(len(menu)):
        if menu[sub_menu].get_attribute("textContent") == "Countries":
            menu[sub_menu].click()
            break

    driver.find_element_by_css_selector('.button').click()
    assert driver.find_element_by_css_selector('h1').text == "Add New Country"

    blank = driver.find_elements_by_css_selector('form a[target=_blank]')


    main_window = driver.current_window_handle

    def there_is_window_other_than(main_window):
        def other_than(driver):
            if len(driver.window_handles) >1:
                new_win = driver.window_handles
                new_win.remove(main_window)
                if ",".join(new_win) != main_window:
                    return ",".join(new_win)
                else:
                    return False
        return other_than

    for win in blank:
        win.click()
        new_win = wait.until(there_is_window_other_than(main_window))
        driver.switch_to_window(new_win)
        driver.close()
        driver.switch_to_window(main_window)

