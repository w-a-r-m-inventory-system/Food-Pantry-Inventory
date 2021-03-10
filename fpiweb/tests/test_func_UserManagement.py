_author__ = 'Mike Rehner'
__project__ = "Food-Pantry-Inventory"
__creation_date__ = "08/27/20"

import time
# be able to run in headless mode
import geckodriver_autoinstaller  # https://pypi.org/project/geckodriver-autoinstaller/

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group

from selenium import webdriver
from selenium.webdriver.firefox.options import Options  # headless mode

from fpiweb.models import Profile


class UserManagementTest(StaticLiveServerTestCase):

    user_name = 'login_user'
    password = 'abc123'
    profile_title = 'Jessie'

    fixtures = ['Activity.json','Constraints.json',
                'Group.json']

    RECORD = False
    def delay_for_recording(self):
        # Need a delay for (1) wait for next page load or (2) recording
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(2)

    # sets browser to run in headless mode or browser mode depending on
    # True/False value of HEADLESS_MODE. Requires HEADLESS_MODE for valid
    # testing purposes when uploading to browserless server
    HEADLESS_MODE = False
    @classmethod
    def get_browser_mode(cls):
        options = Options()  # headless mode
        options.headless = cls.HEADLESS_MODE  # headless mode True or False
        if options.headless:
            return webdriver.Firefox(options=options)  # headless mode
        else:
            return webdriver.Firefox()  # uses Firefox browser

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Removes pk history and truncates all pk instances to 1
        cls.reset_sequences = True
        # Check if the current version of geckodriver exists and if it doesn't
        # exist, download it automatically, then add geckodriver to path
        geckodriver_autoinstaller.install()
        cls.browser = cls.get_browser_mode()
        cls.browser.delete_all_cookies()
        cls.browser.set_window_position(0, 0)
        # required size is so I can get the entire web page video recorded
        # without scrolling
        cls.browser.set_window_size(1920, 1080)


    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    def setUp(self):
        super(UserManagementTest, self).setUp()

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
        profile = Profile.objects.create(user=test_user, title
        = self.profile_title)
        profile.save()

        # Log in user, Verify the user created and logged in
        self.assertTrue(self.client.login(username=self.user_name,
                                          password=self.password))
        # Add cookie to log in the browser
        cookie = self.client.cookies['sessionid']
        # visit page in the site domain so the page accepts the cookie
        self.browser.get(self.live_server_url)
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value,
                                 'secure': False, 'path': '/'})

    # log in function
    def log_in(self, pass_word):
        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys(self.user_name)
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys(pass_word)
        self.delay_for_recording()
        self.browser.find_element_by_tag_name("form").click()
        login.submit()
        self.delay_for_recording()


    # Test login works
    def test_1_Login(self):
        fname = 'test_1_Login'
        self.browser.get(self.live_server_url)
        #self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/login/'))

        # Line below casues test to fail in pytest, passes in unitest
        self.assertIn("Login", self.browser.title)
        self.delay_for_recording()
        self.log_in(self.password)
        print(f"self.browser.title is {self.browser.title}")
        self.assertIn("Welcome to Food Pantry Inventory System",
                      self.browser.title)

    # test logout works and can log back in
    def test_2_logout(self):
        fname = 'test_2_logout'
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/index/'))
        self.delay_for_recording()
        self.assertIn("Welcome to Food Pantry Inventory System",
                      self.browser.title)
        # logout
        self.browser.find_element_by_link_text("Logout").click()
        self.delay_for_recording()
        self.assertIn("Logout", self.browser.title)
        self.browser.find_element_by_link_text("Go to login page.").click()
        self.delay_for_recording()

        # log back in
        self.assertIn("Login", self.browser.title)
        self.delay_for_recording()
        self.log_in(self.password)
        print(f"self.browser.title is {self.browser.title}")
        self.assertIn("Welcome to Food Pantry Inventory System",
                      self.browser.title)


    # test change password and login with new password
    def test_3_change_password(self):
        fname = 'test_3_change_password'
        new_password = 'Buffal00'
        self.browser.get('%s/%s' % (self.live_server_url, 'fpiweb/index/'))
        self.delay_for_recording()
        self.assertIn("Welcome to Food Pantry Inventory System",
                      self.browser.title)

        self.browser.find_element_by_link_text("Change Password").click()
        self.delay_for_recording()
        # Line below casues test to fail in pytest, passes in unitest
        self.assertIn("Change password", self.browser.title)
        change_password = self.browser.find_element_by_tag_name("form")
        old_password = self.browser.find_element_by_id("id_old_password")
        old_password.clear()
        old_password.send_keys(self.password)
        new_password1 = self.browser.find_element_by_id('id_new_password1')
        new_password1.clear()
        new_password1.send_keys(new_password)
        new_password2 = self.browser.find_element_by_id('id_new_password2')
        new_password2.clear()
        new_password2.send_keys(new_password)
        self.delay_for_recording()
        self.browser.find_element_by_tag_name("form").click()
        change_password.submit()
        self.delay_for_recording()

        self.password = new_password

        self.assertIn("Confirm Password", self.browser.title)
        self.delay_for_recording()
        self.browser.find_element_by_xpath("//div[contains("
                 "text(), 'Your password has been successfully changed.')]")
        self.browser.find_element_by_link_text("Return to main page.").click()
        self.delay_for_recording()
        self.assertIn("Welcome to Food Pantry Inventory System",
                      self.browser.title)
        self.browser.find_element_by_link_text("Logout").click()
        self.delay_for_recording()
        self.assertIn("Logout", self.browser.title)
        self.browser.find_element_by_link_text("Go to login page.").click()
        self.delay_for_recording()

        self.assertIn("Login", self.browser.title)

        self.log_in(new_password)
        self.assertIn("Welcome to Food Pantry Inventory System",
                      self.browser.title)


    # test change password, password too common
    def test_4_change_password_common(self):
        new_password = 'password'
        self.browser.get('%s/%s' % (self.live_server_url,
                                    'fpiweb/change_pswd/'))
        self.delay_for_recording()
        self.assertIn("Change password", self.browser.title)

        change_password = self.browser.find_element_by_tag_name("form")
        old_password = self.browser.find_element_by_id("id_old_password")
        old_password.clear()
        old_password.send_keys(self.password)
        new_password1 = self.browser.find_element_by_id('id_new_password1')
        new_password1.clear()
        new_password1.send_keys(new_password)
        new_password2 = self.browser.find_element_by_id('id_new_password2')
        new_password2.clear()
        new_password2.send_keys(new_password)
        self.delay_for_recording()
        self.browser.find_element_by_tag_name("form").click()
        change_password.submit()
        self.delay_for_recording()

        self.browser.find_element_by_class_name("invalid-feedback")
        self.browser.find_element_by_xpath(
            "//div[contains(text(), 'This password is too common.')]")


    # test change password, passwords don't match
    def test_5_change_password_nomatch(self):
        new_password01 = 'Buffal01'
        new_password02 = 'Buffal02'
        self.browser.get('%s/%s' % (self.live_server_url,
                                    'fpiweb/change_pswd/'))
        self.delay_for_recording()
        self.assertIn("Change password", self.browser.title)

        change_password = self.browser.find_element_by_tag_name("form")
        old_password = self.browser.find_element_by_id("id_old_password")
        old_password.clear()
        old_password.send_keys(self.password)
        new_password1 = self.browser.find_element_by_id('id_new_password1')
        new_password1.clear()
        new_password1.send_keys(new_password01)
        new_password2 = self.browser.find_element_by_id('id_new_password2')
        new_password2.clear()
        new_password2.send_keys(new_password02)
        self.delay_for_recording()
        self.browser.find_element_by_tag_name("form").click()
        change_password.submit()
        self.delay_for_recording()

        self.browser.find_element_by_class_name("invalid-feedback")
        self.browser.find_element_by_xpath(
            "//div[contains(text(), 'The two password fields didn')]")







