from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from django.test import TestCase    # a subclass of unitest.TestCase
from django.contrib.auth.models import User #create user for login
from django.test import LiveServerTestCase      # bare bones
# StaticLiveServerTestCase also imports static file
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

import time
import random
import string

# need to use this for
user = "babarehner"
pass_word = 'PostItNotes'


class LogInTest(StaticLiveServerTestCase):

    url = ""
    RECORD = False # increase delay for recording test

    def delay_for_recording(self):
        # Need to delay for (1) wait for next page or (2) recording
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(2)

    def make_random_box_names(self):
        # makes random 6 letter box names to mitigate duplicate errors
        # make sure random is called with current time as a seed value
        random.seed()
        return ''.join(random.choice(string.ascii_letters + string.digits) for _i in range(6))

    @classmethod 
    def setUpClass(cls):    # class raises a cls_atmic attribute error
        super().setUpClass()
        cls.browser = webdriver.Firefox()

    def setUp(self):
        super(LogInTest, self).setUp()
        # self.browser = webdriver.Firefox()
        # self.browser.get( "http://localhost:8000")
        test_user = User.objects.create(username='Testuser')
        test_user.set_password('senha8dg')
        test_user.save()

        '''
        # Login the user
        self.assertTrue(self.client.login(username='Testuser', password='senha8dg'))
        # Add cookie to log in the browser
        cookie = self.client.cookies['sessionid']
        self.browser.get(self.live_server_url)  # visit page in the site domain so the page accepts the cookie
        self.browser.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        '''

    def tearDown(self):
        self.delay_for_recording()
        self.browser.quit()
        super(LogInTest, self).tearDown()


    def test_login(self):
        self.browser.get(self.live_server_url)
        self.assertIn("Login", self.browser.title)
        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys('Testuser')
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys('senha8dg')
        self.browser.find_element_by_tag_name("form").click()
        login.submit()
        self.delay_for_recording()

        self.url = self.browser.current_url
        self.browser.get(self.url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()
        self.delay_for_recording()

        # self.url = self.browser.current_url
        self.assertIn("Build Pallet", self.browser.title)
        name_of_pallet = self.browser.find_element_by_name('name')
        # name_of_pallet.send_keys(self.make_random_box_names())
        name_of_pallet.send_keys('purple')
        # use xpath with input not submit!
        add_button = self.browser.find_element_by_xpath("//input[@value='Add']")
        add_button.submit()


        self.fail("Test Completed")



class TestAddPallet(TestCase):

    def test_add_pallet(self):
        global url

        self.browser.get(self.live_server_url)
        self.assertIn("Login", self.browser.title)
        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()

        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys('senha8dg')
        # self.browser.find_element_by_tag_name("form").click()
        login.submit()


        # Selenium tricky delay- <body> does not work in our use case
        WebDriverWait(self.browser, timeout=2).until(
            lambda driver: driver.find_element_by_tag_name('body'))

        # check if at http://127.0.0.1:8000/fpiweb/index/
        self.url = self.browser.current_url
        self.browser.get(self.url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()
        self.delay_for_recording()

        #self.url = self.browser.current_url
        self.assertIn("Build Pallet", self.browser.title)
        name_of_pallet = self.browser.find_element_by_name('name')
        # name_of_pallet.send_keys(self.make_random_box_names())
        name_of_pallet.send_keys('purple')
        # use xpath with input not submit!
        add_button = self.browser.find_element_by_xpath("//input[@value='Add']")
        add_button.submit()
        self.delay_for_recording()


        # fill in pallet rows
        # self.url = self.browser.current_url
        pallet_row_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_row'))
        pallet_row_select.select_by_index(1)
        pallet_bin_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_bin'))
        pallet_bin_select.select_by_index(1)
        pallet_tier_select = Select(self.browser.find_element_by_id('id_build_pallet-loc_tier'))
        pallet_tier_select.select_by_index(1)
        self.delay_for_recording()


        # scan a box
        scan_a_box = self.browser.find_element_by_xpath('//button[@data-target="#scannerModal"]')
        scan_a_box.click()
        self.delay_for_recording()

        # modal box
        key_in_box_number = self.browser.find_element_by_id('boxNumber')
        key_in_box_number.send_keys('87654')
        scan_button = self.browser.find_element_by_id('scanButton')
        self.delay_for_recording()
        scan_button.click()     # return to main form


class SelectPalletTest(TestCase):
    url = ""

    RECORD = True

    def delay_for_recording(self):
        if self.RECORD:
            time.sleep(10)
        else:
            time.sleep(1)   # delay to make sure page loads

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.url = "http://localhost:8000"

    def tearDown(self):
        self.delay_for_recording()
        self.browser.quit()
        pass

    def test_Login(self):
        global url
        self.browser.get(self.url)
        self.assertIn("Login", self.browser.title)

        login = self.browser.find_element_by_tag_name("form")
        username = self.browser.find_element_by_name("username")
        username.clear()
        username.send_keys(user)
        password = self.browser.find_element_by_id("id_password")
        password.clear()
        password.send_keys(pass_word)
        # self.browser.find_element_by_tag_name("form").click()
        login.submit()
        self.delay_for_recording()
        self.url = self.browser.current_url

        self.browser.get(self.url)
        self.assertIn("Welcome to Food Pantry Inventory System", self.browser.title)
        build_a_pallet = self.browser.find_element_by_link_text("Build a Pallet")
        build_a_pallet.click()
        self.delay_for_recording()

        self.url = self.browser.current_url
        self.assertIn("Build Pallet", self.browser.title)
        pallet_select = Select(self.browser.find_element_by_id('id_pallet'))
        pallet_select.select_by_index(1)
        # use xpath with input not submit!
        select_button = self.browser.find_element_by_xpath("//input[@value='Select']")
        select_button.submit()
        self.delay_for_recording()


# if __name__ == '__main__':
#    unittest.main()