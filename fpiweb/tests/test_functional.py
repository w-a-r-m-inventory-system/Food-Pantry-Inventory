from selenium import webdriver
# from django.test import TestCase
import unittest
import time
import requests


class LogInTest(unittest.TestCase):

    # initialize url
    url = ""

    def setUp(self):
        self.browser = webdriver.Firefox()

    #def tearDown(self):
       #self.browser.quit()

    def test_Login(self):
        self.browser.get('http://localhost:8000')
        self.assertIn("Login", self.browser.title)

        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys("babarehner")
        password = self.browser.find_element_by_name("password")
        password.clear()
        password.send_keys("PostItNotes")
        # self.browser.find_element_by_tag_name("form").click()
        login.submit()
        time.sleep(2)
        self.url = self.browser.current_url

    # def test_Build_a_Pallet(self):

        self.browser.get(self.url)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()


# if __name__ == '__main__':
#    unittest.main()