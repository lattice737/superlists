from selenium import webdriver
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
        self.fail("Finish the test!")

        # User is invited to enter a to-do item right away

        # User types "Buy peacock feathers" into a text box

        # When User presses Enter, the page updates and lists "1: Buy peacock feathers" as an item

        # A textbox persists to invite the addition of items. User enters "Use peacock feathers to make a fly"

        # The page updates again and shows both items on the list

        # User notices a unique URL and text that indicates the list will be saved

        # The User visits the page to confirm the list is still there

        # The User goes back to sleep

if __name__ == "__main__":
    unittest.main(warnings="ignore")
