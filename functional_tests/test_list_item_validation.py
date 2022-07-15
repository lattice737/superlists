from unittest import skip
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        # User goes to home page and accidentally tries to submit an empty list item
        
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes, and there is an error message saying items cannot be blank

        self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:invalid'),
        )

        # She tries again with some text for the item, which works

        self.get_item_input_box().send_keys('Buy milk')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:valid'),
        )

        # The item can be submitted successfully

        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # She tries to enter a blank item again

        self.get_item_input_box().send_keys(Keys.ENTER)

        # A similar warning appears

        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:invalid'),
        )

        # She can correct it by filling text in

        self.get_item_input_box().send_keys('Make tea')
        self.wait_for(
            lambda: self.browser.find_element_by_css_selector('#id_text:valid'),
        )
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')
