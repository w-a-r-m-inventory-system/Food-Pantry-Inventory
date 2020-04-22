__author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/21/20"

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

class ManualBoxPalletMaintenance(StaticLiveServerTestCase):

    fixtures = ['BoxType.json', 'LocBin.json', 'LocRow.json', 'LocTier.json',
                'Location.json', 'ProductCategory.json', 'Product.json',
                'Box.json',]

    test_user = ""

    RECORD = False
    def delay_for_recording(self):
        # Need to delay for (1) wait for page load (2) recording
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(2)


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()


    def setUp(self):
        super(ManualBoxPalletMaintenance, self).setUp()
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

        ####################################################################
        #
        # LOAD TEST DATA into the Test DB in this section.
        # The DB will be taken down after each test
        #
        #
        #
        ######################################################################


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


    def test_LogIn(self):
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

        # lets also test logout


    def test_ManualBoxPalletManagementPage(self):
        # Start off in main page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/index/'))
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        # Test Manual Box and Pallet Maintenance page link to Manual Box Management page
        self.browser.find_element_by_link_text("Manual Box and Pallet Maintenance").click()
        self.delay_for_recording()
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        # Test 'Manage an individual box manually page' link and return
        self.browser.find_element_by_link_text("Manage an individual box manually").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)
        self.browser.back()
        self.delay_for_recording()
        # Test 'Retrun to main page.' form ManualBox and Pallet Management page
        self.browser.find_element_by_link_text("Return to main page.").click()
        self.delay_for_recording()
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)

    '''
    def test_ManualStatusBox(self):
        # Start off in Manual Box Management page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        # Test 'Check the status of a box' link
        self.browser.find_element_by_link_text("Check the status of a box").click()
        self.delay_for_recording()
        self.assertIn("Box Status", self.browser.title)

        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("12345")
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        
        self.fail("Fails when box number entered is not in database")

        self.delay_for_recording()

        self.browser.back()
        self.fail("Fails when box number entered with 6 digits is not in database")
    '''

    def test_NewBox(self):
        # Start off in Manual Box Management page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        # Test 'Add a new box to inventory' link
        self.browser.find_element_by_link_text("Add a new box to inventory").click()
        self.delay_for_recording()
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("77777")
        box_type_select = Select(self.browser.find_element_by_id("id_box_type"))
        # no drop down list data in TestDB so test fails
        box_type_select.select_by_index(1)










