__author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "05/5/20"

# This functional test covers  'Move a pallet' web pages.
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
from selenium.common.exceptions import NoSuchElementException
import time
import random


class ManualPalletMaintenance(StaticLiveServerTestCase):

    fixtures = ['BoxType.json', 'LocBin.json', 'LocRow.json', 'LocTier.json',
                'Location.json', 'ProductCategory.json', 'Product.json',
                'Box.json', 'Pallet.json','PalletBox.json', 'Constraints.json']

    test_user = ""

    # sets browser to run in headless mode or browser mode
    # depending on True/False value of HEADLESS_MODE
    HEADLESS_MODE = True
    @classmethod
    def run_headless_mode(cls):
        options = Options()  # headless mode
        options.headless = cls.HEADLESS_MODE  # headless mode True or False
        if options.headless:
            return webdriver.Firefox(options=options)  # headless mode
        else:
            return webdriver.Firefox()


    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
                                            # and if it doesn't exist, download it automatically,
                                            # then add geckodriver to path
        cls.browser = cls.run_headless_mode()   # True = run in headless mode
        cls.browser.delete_all_cookies()
        cls.browser.set_window_position(0, 0)
        # size is so I can get the entire web page video recorded without scrolling
        cls.browser.set_window_size(1920, 1080)


    # setup user, login and  set sessionid for user
    def setUp(self):
        super(ManualPalletMaintenance, self).setUp()
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


    RECORD = False
    def delay_for_recording(self):
        # Need to delay for (1) wait for page load (2) recording
        if self.RECORD:
            time.sleep(5)
        else:
            time.sleep(2)


    def select_random_dropdown(self, dropdown_int):
        random.seed()
        # return ''.join(random.choice(string.digits) for _i in range(dropdown_int))
        return random.randint(1, dropdown_int)


    # 'START_LOCATION = True' means use 'id_from-loc' while not True means use 'id_to-loc'
    START_LOCATION = True
    def set_pallet_location(self, row, bin, tier, start_location):
        if start_location:
            self.browser.find_element_by_id("id_from-loc_row").click()
            row_location = Select(self.browser.find_element_by_id("id_from-loc_row"))
            row_location.select_by_index(row)
            self.browser.find_element_by_id("id_from-loc_bin").click()
            bin_location = Select(self.browser.find_element_by_id("id_from-loc_bin"))
            bin_location.select_by_index(bin)
            self.browser.find_element_by_id("id_from-loc_tier").click()
            tier_location = Select(self.browser.find_element_by_id("id_from-loc_tier"))
            tier_location.select_by_index(tier)
        else:
            self.browser.find_element_by_id("id_to-loc_row").click()
            row_location = Select(self.browser.find_element_by_id("id_to-loc_row"))
            row_location.select_by_index(row)
            self.browser.find_element_by_id("id_to-loc_bin").click()
            bin_location = Select(self.browser.find_element_by_id("id_to-loc_bin"))
            bin_location.select_by_index(bin)
            self.browser.find_element_by_id("id_to-loc_tier").click()
            tier_location = Select(self.browser.find_element_by_id("id_to-loc_tier"))
            if self.RECORD:
                self.delay_for_recording()      # needed for a screenshot
            tier_location.select_by_index(tier)


        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()


    # Move box to empty pallet
    def test_1A_Move_a_pallet(self):
        fname = "test_Move_a_pallet"
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualmenu/'))
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Manage a pallet manually").click()
        self.delay_for_recording()
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Move a pallet").click()
        self.delay_for_recording()
        self.assertIn("Move Pallet", self.browser.title)

        # get a box is from this location
        self.set_pallet_location(1,1,1, self.START_LOCATION)
        self.browser.find_element_by_xpath("//h2[contains(text(),'Enter location to move pallet to')]")

        # send a box to this empty location
        self.set_pallet_location(1, 3, 2, not self.START_LOCATION)
        self.assertIn(
            self.browser.find_element_by_tag_name('p').text, '1 boxes moved to: row 01, bin 03, tier A2.'
        )


    # Move box to pallet that has boxes
    def test_1B_MovePallet(self):
        fname = "test_Move_a_pallet"
        # setup to move directory to "Move a pallet"?
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualmenu/'))
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Manage a pallet manually").click()
        self.delay_for_recording()
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Move a pallet").click()
        self.delay_for_recording()
        self.assertIn("Move Pallet", self.browser.title)

        # get a box is from this location
        self.set_pallet_location(1, 1, 1, self.START_LOCATION)
        self.browser.find_element_by_xpath("//h2[contains(text(),'Enter location to move pallet to')]")

        # send a box to this location where there are box(es)
        self.set_pallet_location(1, 3, 6, not self.START_LOCATION)

        # check the merge option
        self.browser.find_element_by_id("id_confirm_merge-action").click()
        self.delay_for_recording()
        action = Select(self.browser.find_element_by_id("id_confirm_merge-action"))
        action.select_by_index(1)
        self.delay_for_recording()
        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()
        self.assertIn(
            self.browser.find_element_by_tag_name('p').text, '1 boxes moved to: row 01, bin 03, tier C2.'
        )

        # check the go to new location option
        self.browser.back()
        self.browser.find_element_by_id("id_confirm_merge-action").click()
        self.delay_for_recording()
        action = Select(self.browser.find_element_by_id("id_confirm_merge-action"))
        action.select_by_index(0)
        self.delay_for_recording()
        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()
        self.browser.find_element_by_xpath("//h2[contains(text(),'Enter location to move pallet to')]")


    # Attempt to move box from empty pallet
    def test_1C_MovePallet(self):
        fname = "test_1C_Move_a_pallet testing fpiweb/manual_pallet_move"
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/manualmenu/'))
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Manage a pallet manually").click()
        self.delay_for_recording()
        self.assertIn("Manual Box and Pallet Management", self.browser.title)
        self.browser.find_element_by_link_text("Move a pallet").click()
        self.delay_for_recording()
        self.assertIn("Move Pallet", self.browser.title)

        # Select an empty pallet as determined from Location.json
        self.set_pallet_location(1, 3, 2, self.START_LOCATION)

        self.browser.find_element_by_xpath("//div[@role='alert']")
        self.browser.find_element_by_xpath("//button[@aria-label='close']").click()
        # verify alert has closed
        try:
            self.browser.find_element_by_xpath("//div[@role='alert']")
        except NoSuchElementException:
            print(f"\nAlert from {fname} has closed as expected- verified.\n")
