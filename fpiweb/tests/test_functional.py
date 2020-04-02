from selenium import webdriver
from selenium.webdriver.support.ui import Select
from django.test import TestCase
import unittest
import time


user = "babarehner"
pass_word = 'PostItNotes'
# start url
# url = "http://localhost:8000"


class LogInTest(TestCase):

    uri =""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.url = "http://localhost:8000"

    def tearDown(self):
        time.sleep(2)
        self.browser.quit()
        pass

    def test_Login(self):
        global uri
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
        time.sleep(2)
        self.url = self.browser.current_url

        self.browser.get(self.url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()
        time.sleep(2)

        self.url = self.browser.current_url
        self.assertIn("Build Pallet", self.browser.title)
        name_of_pallet = self.browser.find_element_by_name('name')
        name_of_pallet.send_keys('red14')
        # use xpath with input not submit!
        add_button = self.browser.find_element_by_xpath("//input[@value='Add']")
        add_button.submit()
        time.sleep(2)

        # fill in pallet rows
        # self.url = self.browser.current_url
        pallet_row_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_row'))
        pallet_row_select.select_by_index(1)
        pallet_bin_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_bin'))
        pallet_bin_select.select_by_index(1)
        pallet_tier_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_tier'))
        pallet_tier_select.select_by_index(1)
        time.sleep(2)

        # scan a box
        scan_a_box = self.browser.find_element_by_xpath('//button[@data-target="#scannerModal"]')
        scan_a_box.click()
        time.sleep(2)

        # modal box
        key_in_box_number = self.browser.find_element_by_id('boxNumber')
        key_in_box_number.send_keys('12345')
        scan_button = self.browser.find_element_by_id('scanButton')
        time.sleep(2)
        scan_button.click()     # return to main form


class SelectPalletTest(TestCase):
    uri = ""

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.url = "http://localhost:8000"

    def tearDown(self):
        time.sleep(10)
        self.browser.quit()
        pass

    def test_Login(self):
        global uri
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
        time.sleep(2)
        self.url = self.browser.current_url

        self.browser.get(self.url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()
        time.sleep(2)

        self.url = self.browser.current_url
        self.assertIn("Build Pallet", self.browser.title)
        pallet_select = Select(self.browser.find_element_by_id('id_pallet'))
        pallet_select.select_by_index(1)
        # use xpath with input not submit!
        select_button = self.browser.find_element_by_xpath("//input[@value='Select']")
        select_button.submit()
        time.sleep(2)


# if __name__ == '__main__':
#    unittest.main()