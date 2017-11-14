import pytest
import re
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from data.litecart import url
from data.litecart import path_to_nightly


@pytest.fixture
def driver_f(request):

    wd = webdriver.Firefox(capabilities={"marionette": True}, firefox_binary=path_to_nightly)
    request.addfinalizer(wd.quit)
    return wd


@pytest.fixture
def driver_h(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_litecart_task_10(driver_f, driver_h):

    for driver in driver_f, driver_h:

        driver.get(url)
        WebDriverWait(driver, 10).until(EC.title_is('Online Store | My Store'))

        main_campaigns = {
            'reg': {'price': None, 'color': None, 'txt-dec-line': None, 'size': None},
            'cam': {'price': None, 'color': None, 'font-weight': None, 'size': None}
        }

        sub_campaigns = {
            'reg': {'price': None, 'color': None, 'txt-dec-line': None, 'size': None},
            'cam': {'price': None, 'color': None, 'font-weight': None, 'size': None}
        }

        main_campaigns['name'] = driver.find_element_by_css_selector("#box-campaigns .name").get_attribute("textContent")
        main_campaigns['reg']['price'] = (driver.find_element_by_css_selector("#box-campaigns .regular-price").get_attribute("textContent"))
        main_campaigns['reg']['color'] =(driver.find_element_by_css_selector("#box-campaigns .regular-price").value_of_css_property('color'))
        main_campaigns['reg']['txt-dec-line'] = (driver.find_element_by_css_selector("#box-campaigns .regular-price").value_of_css_property('text-decoration-line'))
        main_campaigns['reg']['size'] = (driver.find_element_by_css_selector("#box-campaigns .regular-price").value_of_css_property('font-size'))

        main_campaigns['cam']['price'] = (driver.find_element_by_css_selector("#box-campaigns .campaign-price").get_attribute("textContent"))
        main_campaigns['cam']['color']= (driver.find_element_by_css_selector("#box-campaigns .campaign-price").value_of_css_property('color'))
        main_campaigns['cam']['font-weight'] = (driver.find_element_by_css_selector("#box-campaigns strong.campaign-price").value_of_css_property('font-weight'))
        main_campaigns['cam']['size'] = (driver.find_element_by_css_selector("#box-campaigns .campaign-price").value_of_css_property('font-size'))

        driver.find_element_by_css_selector('#box-campaigns a:nth-child(1)').click()

        sub_campaigns['name'] = driver.find_element_by_css_selector("h1").text
        sub_campaigns['reg']['price'] = (driver.find_element_by_css_selector(".regular-price").get_attribute("textContent"))
        sub_campaigns['reg']['color'] =(driver.find_element_by_css_selector(".regular-price").value_of_css_property('color'))
        sub_campaigns['reg']['txt-dec-line'] = (driver.find_element_by_css_selector(".regular-price").value_of_css_property('text-decoration-line'))
        sub_campaigns['reg']['size'] = (driver.find_element_by_css_selector(".regular-price").value_of_css_property('font-size'))

        sub_campaigns['cam']['price'] = (driver.find_element_by_css_selector(".campaign-price").get_attribute("textContent"))
        sub_campaigns['cam']['color']= (driver.find_element_by_css_selector(".campaign-price").value_of_css_property('color'))
        sub_campaigns['cam']['font-weight'] = (driver.find_element_by_css_selector("strong.campaign-price").value_of_css_property('font-weight'))
        sub_campaigns['cam']['size'] = (driver.find_element_by_css_selector(".campaign-price").value_of_css_property('font-size'))

        # check (a)
        assert main_campaigns.get('name') == sub_campaigns.get('name')

        # check (b)
        assert main_campaigns.get('reg').get('price') == sub_campaigns.get('reg').get('price')
        assert main_campaigns.get('cam').get('price') == sub_campaigns.get('cam').get('price')

        # check (v)
        # regular price - rgb is equal
        main_color = re.sub('[rgba() ]', "", main_campaigns.get('reg').get('color')).split(',')
        assert main_color is not None
        assert main_color.count(main_color[0]) == 3

        # sub_campaings regular price - rgb is equal
        sub_main_color = re.sub('[rgba() ]', "", sub_campaigns.get('reg').get('color')).split(',')
        assert sub_main_color is not None
        assert sub_main_color.count(sub_main_color[0]) == 3


        # check (v)
        # main text-decoration-line'
        assert main_campaigns['reg']['txt-dec-line'] == "line-through"

        # sub_main text-decoration-line'
        assert sub_campaigns['reg']['txt-dec-line'] == "line-through"

        # check (g)
        # main campaign color is red
        main_camp_color = re.sub('[rgb() ]', "", main_campaigns['cam']['color']).split(',')
        assert main_camp_color is not None
        R, *G_B = main_camp_color
        assert G_B.count('0') == 2

        # main campaign font-weight is bold
        assert main_campaigns['cam']['font-weight'].isdigit() is True
        main_font_weight = int(main_campaigns['cam']['font-weight'])
        assert main_font_weight >= 700



        # sub_campaign color is red and bold
        sub_camp_color = re.sub('[rgb() ]', "", sub_campaigns['cam']['color']).split(',')
        assert sub_camp_color is not None
        R, *G_B = sub_camp_color
        assert G_B.count('0') == 2

        # sub_campaign font-weight is bold
        assert sub_campaigns['cam']['font-weight'].isdigit() is True
        sub_font_weight = int(sub_campaigns['cam']['font-weight'])
        assert sub_font_weight >= 700


        # main campaign-price more than regular-price
        main_cam_size = float(re.sub('[px]', '', main_campaigns['cam']['size']))
        main_reg_size = float(re.sub('[px]', '', main_campaigns['reg']['size']))
        assert main_cam_size > main_reg_size

        # sub_main campaign-price more than regular-price
        sub_main_cam_size = float(re.sub('[px]', '', sub_campaigns['cam']['size']))
        sub_main_reg_size = float(re.sub('[px]', '', sub_campaigns['reg']['size']))
        assert sub_main_cam_size > sub_main_reg_size
        pass



