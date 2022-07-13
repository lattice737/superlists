from unittest import skip
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest

class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):

        # User goes to home page and accidentally tries to submit an empty list item
        
        # The home page refreshes, and there is an error message saying items cannot be blank

        # She tries again with some text for the item, which works

        # She tries to enter a second blank item

        # She can correct it by filling text in

        self.fail('write me!')
