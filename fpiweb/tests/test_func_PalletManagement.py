__author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "05/5/20"

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
            time.sleep(5)


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



    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def add_new_box(self):
        fname = "add_new_box"
        # Start off in Manual Box Management page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manual_add_box/'))
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


    def check_in_box(self):
        fname = "test_CheckinBox"
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manual_checkin_box/'))
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("77777")
        select_product = Select(self.browser.find_element_by_id("id_product"))
        select_product.select_by_index(self.select_random_dropdown(1))

        row_location = Select(self.browser.find_element_by_id("id_loc_row"))
        row_location.select_by_index(1)
        bin_location = Select(self.browser.find_element_by_id("id_loc_bin"))
        bin_location.select_by_index(1)
        tier_location = Select(self.browser.find_element_by_id("id_loc_tier"))
        tier_location.select_by_index(1)

        exp_year = Select(self.browser.find_element_by_id("id_exp_year"))
        exp_year.select_by_index(1)
        exp_month_start = Select(self.browser.find_element_by_id("id_exp_month_start"))
        exp_month_start.select_by_index(1)
        exp_month_end = Select(self.browser.find_element_by_id("id_exp_month_end"))
        exp_month_end.select_by_index(2)

        set_box_checkin_button = self.browser.find_element_by_xpath("//input[@value='Set Box Checkin Information']")
        set_box_checkin_button.submit()
        self.delay_for_recording()
        self.browser.find_element_by_xpath("//div[contains(text(),'has been successfully')]")



    def test_1_Move_a_pallet(self):
        fname = "test_Move_a_box"
        # Set up data
        self.add_new_box()
        self.check_in_box()
        # sstart test
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualmenu/'))
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Manage a pallet manually").click()
        self.delay_for_recording()
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Move a pallet").click()
        self.delay_for_recording()
        self.assertIn("Move Pallet", self.browser.title)

        row_location = Select(self.browser.find_element_by_id("id_from-loc_row"))
        row_location.select_by_index(1)
        bin_location = Select(self.browser.find_element_by_id("id_from-loc_bin"))
        bin_location.select_by_index(1)
        tier_location = Select(self.browser.find_element_by_id("id_from-loc_tier"))
        tier_location.select_by_index(1)

        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()
        self.browser.find_element_by_xpath("//h2[contains(text(),'Enter location to move pallet to')]")

        row_location = Select(self.browser.find_element_by_id("id_to-loc_row"))
        row_location.select_by_index(4)
        bin_location = Select(self.browser.find_element_by_id("id_to-loc_bin"))
        bin_location.select_by_index(9)
        tier_location = Select(self.browser.find_element_by_id("id_to-loc_tier"))
        tier_location.select_by_index(6)

        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()

        # box_number = self.browser.find_element_by_id("id_box_number")
        # # Use box number from fixtures/Box.json
        # box_number.send_keys("12345")
        # search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        # search_button.submit()
        # self.delay_for_recording()
        #
        # # Test does not check if moved to same location, uses random choices
        # row_location = Select(self.browser.find_element_by_id("id_loc_row"))
        # row_location.select_by_index(self.select_random_dropdown(4))
        # bin_location = Select(self.browser.find_element_by_id("id_loc_bin"))
        # bin_location.select_by_index(self.select_random_dropdown(9))
        # tier_location = Select(self.browser.find_element_by_id("id_loc_tier"))
        # tier_location.select_by_index(self.select_random_dropdown(6))
        #
        # move_button = self.browser.find_element_by_xpath("//input[@value='Move']")
        # move_button.submit()
        # self.delay_for_recording()
        #
        # self.browser.find_element_by_xpath("//div[contains(text(),'has been successfully')]")
        # self.browser.find_element_by_link_text("Return to Manual Box Menu").click()
        # self.delay_for_recording()
        # self.assertIn("Manual Box Management", self.browser.title)
        #
        # # Check for invalid box number
        # self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manual_move_box/'))
        # self.assertIn("Move Box", self.browser.title)
        # box_number = self.browser.find_element_by_id("id_box_number")
        # box_number.send_keys("77777")
        # search_button = self.browser.find_element_by_xpath("//input[@value='Search']")
        # search_button.submit()
        # self.delay_for_recording()
        # # Find <li> item that contains 'Box number invalid' text
        # self.browser.find_element_by_xpath("//li[contains(text(),'Box number invalid')]")
        # # find class with name  'invalid feedback'
        # self.browser.find_element_by_class_name("invalid-feedback")
        # self.browser.find_element_by_link_text("Cancel Box Move").click()
        # self.delay_for_recording()
        # self.assertIn("Manual Box Management", self.browser.title)
