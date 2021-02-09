__author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "08/27/20"

import time
# be able to run in headless mode
import geckodriver_autoinstaller  # https://pypi.org/project/geckodriver-autoinstaller/

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # headless mode

from fpiweb.models import Profile


class UserManagementTest(StaticLiveServerTestCase):

    # When including Profile.json in fixtures the following error is produced:
    # django.db.utils.IntegrityError: Problem installing fixtures: insert or update on
    # table "fpiweb_profile" violates foreign key constraint "fpiweb_profile_user_id_a87cff91_fk_auth_user_id"
    # DETAIL:  Key (user_id)=(1) is not present in table "auth_user".
    fixtures = ['Activity.json', 'Constraints.json', 'Group.json',
                'PalletBox.json',
                'BoxType.json', 'Location.json', 'LocBin.json', 'LocRow.json', 'LocTier.json',
                'ProductExample.json',
                'Product.json', 'ProductCategory.json',
                'Box.json', 'Pallet.json', ]

    RECORD = True
    def delay_for_recording(self):
        # Need a delay for (1) wait for next page load or (2) recording
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(2)

    # sets browser to run in headless mode or browser mode
    # depending on True/False value of HEADLESS_MODE
    # Requires HEADLESS_MODE for valid testing purposes when uploading to browserless server
    HEADLESS_MODE = True

    @classmethod
    def get_browser_mode(cls):
        options = Options()  # headless mode
        options.headless = cls.HEADLESS_MODE  # headless mode True or False
        if options.headless:
            return webdriver.Firefox(options=options)  # headless mode
        else:
            return webdriver.Firefox()  # use Firefox browser

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        geckodriver_autoinstaller.install()  # Check if the current version of geckodriver exists
        # and if it doesn't exist, download it automatically,
        # then add geckodriver to path
        cls.browser = cls.get_browser_mode()
        cls.browser.delete_all_cookies()
        cls.browser.set_window_position(0, 0)
        # required size is so I can get the entire web page video recorded without scrolling
        cls.browser.set_window_size(1920, 1080)


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        super(UserManagementTest, self).setUp()

        # Here I am not using utility.py to create a user,
        # I am creating a user by code inside the StaticLiveServerTestCase
        test_user = User.objects.create(username='TestUser')
        test_user.set_password('test_password')
        test_user.save()

        Profile.objects.create(user=test_user)

        # Log in user, Verify the user created and logged in
        self.assertTrue(self.client.login(username='TestUser', password='test_password'))
        # Add cookie to log in the browser
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)  # visit page in the site domain so the page accepts the cookie
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})


    def test_UserManagement(self):

        self.browser.get(self.live_server_url)
        self.assertIn("Login", self.browser.title)
        self.delay_for_recording()
        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys('TestUser')
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys('test_password')
        self.delay_for_recording()
        self.browser.find_element_by_tag_name("form").click()
        login.submit()
        self.delay_for_recording()
        print(f"self.browser.title is {self.browser.title}")
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)

        # Test change password- not implemented 8/27/20
        self.browser.find_element_by_link_text("Change Password").click()
        self.delay_for_recording()
        self.assertIn("Change password", self.browser.title)
        self.browser.find_element_by_link_text("Return to main page.").click()
        self.delay_for_recording()
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        self.delay_for_recording()

        # Test logout
        self.browser.find_element_by_link_text("Logout").click()
        self.delay_for_recording()
        self.assertIn("Logout", self.browser.title)
        self.browser.find_element_by_link_text("Go to login page.").click()
        self.delay_for_recording()

        self.assertIn("Login", self.browser.title)
        self.delay_for_recording()

