from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')

    def test_empty_items_not_added(self):

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

    def test_duplicate_items_not_added(self):

        # User goes to home page and starts a new list

        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy wellies')

        # She accidentally enters a duplicate item

        self.get_item_input_box().send_keys('Buy wellies')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # An error message is displayed

        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "This item is already on the list",
        ))

    def test_error_messages_cleared_on_keypress(self):

        # User starts a list and causes a validation error

        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Banter too thick')

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed(),
        ))

        # She starts typing in the input box to clear the error

        self.get_item_input_box().send_keys('a')

        # The error messages disappears

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed(),
        ))

    def test_error_messages_cleared_on_click(self):

        # User starts a list and causes a validation error

        self.browser.get(self.live_server_url)

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Banter too thick')

        self.get_item_input_box().send_keys('Banter too thick')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed(),
        ))

        # She clicks inside the input box to clear the error

        self.get_item_input_box().click()

        # The error messages disappears

        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed(),
        ))