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
                'Box.json', 'Pallet.json','PalletBox.json', 'Constraints.json']

    test_user = ""

    RECORD = False
    def delay_for_recording(self):
        # Need to delay for (1) wait for page load (2) recording
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(2)


    def select_random_dropdown(self, dropdown_int):
        random.seed()
        # return ''.join(random.choice(string.digits) for _i in range(dropdown_int))
        return random.randint(1,dropdown_int)


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.browser = webdriver.Firefox()
        cls.browser.delete_all_cookies()


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
        ######################################################################


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


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

        # lets also test logout


    def test_2ManualBoxPalletManagementPage(self):
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


    def test_3ManualStatusBox(self):
        fname="test_ManualStatusBox"
        # Start off in Manual Box Management page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        # Test 'Check the status of a box' link
        self.browser.find_element_by_link_text("Check the status of a box").click()
        self.delay_for_recording()
        self.assertIn("Box Status", self.browser.title)

        # test for valid box number
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("12345")
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()

        # test for box number not in database
        self.browser.back()
        self.delay_for_recording()
        self.assertIn("Box Status", self.browser.title)
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.clear()
        box_number.send_keys("77777")
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()
        if self.browser.title.__contains__("Server Error"):
            self.fail("Test fails when entering invalid Box Number, 500 page displayed in " +
                      fname)

    def test_4AddNewBox(self):
        fname= "test_AddNewBox"
        # Start off in Manual Box Management page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        # Test 'Add a new box to inventory' link with valid new box number
        self.browser.find_element_by_link_text("Add a new box to inventory").click()
        self.delay_for_recording()
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("77777")
        box_type_select = Select(self.browser.find_element_by_id("id_box_type"))
        box_type_select.select_by_index(self.select_random_dropdown(2))
        add_button = self.browser.find_element_by_xpath("//input[@value='Add Box']")
        add_button.submit()
        self.delay_for_recording()
        try:
            self.assertTrue(self.browser.find_element_by_xpath("//input[@value='confirmation' "
                                                               "and @type='hidden']"))
        except:
            self.fail("Exceptions raised. Failed to add New Box in function " + fname)

        # Test 'Add a new box to inventory' with a box number already in dataset
        self.browser.find_element_by_link_text("Add another box").click()
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("77777")
        box_type_select = Select(self.browser.find_element_by_id("id_box_type"))
        box_type_select.select_by_index(self.select_random_dropdown(2))
        add_button = self.browser.find_element_by_xpath("//input[@value='Add Box']")
        add_button.submit()
        self.delay_for_recording()
        try:
            # Look for error message
            self.browser.find_element_by_class_name("invalid-feedback")
        except:
            self.fail("Unable to find invalid-feedback in " + fname)

        # Verify 'Cancel Adding a Box' works
        self.browser.find_element_by_link_text("Cancel Adding a Box").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)


    def test_5CheckinBox(self):
        fname = "test_CheckinBox"
        # Start off in Manual Box Management page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        # Test 'Check in a box' link with valid new box number
        self.browser.find_element_by_link_text("Checkin a box").click()
        self.delay_for_recording()
        self.assertIn("Checkin a Box", self.browser.title)
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("12345")
        select_product = Select(self.browser.find_element_by_id("id_product"))
        select_product.select_by_index(self.select_random_dropdown(19))

        row_location = Select(self.browser.find_element_by_id("id_loc_row"))
        row_location.select_by_index(self.select_random_dropdown(4))
        bin_location = Select(self.browser.find_element_by_id("id_loc_bin"))
        bin_location.select_by_index(self.select_random_dropdown(9))
        tier_location = Select(self.browser.find_element_by_id("id_loc_tier"))
        tier_location.select_by_index(self.select_random_dropdown(6))

        exp_year = Select(self.browser.find_element_by_id("id_exp_year"))
        exp_year.select_by_index(self.select_random_dropdown(4))
        exp_month_start = Select(self.browser.find_element_by_id("id_exp_month_start"))
        exp_month_start.select_by_index(1)
        exp_month_end = Select(self.browser.find_element_by_id("id_exp_month_end"))
        exp_month_end.select_by_index(self.select_random_dropdown(12))

        set_box_checkin_button = self.browser.find_element_by_xpath("//input[@value='Set Box Checkin Information']")
        set_box_checkin_button.submit()
        self.delay_for_recording()
        self.browser.find_element_by_xpath("//div[contains(text(),'has been successfully')]")
        self.browser.find_element_by_link_text("Return to Manual Box Menu").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)
        self.delay_for_recording()

        # Verify that invalid box number handled
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manual_checkin_box/'))
        self.assertIn("Checkin a Box", self.browser.title)
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("77777")
        select_product = Select(self.browser.find_element_by_id("id_product"))
        select_product.select_by_index(self.select_random_dropdown(19))

        row_location = Select(self.browser.find_element_by_id("id_loc_row"))
        row_location.select_by_index(self.select_random_dropdown(4))
        bin_location = Select(self.browser.find_element_by_id("id_loc_bin"))
        bin_location.select_by_index(self.select_random_dropdown(9))
        tier_location = Select(self.browser.find_element_by_id("id_loc_tier"))
        tier_location.select_by_index(self.select_random_dropdown(6))

        exp_year = Select(self.browser.find_element_by_id("id_exp_year"))
        exp_year.select_by_index(self.select_random_dropdown(4))
        exp_month_start = Select(self.browser.find_element_by_id("id_exp_month_start"))
        exp_month_start.select_by_index(1)
        exp_month_end = Select(self.browser.find_element_by_id("id_exp_month_end"))
        exp_month_end.select_by_index(self.select_random_dropdown(12))

        set_box_checkin_button = self.browser.find_element_by_xpath("//input[@value='Set Box Checkin Information']")
        set_box_checkin_button.submit()
        self.delay_for_recording()
        # find <li> item that contains 'Invalid box number' text
        self.browser.find_element_by_xpath("//li[contains(text(),'Invalid box number')]")
        # find class with name  'invalid feedback'
        self.browser.find_element_by_class_name("invalid-feedback")
        # Cancel Box Check in
        self.browser.find_element_by_link_text("Cancel Box Check In").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)


    def test_6Checkout_a_box(self):
        fname = "test_CheckinBox"
        # Start out in Manual Box Management
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        # Test 'Checkout (consume product in) a box' link
        self.browser.find_element_by_link_text("Checkout (consume product in) a box").click()
        self.delay_for_recording()
        self.assertIn("Consume Box", self.browser.title)

        box_number = self.browser.find_element_by_id("id_box_number")
        # Use box number from fixtures/Box.json
        box_number.send_keys("12345")
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()

        consume_button = self.browser.find_element_by_xpath("//input[@value='Consume']")
        consume_button.submit()
        self.delay_for_recording()

        return_to_manual_box_menu = self.browser.find_element_by_link_text("Return to Manual Box Menu")
        return_to_manual_box_menu.click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)

        # Test for Empty Box & 'Cancel Box Consumption' link
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        self.browser.find_element_by_link_text("Checkout (consume product in) a box").click()
        self.delay_for_recording()
        self.assertIn("Consume Box", self.browser.title)
        box_number = self.browser.find_element_by_id("id_box_number")
        # Use box number from above
        box_number.send_keys("12345")
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()
        # find <li> item that contains the following text
        self.browser.find_element_by_xpath("//li[contains(text(),'Box number missing or box is empty')]")
        # find class with name  'invalid feedback'
        self.browser.find_element_by_class_name("invalid-feedback")
        self.browser.find_element_by_link_text("Cancel Box Consumption").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)


    def test_7Move_a_box(self):
        fname = "test_Move_a_box"
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        self.browser.find_element_by_link_text("Move a box").click()
        self.delay_for_recording()
        self.assertIn("Move Box", self.browser.title)

        box_number = self.browser.find_element_by_id("id_box_number")
        # Use box number from fixtures/Box.json
        box_number.send_keys("12345")
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()

        # Test does not check if moved to same location, uses random choices
        row_location = Select(self.browser.find_element_by_id("id_loc_row"))
        row_location.select_by_index(self.select_random_dropdown(4))
        bin_location = Select(self.browser.find_element_by_id("id_loc_bin"))
        bin_location.select_by_index(self.select_random_dropdown(9))
        tier_location = Select(self.browser.find_element_by_id("id_loc_tier"))
        tier_location.select_by_index(self.select_random_dropdown(6))

        move_button = self.browser.find_element_by_xpath("//input[@value='Move']")
        move_button.submit()
        self.delay_for_recording()

        self.browser.find_element_by_xpath("//div[contains(text(),'has been successfully')]")
        self.browser.find_element_by_link_text("Return to Manual Box Menu").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)

        # Check for invalid box number
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manual_move_box/'))
        self.assertIn("Move Box", self.browser.title)
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("77777")
        search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        search_button.submit()
        self.delay_for_recording()
        # Find <li> item that contains 'Box number invalid' text
        self.browser.find_element_by_xpath("//li[contains(text(),'Box number invalid')]")
        # find class with name  'invalid feedback'
        self.browser.find_element_by_class_name("invalid-feedback")
        self.browser.find_element_by_link_text("Cancel Box Move").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)











