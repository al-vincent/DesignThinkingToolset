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
        First simple test; ensure that the page title includes the correct text.
        """
        # He sees that the page's title includes the expected text
        self.assertIn(self.CONFIG["TITLE_TEXT"], self.browser.title)
    
    