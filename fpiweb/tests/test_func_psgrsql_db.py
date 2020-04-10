################################################
# TESTS ON THIs PAGE REQUIRE ACCESS TO LIVE DB!!!
# TESTS ON THIS PAGE CHANGE DATA IN LIVE DB!!!
###################################################

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from django.test import TestCase

import time
import random
import string

##################################################
# Required to log in to db. Comment out variables.
# Keep variables but erase credentials before pushing up
user = "babarehner"
pass_word = 'PostItNotes'
##################################################


# Requires Django Server to be running prior to test!!
class AddPallet(TestCase):

    url = ""

    # delay for video recording
    RECORD = False
    def delay_for_recording(self):
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(1)   # delay to make sure page loads

    name = True
    def make_random_box(self, name):
        # makes random 5 letter box names/numbers to mitigate duplicate errors
        # make sure random is called with current time as a seed value
        random.seed()
        if name:
            return ''.join(random.choice(string.ascii_letters) for _i in range(5))
        else:
            return ''.join(random.choice(string.digits) for _i in range(5))

    def select_random_dropdown(self, dropdown_int):
        random.seed()
        # return ''.join(random.choice(string.digits) for _i in range(dropdown_int))
        return random.randint(1,dropdown_int)

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1920, 1080)
        self.browser.set_window_position(0,0)
        self.url = "http://localhost:8000"

    def tearDown(self):
        self.delay_for_recording()
        self.browser.quit()


    def test_Login(self):
        global url
        self.browser.get(self.url)
        self.assertIn("Login", self.browser.title)

        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys(user)
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys(pass_word)
        # self.browser.find_element_by_tag_name("form").click()
        login.submit()
        self.delay_for_recording()
        self.url = self.browser.current_url

        self.browser.get(self.url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()
        self.delay_for_recording()

        self.url = self.browser.current_url
        self.assertIn("Build Pallet", self.browser.title)
        name_of_pallet = self.browser.find_element_by_name('name')
        name_of_pallet.send_keys(self.make_random_box(self.name))
        # name_of_pallet.send_keys('purple')
        self.delay_for_recording()
        # use xpath with input not submit!
        select_button = self.browser.find_element_by_xpath("//input[@value='Add']")
        select_button.submit()
        self.delay_for_recording()

        # fill in pallet rows
        self.url = self.browser.current_url
        self.browser.find_element_by_id('id_build_pallet-loc_row').click()
        self.delay_for_recording()
        pallet_row_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_row'))
        self.delay_for_recording()
        pallet_row_select.select_by_index(self.select_random_dropdown(3))
        self.delay_for_recording()
        self.browser.find_element_by_id('id_build_pallet-loc_bin').click()
        self.delay_for_recording()
        pallet_bin_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_bin'))
        self.delay_for_recording()
        pallet_bin_select.select_by_index(self.select_random_dropdown(4))
        self.delay_for_recording()
        self.browser.find_element_by_id('id_build_pallet-loc_tier').click()
        self.delay_for_recording()
        pallet_tier_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_tier'))
        self.delay_for_recording()
        pallet_tier_select.select_by_index(self.select_random_dropdown(5))
        self.delay_for_recording()

        # scan a box
        scan_a_box = self.browser.find_element_by_xpath('//button[@data-target="#scannerModal"]')
        scan_a_box.click()
        self.delay_for_recording()

        # modal box
        key_in_box_number = self.browser.find_element_by_id('boxNumber')
        key_in_box_number.send_keys(self.make_random_box(not self.name)) # digits only
        scan_button = self.browser.find_element_by_id('scanButton')
        self.delay_for_recording()
        scan_button.click()  # return to build a pallet
        self.delay_for_recording()

        # select product
        self.browser.find_element_by_id('id_box_forms-0-product').click()
        self.delay_for_recording()
        product_select = Select(self.browser.find_element_by_id('id_box_forms-0-product'))
        product_select.select_by_index(self.select_random_dropdown(10))
        self.browser.find_element_by_id('id_box_forms-0-exp_year').click()
        year_select = Select(self.browser.find_element_by_id('id_box_forms-0-exp_year'))
        self.delay_for_recording()
        year_select.select_by_index(self.select_random_dropdown(4))
        self.delay_for_recording()
        self.browser.find_element_by_id('id_box_forms-0-exp_month_start').click()
        month_start = self.browser.find_element_by_id('id_box_forms-0-exp_month_start')
        month_start.send_keys(self.select_random_dropdown(1))
        month_end = self.browser.find_element_by_id('id_box_forms-0-exp_month_end')
        month_end.send_keys(self.select_random_dropdown(12))
        ### works for scan another box = self.browser.find_element_by_xpath('//button[@data-target="#scannerModal"]')
        # syntax for hairy elements!!!
        self.browser.find_element_by_xpath("//button[contains (.,'Pallet Complete')]").click()
        self.delay_for_recording()

        # Pallet Complete
        self.assertIn("Build Pallet Confirmation", self.browser.title)
        self.browser.find_element_by_link_text('Return to main page.').click()
        self.delay_for_recording()

        # Back to main page
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)

        self.fail('Test Completed')



class SelectPallet(TestCase):
    url = ""

    # delay for video recording
    RECORD = True

    def delay_for_recording(self):
        if self.RECORD:
            time.sleep(5)
        else:
            time.sleep(1)  # delay to make sure page loads

    name = True

    def make_random_box(self, name):
        # makes random 5 letter box names/numbers to mitigate duplicate errors
        # make sure random is called with current time as a seed value
        random.seed()
        if name:
            return ''.join(random.choice(string.ascii_letters) for _i in range(5))
        else:
            return ''.join(random.choice(string.digits) for _i in range(5))

    def select_random_dropdown(self, dropdown_int):
        random.seed()
        # return ''.join(random.choice(string.digits) for _i in range(dropdown_int))
        return random.randint(1, dropdown_int)

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.set_window_size(1920, 1080)
        self.browser.set_window_position(0, 0)
        self.url = "http://localhost:8000"

    def tearDown(self):
        self.delay_for_recording()
        # self.browser.quit()


    def test_Select(self):
        global url
        self.browser.get(self.url)
        self.assertIn("Login", self.browser.title)

        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys(user)
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys(pass_word)
        # self.browser.find_element_by_tag_name("form").click()
        login.submit()
        self.delay_for_recording()
        self.url = self.browser.current_url

        self.browser.get(self.url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()
        self.delay_for_recording()

        self.url = self.browser.current_url
        self.assertIn("Build Pallet", self.browser.title)
        self.browser.find_element_by_id('id_pallet').click()
        self.delay_for_recording()
        select_pallet = Select(self.browser.find_element_by_id('id_pallet'))
        select_pallet.select_by_index(self.select_random_dropdown(2))
        # name_of_pallet.send_keys('purple')
        self.delay_for_recording()
        # use xpath with input not submit!
        select_button = self.browser.find_element_by_xpath("//input[@value='Select']")
        select_button.submit()
        self.delay_for_recording()
