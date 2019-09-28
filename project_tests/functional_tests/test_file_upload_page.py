from selenium.webdriver.support.ui import Select
from django.conf import settings

import time
import os
from json import load

# from functional_tests import base
from project_tests.functional_tests import base


# -----------------------------------------------------------------------------------------
# TEST CLASSES
# -----------------------------------------------------------------------------------------
class HomePageStaticTests(base.StaticTests):
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
        self.assertIn(self.ELEMS["TITLE_TEXT"], self.browser.title)
    
    def test_get_image_file_button_has_correct_label_text(self):
        """
        Test whether the home page contains a button for getting images from local system.
        Check that the button has the correct text label.
        """
        cfg = self.ELEMS["UPLOAD_IMG_FORM"]["CHOOSE_IMG_LBL"]
        img_btn = self.browser.find_element_by_xpath(cfg["XPATH"])
        self.assertEqual(img_btn.get_attribute("innerText"), cfg["TEXT"])
    
    def test_page_has_upload_image_button_with_correct_text(self):
        """
        Test whether the home page has a button for uploading images to the service,
        and whether the button contains the correct text.
        """
        cfg = self.ELEMS["UPLOAD_IMG_FORM"]["CHOOSE_IMG_LBL"]
        img_btn = self.browser.find_element_by_xpath(cfg["XPATH"])
        self.assertEqual(img_btn.get_attribute("innerText"), cfg["TEXT"])

class HomePageDynamicTests(base.DynamicTests):
    """
    Tests to check whether the interactive elements of the page work as expected; e.g. button-
    clicks, selections etc.

    These tests require isolation from each other, so a browser instance is created at the 
    start of each test and destroyed at the end.
    """

    def test_clicking_choose_image_file_button_opens_window(self):
        pass

    def test_only_image_files_can_be_selected(self):
        # Try adding several non-image files..?
        # Can't possibly test every option - will stick with trying a few
        pass

    def test_clicking_upload_button_gets_file(self):
        upload_button = self.browser.find_element_by_id(self.ELEMS["UPLOAD_IMG_FORM"]["CHOOSE_IMG_BTN"]["ID"])
        file_path = os.path.join(settings.MEDIA_DIR, self.PATHS["TEST_IMG"]["DIR"], self.PATHS["TEST_IMG"]["FILE"])
        upload_button.send_keys(file_path)
        # self.assertEqual(file_path)
        print(f"Inner text: {upload_button.get_attribute('innerText')}")

    def test_success_message_is_shown(self):
        pass