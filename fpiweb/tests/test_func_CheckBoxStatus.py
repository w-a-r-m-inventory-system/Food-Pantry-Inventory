import random

from selenium import webdriver
# from django.test import TestCase
import unittest
import time
import requests

# Need to use my username and password because I don't seem to be able to use
# fixtures to load LiveStaticTestCase
from selenium.webdriver.support.select import Select

user_name = "mike"
pass_word = "PostItNotes" \

class CheckStatusBox(unittest.TestCase):

    # initialize url
    url = ""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.url = "http://localhost:8765"
        self.browser.set_window_position(0, 0)
        # size is so I can get the entire web page video recorded without scrolling
        self.browser.set_window_size(1920, 1230)

    def tearDown(self):
        self.browser.quit()
        pass

    # delay for video recording and page loads
    RECORD = True
    def delay_for_recording(self):
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(2)

    # used to select a random element from a dropdown list
    def select_random_dropdown(self, dropdown_int):
        random.seed()
        # return ''.join(random.choice(string.digits) for _i in range(dropdown_int))
        return random.randint(1, dropdown_int)


    # logs in user leaves user at Main menu page
    def login_user(self):
        self.browser.get(self.url)
        self.assertIn("Login", self.browser.title)

        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys("mike")
        password = self.browser.find_element_by_name("password")
        password.clear()
        password.send_keys("PostItNotes")
        login.submit()
        self.delay_for_recording()
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)

    # tests row, bin, tier location settings by setting location from the dropdown
    # lists presented.
    def set_location_test(self):
        self.browser.find_element_by_xpath("//*[@id='id_loc_row']").click()
        self.delay_for_recording()
        row_location = Select(self.browser.find_element_by_id("id_loc_row"))
        row_location.select_by_index(self.select_random_dropdown(4))
        self.browser.find_element_by_xpath("//*[@id='id_loc_bin']").click()
        self.delay_for_recording()
        bin_location = Select(self.browser.find_element_by_id("id_loc_bin"))
        bin_location.select_by_index(self.select_random_dropdown(9))
        self.browser.find_element_by_xpath("//*[@id='id_loc_tier']").click()
        self.delay_for_recording()
        tier_location = Select(self.browser.find_element_by_id("id_loc_tier"))
        tier_location.select_by_index(self.select_random_dropdown(6))

    def test_1_CheckStatusBox(self):
        self.login_user()
        self.url = self.browser.current_url
        # test for box number in DB
        self.browser.find_element_by_link_text("Check the status of a box").click()
        self.delay_for_recording()
        self.assertIn("Box Status", self.browser.title)
        # test for valid box number
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("12345")
        self.delay_for_recording()
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()

        # test for box number not in DB
        self.browser.get(self.url)
        self.browser.find_element_by_link_text("Check the status of a box").click()
        self.delay_for_recording()
        self.assertIn("Box Status", self.browser.title)
        # test for valid box number
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("99999")
        self.delay_for_recording()
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()

    def test_2_CheckinBox(self):
            self.login_user()


            # Test 'Check in a box' link with valid new box number
            self.browser.find_element_by_link_text("Checkin a Box").click()
            self.url = self.browser.current_url     # sve for future reference below
            self.delay_for_recording()
            self.assertIn("Checkin a Box", self.browser.title)
            box_number = self.browser.find_element_by_id("id_box_number")
            box_number.send_keys("12345")
            # line below is to show drop down for recording purposes
            self.browser.find_element_by_xpath("//*[@id='id_product']").click()
            self.delay_for_recording()
            select_product = Select(self.browser.find_element_by_id("id_product"))
            select_product.select_by_index(self.select_random_dropdown(19))

            self.set_location_test()

            self.browser.find_element_by_xpath("//*[@id='id_exp_year']").click()
            self.delay_for_recording()
            exp_year = Select(self.browser.find_element_by_id("id_exp_year"))
            exp_year.select_by_index(self.select_random_dropdown(4))
            self.browser.find_element_by_xpath("//*[@id='id_exp_month_end']").click()
            self.delay_for_recording()
            exp_month_start = Select(self.browser.find_element_by_id("id_exp_month_start"))
            exp_month_start.select_by_index(1)
            self.browser.find_element_by_xpath("//*[@id='id_exp_month_end']").click()
            self.delay_for_recording()
            exp_month_end = Select(self.browser.find_element_by_id("id_exp_month_end"))
            exp_month_end.select_by_index(self.select_random_dropdown(12))

            set_box_checkin_button = self.browser.find_element_by_xpath("//input[@value='Set Box Checkin Information']")
            set_box_checkin_button.submit()
            self.delay_for_recording()
            self.browser.find_element_by_xpath("//div[contains(text(),'has been successfully')]")
            self.delay_for_recording()
            self.browser.find_element_by_link_text("Return to Main Menu").click()
            self.delay_for_recording()
            self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
            self.delay_for_recording()

            # Verify that invalid box number handled
            self.browser.get(self.url)
            self.assertIn("Checkin a Box", self.browser.title)
            box_number = self.browser.find_element_by_id("id_box_number")
            box_number.send_keys("99999")
            self.browser.find_element_by_xpath("//*[@id='id_product']").click()
            self.delay_for_recording()
            select_product = Select(self.browser.find_element_by_id("id_product"))
            select_product.select_by_index(self.select_random_dropdown(19))

            self.set_location_test()

            self.browser.find_element_by_xpath("//*[@id='id_exp_year']").click()
            self.delay_for_recording()
            exp_year = Select(self.browser.find_element_by_id("id_exp_year"))
            exp_year.select_by_index(self.select_random_dropdown(4))
            self.browser.find_element_by_xpath("//*[@id='id_exp_month_start']").click()
            self.delay_for_recording()
            exp_month_start = Select(self.browser.find_element_by_id("id_exp_month_start"))
            exp_month_start.select_by_index(1)
            self.browser.find_element_by_xpath("//*[@id='id_exp_month_end']").click()
            self.delay_for_recording()
            exp_month_end = Select(self.browser.find_element_by_id("id_exp_month_end"))
            exp_month_end.select_by_index(self.select_random_dropdown(12))

            set_box_checkin_button = self.browser.find_element_by_xpath("//input[@value='Set Box Checkin Information']")
            set_box_checkin_button.submit()
            self.delay_for_recording()
            # find <li> item that contains 'Invalid box number' text
            self.browser.find_element_by_xpath("//li[contains(text(),'Invalid box number')]")
            # find class with name  'invalid feedback'
            self.browser.find_element_by_class_name("invalid-feedback")
            self.delay_for_recording()
            # Cancel Box Check in
            self.browser.find_element_by_link_text("Cancel Box Check In").click()
            self.delay_for_recording()
            self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)

    # def test_3_CheckoutBox(self):
    #         self.login_user()
    #
    # def test_4_BuildPallet(self):
    #         self.login_user()
    #
    # def test_5_MovePallet(self):
    #         self.login_user()
    #
    # def test_6_MoveBox(self):
    #         self.login_user()
    #
    # def test_7AddNewBox(self):
    #     self.login_user()
    #     self.browser.find_element_by_link_text("Add a new box to inventory").click()
    #     self.delay_for_recording()
    #     self.assertIn("New Box", self.browser.title)
    #     box_number = self.browser.find_element_by_id("id_box_number")
    #     box_number.send_keys("77777")
    #     self.browser.find_element_by_xpath("//*[@id='id_box_type']").click()
    #     self.delay_for_recording()
    #     box_type_select = Select(self.browser.find_element_by_id("id_box_type"))
    #     box_type_select.select_by_index(self.select_random_dropdown(2))
    #     add_button = self.browser.find_element_by_xpath("//input[@value='Add Box']")
    #     add_button.submit()
    #     self.delay_for_recording()

