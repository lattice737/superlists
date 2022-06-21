import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import LiveServerTestCase # replaces unittest.TestCase
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):

        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')

        if staging_server:
            self.live_server_url = f"http://{staging_server}"

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):

        start_time = time.time()

        while True:

            try:

                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')

                self.assertIn(row_text, [row.text for row in rows])

                return

            except (AssertionError, WebDriverException) as exception:

                elapsed = time.time() - start_time

                if elapsed > MAX_WAIT: raise exception

                time.sleep(0.5)

    def test_start_list(self):

        # User goes to app homepage
        
        self.browser.get(self.live_server_url)

        # The page title and header mention to-do lists
        
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("To-Do", header_text)

        # User is invited to enter a to-do item right away
        
        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            input_box.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User types "Buy peacock feathers" into a text box
        
        input_box.send_keys('Buy peacock feathers')

        # When User presses Enter, the page updates and lists "1: Buy peacock feathers" as an item

        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # A textbox persists to invite the addition of items. User enters "Use peacock feathers to make a fly"

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        # The page updates again and shows both items on the list

        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

    def test_multiple_user_urls(self):

        # User starts a new to-do list

        self.browser.get(self.live_server_url)
        
        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Buy peacock feathers')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # User's list has a unique URL

        user_url = self.browser.current_url
        self.assertRegex(user_url, '/lists/.+')

        # New User visits the website

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User's list is not shown

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # NewUser starts a new list by entering a new item

        new_input_box = self.browser.find_element_by_id("id_new_item")
        new_input_box.send_keys("Buy milk")
        new_input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')

        # NewUser gets a unique URL

        new_user_url = self.browser.current_url
        self.assertRegex(new_user_url, "/lists/.+")
        self.assertNotEqual(new_user_url, user_url)

        # User's list items should not be displayed

        page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Both users go to sleep

    def test_layout_and_styling(self):

        # User goes to home page

        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10,
        )

        input_box.send_keys('testing')
        input_box.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table("1: testing")

        input_box = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            input_box.location['x'] + input_box.size['width'] / 2,
            512,
            delta=10
        )

