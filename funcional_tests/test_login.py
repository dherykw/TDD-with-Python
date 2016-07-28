import time

from .base import FunctionalTest

TEST_EMAIL = 'pepe@mockmyid.com'


class LoginTest(FunctionalTest):
    def test_login_with_persona(self):
        # Pepe goes to the superlist site
        # and notices a "Sign in" link for the first time
        self.browser.get(self.server_url)
        self.browser.find_element_by_id('id_login').click()

        # A persona login box appears
        self.switch_to_new_window('Mozilla Persona')

        # Pepe logs in wirh his email address
        ## Use mockmyid.com for test email
        self.browser.find_element_by_id('authentication_email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_tag_name('button').click()

        # The persona windows closes
        self.switch_to_new_window('To-Do')

        # Pepe can see that he is logged in
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Refreshing the page, she sees it's a real session login,
        # not just a one-off for that page
        self.browser.refresh()
        self.wait_to_be_logged_in(TEST_EMAIL)

        # Terrified of this new feature, she reflexively clicks "logout"
        self.browser.find_element_by_id('id_logout').click()
        self.wait_to_be_logged_out(TEST_EMAIL)

        # The "logged out" status also persist after a refresh
        self.browser.refresh()
        self.wait_to_be_logged_out(TEST_EMAIL)

    def switch_to_new_window(self, text_in_title):
        retries = 60
        while retries > 0:
            for handle in self.browser.window_handles:
                self.browser.switch_to_window(handle)
                if text_in_title in self.browser.title:
                    return
            retries -= 1
            time.sleep(0.5)
        self.fail('could not find the window')
