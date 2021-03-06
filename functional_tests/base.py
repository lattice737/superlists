import time
import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium import webdriver

MAX_WAIT = 5

class FunctionalTest(StaticLiveServerTestCase):

    def setUp(self):

        self.browser = webdriver.Chrome()
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

    def wait_for(self, function):

        start_time = time.time()

        while True:

            try: return function()

            except (AssertionError, WebDriverException) as exception:

                elapsed = time.time() - start_time

                if elapsed > MAX_WAIT: raise exception

                time.sleep(0.5)

    def get_item_input_box(self):
        return self.browser.find_element_by_id('id_text')