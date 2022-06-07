from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # User goes to app homepage
        
        self.browser.get("http://localhost:8000")

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

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in the table",
        )

        # A textbox persists to invite the addition of items. User enters "Use peacock feathers to make a fly"

        self.fail("Finish the test!")
 
        # The page updates again and shows both items on the list

        # User notices a unique URL and text that indicates the list will be saved

        # The User visits the page to confirm the list is still there

        # The User goes back to sleep

if __name__ == "__main__":
    unittest.main(warnings="ignore")
