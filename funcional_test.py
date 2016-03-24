import unittest
from selenium import webdriver


class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_start_a_new_todo_list(self):
        self.browser.get('http://localhost:8000')
        self.assertIn('To-Do', self.browser.title)


if __name__ == '__name__':
    unittest.main(warnings='ignore')
