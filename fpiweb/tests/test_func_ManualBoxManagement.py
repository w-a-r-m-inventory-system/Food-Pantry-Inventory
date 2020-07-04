_author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "04/21/20"

# This functional test covers  all the Manual Box Management web pages.
# Basic login is also covered in this functional test.
# Default Browser is FireFox and can run in headless mode
# Not all edge cases are covered but I hope I covered the main cases.
# Test function names  have numbers in them to force order on how they run
# for video recording.
# Video recording is used to implement User Documentation.

from selenium import webdriver
import geckodriver_autoinstaller  # https://pypi.org/project/geckodriver-autoinstaller/
from selenium.webdriver.support.ui import Select
from . import utility
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options  # headless mode
import time
import random


class ManualBoxManagement(StaticLiveServerTestCase):

    fixtures = ['BoxType.json', 'LocBin.json', 'LocRow.json', 'LocTier.json',
                'Location.json', 'ProductCategory.json', 'Product.json',
                'Box.json', 'Pallet.json','PalletBox.json', 'Constraints.json']

    test_user = ""

    # sets browser to run in headless mode or browser mode
    # depending on True/False value of HEADLESS_MODE
    HEADLESS_MODE = True
    @classmethod
    def get_browser_mode(cls):
        options = Options()  # headless mode
        options.headless = cls.HEADLESS_MODE  # headless mode True or False
        if options.headless:
            return webdriver.Firefox(options=options)  # headless mode
        else:
            return webdriver.Firefox()      # use Firefox browser


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
                                            # and if it doesn't exist, download it automatically,
                                            # then add geckodriver to path
        cls.browser = cls.get_browser_mode()
        cls.browser.delete_all_cookies()
        cls.browser.set_window_position(0, 0)
        # weird size is so I can get the entire web page video recorded without scrolling
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
        # Add cookie about login to the browser
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value,
                                 'secure': False, 'path': '/'})


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()


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
        return random.randint(1, dropdown_int)


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
        # Test 'Return to main page.' form ManualBox and Pallet Management page
        self.browser.find_element_by_link_text("Return to main page.").click()
        self.delay_for_recording()
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)


    def test_3ManualStatusBox(self):
        fname="test_3ManualStatusBox testing fpiweb/manual_box_status"
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
            print(f"\n*** {fname} fails when entering invalid box number or 6+ digit box "
                  f"number.*** \n")


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
        self.browser.find_element_by_xpath("//*[@id='id_box_type']").click()
        self.delay_for_recording()
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
        self.browser.find_element_by_xpath("//*[@id='id_box_type']").click()
        self.delay_for_recording()
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
        fname = "test_5CheckinBox"
        # Start off in Manual Box Management page
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualboxmenu/'))
        self.assertIn("Manual Box Management", self.browser.title)
        # Test 'Check in a box' link with valid new box number
        self.browser.find_element_by_link_text("Checkin a box").click()
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
        self.browser.find_element_by_link_text("Return to Manual Box Menu").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)
        self.delay_for_recording()

        # Verify that invalid box number handled
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manual_checkin_box/'))
        self.assertIn("Checkin a Box", self.browser.title)
        box_number = self.browser.find_element_by_id("id_box_number")
        box_number.send_keys("77777")
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
        # Cancel Box Check in
        self.browser.find_element_by_link_text("Cancel Box Check In").click()
        self.delay_for_recording()
        self.assertIn("Manual Box Management", self.browser.title)


    def test_6Checkout_a_box(self):
        fname = "test_6Checkout_a_box"
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
        fname = "test_7Move_a_box"
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
        self.set_location_test()

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

