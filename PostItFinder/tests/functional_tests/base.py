from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.conf import settings
import os
from json import load
import time


# arbitrarily use test_png.png as our setup image throughout
IMG_FILE = "test_jpg.jpg"

# -----------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------------------------------------------------------

# read in config vars
with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
    CONFIG = load(f)
    ELEMS = CONFIG["HTML"]
    PATHS = CONFIG["PATHS"]
    CONST = CONFIG["CONSTANTS"]

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
        # options.add_argument('-headless')
        return webdriver.Firefox(firefox_options=options)
    else:
        return webdriver.Chrome()

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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
    image_path = os.path.join(test_path, "resources", "test_images", IMG_FILE)
    input_elem.send_keys(image_path)

    # wait a few seconds for the image to render
    time.sleep(2)

    # click the Next button
    nxt_btn = browser.find_element_by_id(ELEMS["APP"]["NEXT_BTN"]["ID"])
    nxt_btn.click()

    # wait for the new page to render
    time.sleep(2)



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