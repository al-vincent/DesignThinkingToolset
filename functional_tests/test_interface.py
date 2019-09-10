from selenium.webdriver.support.ui import Select
from django.conf import settings

import time
import os
from json import load

from functional_tests import base

# -----------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------------------
def get_webdriver():
    if 'BUILD_ENV' in os.environ:
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.add_argument('-headless')
        return webdriver.Firefox(firefox_options=options)
    else:
        return webdriver.Chrome()

# -----------------------------------------------------------------------------------------
# TEST CLASSES
# -----------------------------------------------------------------------------------------
class LoadPageTests(base.StaticTests):
    """
    Tests to check whether the main page elements exist and render correctly when the 
    user first browses to the page.
    
    None of the tests change any values / run any javascript / etc., so the order in
    which the tests are run is irrelevant. This also means that the browser does *NOT*
    need to be created and destroyed after each test; instead, it can be spun up once
    at the start of the test suite and torn down at the end.
    """
        
    def test_page_has_correct_title(self):
        """
        Ensure that the page title includes the correct text.
        """
        # He sees that the page's title includes the expected text
        self.assertIn(self.CONFIG["TITLE_TEXT"], self.browser.title)
    
    def test_page_has_button_to_get_image_from_file(self):
        """
        Test whether the home page contains a button for getting images from local system.
        Check that the button is 
        """
        cfg = self.CONFIG["UPLOAD_IMAGE_FORM"]["CHOOSE_IMAGE_LBL"]
        img_btn = self.browser.find_element_by_xpath(cfg["XPATH"])
        self.assertEqual(img_btn.get_attribute("innerText"), cfg["TEXT"])
    