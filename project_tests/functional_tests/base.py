from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
import os
from json import load


# -----------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------------------

def get_webdriver():
    """
    Choose the webdriver to use, based on the test environment.
    Chromedriver is fast and effective on Windows / local machine, but *very* fiddly to set
    up in Travis CI. Firefox / geckodriver are instead used in this environment, and run
    headlessly.
    """
    if 'BUILD_ENV' in os.environ:
        from selenium.webdriver.firefox.options import Options
        options = Options()
        options.add_argument('-headless')
        return webdriver.Firefox(firefox_options=options)
    else:
        return webdriver.Chrome()


# -----------------------------------------------------------------------------------------
# TEST TEMPLATE CLASSES
# -----------------------------------------------------------------------------------------

class StaticTests(StaticLiveServerTestCase):
    """
    Tests to check whether the main page elements exist and render correctly when the 
    user first browses to the page.
    
    None of the tests change any values / run any javascript / etc., so the order in
    which the tests are run is irrelevant. This also means that the browser does *NOT*
    need to be created and destroyed after each test; instead, it can be spun up once
    at the start of the test suite and torn down at the end.
    """
    # read in config vars
    with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)
        ELEMS = CONFIG["HTML"]
        PATHS = CONFIG["PATHS"]
        CONST = CONFIG["CONSTANTS"]

    @classmethod
    def setUpClass(cls):
        """
        Spin up the browser driver once before all tests are run
        """
        super().setUpClass()                
        # set up the webdriver
        cls.browser = get_webdriver()
        cls.browser.implicitly_wait(3)
    
    @classmethod
    def tearDownClass(cls):
        """
        Tear down the browser when all tests are complete.
        """
        cls.browser.quit()
        super().tearDownClass()
    
    def setUp(self):
        """
        Browse to the homepage. 
        
        AFAIK, Django *requires* the live_server_url to be run outside a class method; 
        otherwise, it could be put in setUpClass().
        """
        # Cornelius opens the homepage
        self.browser.get(self.live_server_url)

# -----------------------------------------------------------------------------------------

class DynamicTests(StaticLiveServerTestCase):
    """
    Tests that interract with the elements on a page, potentially changing state between
    tests. The browser is closed down after each test to ensure isolation and restarted
    at the beginning of each new test.
    """
    # read in config vars
    with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)
        ELEMS = CONFIG["HTML"]
        PATHS = CONFIG["PATHS"]
        CONST = CONFIG["CONSTANTS"]
    
    def setUp(self):
        """
        Browse to the homepage. 
        """
        # Cornelius opens the homepage
        self.browser = get_webdriver()
        self.browser.get(self.live_server_url)
    
    def tearDown(self):
        """
        Close down the browser.
        """
        self.browser.quit()