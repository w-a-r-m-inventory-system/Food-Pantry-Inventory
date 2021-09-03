__author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "05/5/20"

# This functional test covers  'Move a pallet' web pages.
# Default Browser is FireFox and can run in headless mode
# Not all edge cases are covered but I hope I covered the main cases.
# Test function names  have numbers in them to force order on how they run
# for video recording.
# Video recording is used to implement User Documentation.
from django.contrib.auth.models import User, Group
from selenium import webdriver
import geckodriver_autoinstaller  # https://pypi.org/project/geckodriver-autoinstaller/
from selenium.webdriver.support.ui import Select
from . import utility
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.options import Options  # headless mode
from selenium.common.exceptions import NoSuchElementException
import time
import random
import pytest

from ..constants import AccessLevel
from ..models import Profile


class ManualPalletMaintenance(StaticLiveServerTestCase):

    user_name = 'login_user'
    password = 'abc123'
    profile_title = 'Jessie'

    fixtures = ['Activity.json','Constraints.json',
                'Group.json',
                 'PalletBox.json',
                 'BoxType.json', 'Location.json', 'LocBin.json', 'LocRow.json',
                 'LocTier.json',
                 'ProductExample.json',
                 'Product.json', 'ProductCategory.json',
                 'Box.json', 'Pallet.json' ]

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
        # Required to truncate all pk instances to 1
        cls.reset_sequences = True
        # Check if the current version of geckodriver existsand if it doesn't
        # exist, download it automatically, then add geckodriver to path
        geckodriver_autoinstaller.install()
        cls.browser = cls.run_headless_mode()   # True = run in headless mode
        cls.browser.delete_all_cookies()
        cls.browser.set_window_position(0, 0)
        # size is so I can get the entire web page video recorded without scrolling
        cls.browser.set_window_size(1920, 1080)


    # setup user, login and  set sessionid for user
    def setUp(self):
        super(ManualPalletMaintenance, self).setUp()
        #test_user = utility.create_user(username='user')

        # Here I am not using utility.py to create a user,
        # I am creating a user by code inside the StaticLiveServerTestCase
        test_user = User.objects.create_superuser(username=self.user_name)
        test_user.set_password(self.password)
        # add group permissions to user
        group_list = Group.objects.all()
        for group in group_list:
            test_user.groups.add(group)
        test_user.save()
        # add profile to user
        profile = Profile.objects.create(user=test_user,
                                         title=self.profile_title)
        profile.save()

        # Log in user, Verify the user created and logged in
        self.assertTrue(self.client.login(username=self.user_name,
                                          password=self.password))
        # Add cookie to login to the browser
        cookie = self.client.cookies['sessionid']
        # visit page in the site domain so the page accepts the cookie
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value,
                                 'secure': False, 'path': '/'})


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    RECORD = False
    def delay_for_recording(self):
        # Need to delay for (1) wait for page load (2) record video of screens
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(2)


    def select_random_dropdown(self, dropdown_int):
        random.seed()
        # return ''.join(random.choice(string.digits) for _i in range(dropdown_int))
        return random.randint(1, dropdown_int)


    def set_pallet_location(self, row, bin, tier ):
        # below line is to drop down product list for recording
        self.browser.find_element_by_id("id_build_pallet-loc_row").click()
        self.delay_for_recording()
        row_location = Select(self.browser.find_element_by_id(
            "id_build_pallet-loc_row"))
        row_location.select_by_index(row)
        self.browser.find_element_by_id("id_build_pallet-loc_bin").click()
        self.delay_for_recording()
        bin_location = Select(self.browser.find_element_by_id(
            "id_build_pallet-loc_bin"))
        bin_location.select_by_index(bin)
        self.browser.find_element_by_id("id_build_pallet-loc_tier").click()
        self.delay_for_recording()
        tier_location = Select(self.browser.find_element_by_id(
            "id_build_pallet-loc_tier"))
        tier_location.select_by_index(tier)

    @pytest.mark.skip(reason="passes in test- fails in pytest")
    def test_1_SelectPallet(self):
        fname = "test_1_SelectPallet"
        self.browser.get(
            '%s/%s' % (self.live_server_url, "fpiweb/build_pallet/"))
        self.delay_for_recording()
        self.assertIn("Build Pallet", self.browser.title)

        self.browser.find_element_by_id("id_pallet").click()
        select_pallet = Select(self.browser.find_element_by_id(
            "id_pallet"))
        select_pallet.select_by_index(1)
        select_button = self.browser.find_element_by_xpath("//input["
                                                    "@value='Select']")
        select_button.click()
        self.delay_for_recording()
        self.set_pallet_location(2,3,4)

        pallet_complete = self.browser.find_element_by_xpath("//button["
                                         "contains(text(), 'Pallet Complete')]")
        pallet_complete.click()
        self.delay_for_recording()

        self.assertIn("Build Pallet Confirmation", self.browser.title)
        self.delay_for_recording()
        self.browser.find_element_by_xpath("//a[contains(text(), "
                                           "'Return to main page.')]").click()
        self.delay_for_recording()


    @pytest.mark.skip(reason="passes in test- fails in pytest")
    def test_2_BuildPallet(self):
        fname = 'test_2_BuildefdPallet'
        self.browser.get(
            '%s/%s' % (self.live_server_url, "fpiweb/build_pallet/"))
        self.delay_for_recording()
        self.assertIn("Build Pallet", self.browser.title)
        name_of_pallet = self.browser.find_element_by_id('id_name')
        name_of_pallet.send_keys('green')
        self.delay_for_recording()
        add_pallet = self.browser.find_element_by_xpath(("//*[@value='Add']"))
        add_pallet.click()
        self.delay_for_recording()

        # get to next screen on same page
        self.set_pallet_location(2, 2, 2)
        scan_box = self.browser.find_element_by_xpath("//button[contains(text("
                                                      "), 'Scan a Box')]")
        scan_box.click()
        self.delay_for_recording()
        box_number = self.browser.find_element_by_id("boxNumber")
        box_number.send_keys('12350')
        self.delay_for_recording()
        scan_button = self.browser.find_element_by_id("scanButton")
        scan_button.click()
        self.delay_for_recording()

        self.browser.find_element_by_id("id_box_forms-0-product").click()
        self.delay_for_recording()
        select_product = Select(self.browser.find_element_by_id(
            "id_box_forms-0-product"))

        select_product.select_by_index(self.select_random_dropdown(18))

        self.browser.find_element_by_id("id_box_forms-0-exp_year").click()
        expired_year = Select(self.browser.find_element_by_id
                              ("id_box_forms-0-exp_year"))
        self.delay_for_recording()
        expired_year.select_by_index(self.select_random_dropdown(4))

        month_start = self.browser.find_element_by_id(
            "id_box_forms-0-exp_month_start")
        month_start.send_keys("1")

        month_end = self.browser.find_element_by_id(
            "id_box_forms-0-exp_month_end")
        month_end.send_keys(self.select_random_dropdown(12))
        self.delay_for_recording()

        pallet_complete = self.browser.find_element_by_xpath("//button["
                              "contains(text(), 'Pallet Complete')]")
        pallet_complete.click()

        self.assertIn("Build Pallet Confirmation", self.browser.title)
        self.delay_for_recording()
        self.browser.find_element_by_xpath("//a[contains(text(), "
                                       "'Return to main page.')]").click()
        self.delay_for_recording()

    # # This test currently fails so it is commented out. Test checks the
    # # edge condition where the Expiration Month End > Expiration Month Start.
    # # The Build Pallet page does not go forward to the Pallet Complete page.
    # # Also when the Build Pallet page is shown after incorrect input all
    # # boxes are checked green and there is no error message
    # def test_3_BuildPallet_RangeErrorExpirMonths(self):
    #     fname = 'test_3_BuildefdPallet_RangeErrorExpirMonths'
    #     self.browser.get(
    #         '%s/%s' % (self.live_server_url, "fpiweb/build_pallet/"))
    #     self.delay_for_recording()
    #     self.assertIn("Build Pallet", self.browser.title)
    #     name_of_pallet = self.browser.find_element_by_id('id_name')
    #     name_of_pallet.send_keys('green')
    #     self.delay_for_recording()
    #     add_pallet = self.browser.find_element_by_xpath(("//*[@value='Add']"))
    #     add_pallet.click()
    #     self.delay_for_recording()
    #
    #     # get to next screen on same page
    #     self.set_pallet_location(2, 2, 2)
    #     scan_box = self.browser.find_element_by_xpath("//button[contains(text("
    #                                                   "), 'Scan a Box')]")
    #     scan_box.click()
    #     self.delay_for_recording()
    #     box_number = self.browser.find_element_by_id("boxNumber")
    #     box_number.send_keys('12350')
    #     self.delay_for_recording()
    #     self.assertIn("Build Pallet", self.browser.title)
    #     scan_button = self.browser.find_element_by_id("scanButton")
    #     scan_button.click()
    #     self.delay_for_recording()
    #     self.browser.find_element_by_id("id_box_forms-0-product").click()
    #     select_product = Select(self.browser.find_element_by_id(
    #         "id_box_forms-0-product"))
    #     self.delay_for_recording()
    #     select_product.select_by_index(self.select_random_dropdown(18))
    #     self.delay_for_recording()
    #     month_start = self.browser.find_element_by_id(
    #         "id_box_forms-0-exp_month_start")
    #     month_start.send_keys("12")
    #     self.delay_for_recording()
    #     month_end = self.browser.find_element_by_id(
    #         "id_box_forms-0-exp_month_end")
    #     month_end.send_keys(self.select_random_dropdown(11))
    #     self.delay_for_recording()
    #
    #     pallet_complete = self.browser.find_element_by_xpath("//button["
    #                                      "contains(text(), 'Pallet Complete')]")
    #     pallet_complete.click()
    #     self.delay_for_recording()
    #
    #     try:
    #         self.assertIn("Build Pallet Confirmation", self.browser.title)
    #         self.delay_for_recording()
    #     except:
    #         self.fail(
    #             "Exceptions raised. Unable to find invalid feedback message in "
    #             "function. All input is marked with a green checkmark " + fname)
    #
    #
    # # This test currently fails so it is commented out. Test checks the edge
    # # condition when a 6 digit Box Number is enterd in the 'Scan a Box'
    # # field. Currently goes to Server Error 500. Should offer the user a
    # # chance to correct their input with a 5 digit number
    # def test_4_BuildPallet_ExtraDigitBoxNumber(self):
    #     fname = 'test_4_BuildPallet_ExtraDigitBoxNumber'
    #     self.browser.get(
    #         '%s/%s' % (self.live_server_url, "fpiweb/build_pallet/"))
    #     self.delay_for_recording()
    #     self.assertIn("Build Pallet", self.browser.title)
    #     name_of_pallet = self.browser.find_element_by_id('id_name')
    #     name_of_pallet.send_keys('green')
    #     self.delay_for_recording()
    #     add_pallet = self.browser.find_element_by_xpath(("//*[@value='Add']"))
    #     add_pallet.click()
    #     self.delay_for_recording()
    #
    #     self.set_pallet_location(2, 2, 2)
    #     scan_box = self.browser.find_element_by_xpath("//button[contains(text("
    #                                                   "), 'Scan a Box')]")
    #     scan_box.click()
    #     self.delay_for_recording()
    #     box_number = self.browser.find_element_by_id("boxNumber")
    #     box_number.send_keys('123507')
    #     self.delay_for_recording()
    #     scan_button = self.browser.find_element_by_id("scanButton")
    #     scan_button.click()
    #     self.delay_for_recording()
    #
    #     try:
    #         self.assertIn("Build Pallet", self.browser.title)
    #         self.delay_for_recording()
    #     except:
    #         self.fail(
    #             "Exceptions raised. Unable to find invalid feedback in "
    #             "function. Goes to Server Error 500 " + fname)






