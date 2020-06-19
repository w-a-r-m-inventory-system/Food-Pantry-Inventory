__author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/21/20"

# This functional test covers  all the Manual Box Management web pages.
# Basic login is also covered in this functional test.
# Not all edge cases are covered but I hope I covered the main cases.
# Test function names  have numbers in them to force order on how they run
# for video recording.
# Video recording is used to implement User Documentation.

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from . import utility
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

# curious why this shows an error?
from fpiweb.models import \
    Activity, \
    Box, \
    BoxType, \
    Product


import time
import random
import string

class ManualBoxManagement(StaticLiveServerTestCase):

    fixtures = ['BoxType.json', 'LocBin.json', 'LocRow.json', 'LocTier.json',
                'Location.json', 'ProductCategory.json', 'Product.json',
                'Box.json', 'Pallet.json','PalletBox.json', 'Constraints.json']

    test_user = ""

    RECORD = False
    def delay_for_recording(self):
        # Need to delay for (1) recording or  (2) wait for new page to load
        if self.RECORD:
            time.sleep(5)
        else:
            time.sleep(2)


    # used to select a random element from a dropdown list
    def select_random_dropdown(self, dropdown_int):
        random.seed()
        # return ''.join(random.choice(string.digits) for _i in range(dropdown_int))
        return random.randint(1,dropdown_int)


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.delete_all_cookies()
        cls.browser.set_window_position(0, 0)
        # weird size is so I can get the entire web page recorded without scrolling
        cls.browser.set_window_size(2100, 1181)


    # sets up user to login with StaticLIveServerTestCase
    def setUp(self):
        super(ManualBoxManagement, self).setUp()
        test_user = utility.create_user('test', 'user')
        test_user.set_password(utility.default_password)
        test_user.save()

        # Login the user
        self.assertTrue(self.client.login(username=test_user,
                                          password=utility.default_password))
        # Add cookie to login to the browser
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value,
                                 'secure': False, 'path': '/'})


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


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


    # Tests login
    def test_1LogIn(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Login", self.browser.title)
        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys('tuser')     # from utility.
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys(utility.default_password)
        self.browser.find_element_by_tag_name("form").click()
        login.submit()
        # Go to main page
        self.delay_for_recording()
        self.browser.get(self.browser.current_url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)

        # Should also test logout sometime in the future.


