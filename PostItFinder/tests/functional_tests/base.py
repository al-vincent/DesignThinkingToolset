from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings

import os
from json import load
import time


# -----------------------------------------------------------------------------------------
# CONSTANTS
# -----------------------------------------------------------------------------------------

# set the maximum waiting time
MAX_WAIT = 30

# arbitrarily use test_png.png as our setup image throughout
IMG_FILE = "test_jpg.jpg"

# read in config vars
with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
    CONFIG = load(f)
    ELEMS = CONFIG["HTML"]
    PATHS = CONFIG["PATHS"]
    CONST = CONFIG["CONSTANTS"]

# -----------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------------------

def get_webdriver(no_cookies=False):
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

        # this and the below temporarily block all cookies in the browser. 
        # Taken from https://stackoverflow.com/a/32381986
        if no_cookies:
            fp = webdriver.FirefoxProfile()
            fp.set_preference("network.cookie.cookieBehavior", 2)
        return webdriver.Firefox(firefox_options=options, firefox_profile=fp)
    else:
        if no_cookies:
            co = webdriver.ChromeOptions()
            co.add_experimental_option("prefs", {"profile.default_content_setting_values.cookies": 2})
            return  webdriver.Chrome(chrome_options=co)
        else:
            return webdriver.Chrome()

def get_image_file_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
    return os.path.join(test_path, "resources", "test_images", file_name)

def navigate_to_choose_image_page(browser):
    # click on the home page Start button
    start_btn_id = ELEMS["HOME"]["START_BTN"]["ID"]
    browser.find_element_by_id(start_btn_id).click()

def navigate_to_set_regions_page(browser):
    # navigate to the choose-image page from the home page
    navigate_to_choose_image_page(browser)

    # arbitrarily use test_png.png as our test image
    input_id = ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

    # get the input elements and update with the file path
    input_elem = browser.find_element_by_id(input_id)
    # the below is a bit convoluted, but should guarantee that the images are found correctly
    image_path = get_image_file_path(IMG_FILE)
    input_elem.send_keys(image_path)

    # wait a few seconds for the image to render
    time.sleep(2)

    # click the Next button
    browser.find_element_by_id(ELEMS["APP"]["NEXT_BTN"]["ID"]).click()
    
def navigate_to_analyse_text_page(browser):
    # navigate to the set-regions page
    navigate_to_set_regions_page(browser)

    # add a single region, via the Add Regions button
    browser.find_element_by_id(ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

    # wait for the results to be returned
    WebDriverWait(browser, MAX_WAIT).until(
        EC.visibility_of_element_located((By.CLASS_NAME, CONST["CLASSES"]["REGION"]))
    )

    # click the Next button
    browser.find_element_by_id(ELEMS["APP"]["NEXT_BTN"]["ID"]).click()


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
    
    # def navigate_to_choose_image_page(self):
    #     # click on the home page Start button
    #     start_btn_id = ELEMS["HOME"]["START_BTN"]["ID"]
    #     self.browser.find_element_by_id(start_btn_id).click()
    
    # def navigate_to_set_regions_page(self):
    #     # navigate to the choose-image page from the home page
    #     self.navigate_to_choose_image_page()

    #     # arbitrarily use test_png.png as our test image
    #     input_id = ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input elements and update with the file path
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', IMG_FILE)
    #     input_elem.send_keys(path)

    #     # wait a few seconds for the image to render
    #     time.sleep(2)

    #     # click the Next button
    #     nxt_btn = self.browser.find_element_by_id(ELEMS["APP"]["NEXT_BTN"]["ID"])
    #     nxt_btn.click()

    #     # wait for the new page to render
    #     time.sleep(2)

# -----------------------------------------------------------------------------------------

class DynamicTests(StaticLiveServerTestCase):
    """
    Tests that interract with the elements on a page, potentially changing state between
    tests. The browser is closed down after each test to ensure isolation and restarted
    at the beginning of each new test.
    """
        
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
    
    # def navigate_to_choose_image_page(self):
    #     # click on the home page Start button
    #     start_btn_id = ELEMS["HOME"]["START_BTN"]["ID"]
    #     self.browser.find_element_by_id(start_btn_id).click()
    
    # def navigate_to_set_regions_page(self):
    #     # navigate to the choose-image page from the home page
    #     self.navigate_to_choose_image_page()

    #     # arbitrarily use test_png.png as our test image
    #     input_id = ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input elements and update with the file path
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', IMG_FILE)
    #     input_elem.send_keys(path)

    #     # wait a few seconds for the image to render
    #     time.sleep(2)

    #     # click the Next button
    #     nxt_btn = self.browser.find_element_by_id(ELEMS["APP"]["NEXT_BTN"]["ID"])
    #     nxt_btn.click()

    #     # wait for the new page to render
    #     time.sleep(2)

# -----------------------------------------------------------------------------------------

class ExceptionTests(StaticLiveServerTestCase):
    """
    These dynamic tests cannot use the standard boilerplate setUp and tearDown
    form base.py, as they need some extra options configured.
    """
        
    def setUp(self):
        """
        Set options
        """        
        self.browser = get_webdriver(no_cookies=True)
        self.browser.get(self.live_server_url)

        # Cornelius opens the homepage
    
    def tearDown(self):
        """
        Close down the browser.
        """
        self.browser.quit()