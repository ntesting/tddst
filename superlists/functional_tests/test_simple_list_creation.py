from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_list_and_retrieve_later(self):
        # the page show TODO in its title
        self.browser.get(self.server_url)
        self.assertIn('TODO', self.browser.title, "Server might be down?")
        
        # show inputbox for entering todos
        inputbox = self.browser.find_element_by_id('new_item')
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )
        
        # add entry via input box
        entry = 'Buy peacock feathers'
        inputbox.send_keys(entry)
        inputbox.send_keys(Keys.ENTER)
        
        # upon hitting enter redirect to list url
        list_url = self.browser.current_url
        self.assertRegex(list_url, '/lists/.+') #1
        self.check_table_for_entry(entry)


        # add a second entry
        self.browser.get(self.server_url)
        self.assertIn('TODO', self.browser.title, "Server might be down?")
        inputbox = self.browser.find_element_by_id('new_item')
        entry2 = 'Buy milk'
        inputbox.send_keys(entry2)
        inputbox.send_keys(Keys.ENTER)
        
        inputbox = self.browser.find_element_by_id('new_item')
        entry3 = 'Eat cereals'
        inputbox.send_keys(entry3)
        inputbox.send_keys(Keys.ENTER)

        # find entry in table
        list_url = self.browser.current_url
        self.assertRegex(list_url, '/lists/.+') #1
        self.check_table_for_entry(entry2)
        self.check_table_for_entry(entry3)
        
        # ---------------------------------------
        # new user visits page
        self.browser.quit()
        self.browser = webdriver.Firefox()
        
        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, list_url)

        # Again, there is no trace of Edith's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
