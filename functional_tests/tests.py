from django.test import LiveServerTestCase # replaces unittest.TestCase
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(10)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):

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

        import time
        time.sleep(2)

        list_url = self.browser.current_url
        
        self.assertRegex(list_url, "/lists/.+")
        self.check_for_row_in_list_table("1: Buy peacock feathers")

        # A textbox persists to invite the addition of items. User enters "Use peacock feathers to make a fly"

        input_box = self.browser.find_element_by_id('id_new_item')
        input_box.send_keys('Use peacock feathers to make a fly')
        input_box.send_keys(Keys.ENTER)

        time.sleep(2)
 
        # The page updates again and shows both items on the list

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # NewUser visits the site
        
        ## A new broswer session is used to make sure none of User's info is displayed

        self.browser.quit()
        self.browser = webdriver.Firefox()

        # NewUser visits the home page. There should be no sign of User's list

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text

        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # NewUser starts a new list by entering a new item

        new_input_box = self.browser.find_element_by_id("id_new_item")
        new_input_box.send_keys("Buy milk")
        new_input_box.send_keys(Keys.ENTER)

        time.sleep(2)

        # NewUser gets a unique URL

        new_list_url = self.browser.current_url

        self.assertRegex(new_list_url, "/lists/.+")
        self.assertNotEqual(new_list_url, list_url)

        # User's list items should not be displayed

        #page_text = self.browser.find_element_by_tag_name('body').text
        
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Both users go to sleep
