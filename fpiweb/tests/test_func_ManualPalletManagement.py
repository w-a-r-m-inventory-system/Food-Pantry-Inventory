__author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "05/5/20"

from selenium import webdriver
import geckodriver_autoinstaller  # https://pypi.org/project/geckodriver-autoinstaller/
from selenium.webdriver.support.ui import Select
from . import utility
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options  # headless mode
import time
import random


class ManualPalletMaintenance(StaticLiveServerTestCase):

    fixtures = ['BoxType.json', 'LocBin.json', 'LocRow.json', 'LocTier.json',
                'Location.json', 'ProductCategory.json', 'Product.json',
                'Box.json', 'Pallet.json','PalletBox.json', 'Constraints.json']

    test_user = ""

    # run in headless modw- check this works
    def run_headless_browser(self, cls):
        options = Options()  # headless mode
        options.headless = True  # headless mode
        cls.browser = webdriver.Firefox(options=options)  # headless mode

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
        geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
                                            # and if it doesn't exist, download it automatically,
                                            # then add geckodriver to path
        # options = Options()  # headless mode
        # options.headless = True  # headless mode
        # cls.browser = webdriver.Firefox(options=options)  # headless mode
        cls.browser = webdriver.Firefox()     # browser head mode
        cls.browser.delete_all_cookies()
        cls.browser.set_window_position(0, 0)
        # weird size is so I can get the entire web page video recorded without scrolling
        cls.browser.set_window_size(2100, 1181)


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
        row_location.select_by_index(1)
        bin_location = Select(self.browser.find_element_by_id("id_to-loc_bin"))
        bin_location.select_by_index(3)
        tier_location = Select(self.browser.find_element_by_id("id_to-loc_tier"))
        tier_location.select_by_index(2)

        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()


    # Move box to pallet with boxes
    def test_1B_MovePallet(self):
        fname = "test_Move_a_pallet"
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
        row_location.select_by_index(1)
        bin_location = Select(self.browser.find_element_by_id("id_to-loc_bin"))
        bin_location.select_by_index(3)
        tier_location = Select(self.browser.find_element_by_id("id_to-loc_tier"))
        tier_location.select_by_index(6)

        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()


    # Attempt to move box from empty pallet
    def test_1C_MovePallet(self):
        fname = "test_Move_a_pallet"
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
        row_location.select_by_index(1)
        bin_location = Select(self.browser.find_element_by_id("id_to-loc_bin"))
        bin_location.select_by_index(3)
        tier_location = Select(self.browser.find_element_by_id("id_to-loc_tier"))
        tier_location.select_by_index(6)

        submit_query_button = self.browser.find_element_by_xpath("//input[@type='submit']")
        submit_query_button.submit()
        self.delay_for_recording()


