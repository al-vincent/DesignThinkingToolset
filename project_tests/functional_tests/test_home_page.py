from selenium.webdriver.support.ui import Select
from django.conf import settings

import time
import os
from json import load

# from functional_tests import base
from project_tests.functional_tests import base


# =========================================================================================
# STATIC TESTS
# =========================================================================================
class HomePageStaticTests(base.StaticTests):
    """
    Tests to check whether the main page elements exist and render correctly when the 
    user first browses to the page.
    
    None of the tests change any values / run any javascript / etc., so the order in
    which the tests are run is irrelevant. This also means that the browser does *NOT*
    need to be created and destroyed after each test; instead, it can be spun up once
    at the start of the test suite and torn down at the end.
    """

    # NAVBAR = self.ELEMS["BASE"]["NAVBAR"]
    # STEPPER = self.ELEMS["APP"]["STEPPER"]

    # -------------------------------------------------------------------------------------
    # Page tests
    # -------------------------------------------------------------------------------------
    def test_page_uses_app_template(self):
        """
        Check that the app uses the index.html template.
        
        NOTE that although index.html will inherit from the app template, we don't have 
        to test this explicitly. If the inheritance works, the page will be rendered 
        correctly and the tests will pass; if it doesn't work correctly, the tests will 
        fail and we'll need to fix.
        """
        response = self.client.get("/")
        self.assertTemplateUsed(response, self.PATHS["PAGES"]["HOME"])

    def test_page_has_correct_title(self):
        """
        Ensure that the page title includes the correct text.
        """
        self.assertIn(self.ELEMS["TITLE"], self.browser.title)
    
    # -------------------------------------------------------------------------------------
    # Navbar tests
    # -------------------------------------------------------------------------------------
    def test_navbar_is_displayed(self):
        navbar = self.browser.find_element_by_id(self.ELEMS["BASE"]["NAVBAR"]["ID"])
        self.assertTrue(navbar.is_displayed())

    def test_navbar_has_logo(self):
        pass

    def test_navbar_uses_correct_logo(self):
        pass

    def test_navbar_about_link_is_displayed(self):
        about_link = self.browser.find_element_by_id(self.ELEMS["BASE"]["NAVBAR"]["ABOUT"]["ID"])
        self.assertTrue(about_link.is_displayed())

    def test_navbar_faq_link_is_displayed(self):
        faq_link = self.browser.find_element_by_id(self.ELEMS["BASE"]["NAVBAR"]["FAQ"]["ID"])
        self.assertTrue(faq_link.is_displayed())
    
    # -------------------------------------------------------------------------------------
    # Stepper bar tests
    # -------------------------------------------------------------------------------------
    def test_stepper_bar_is_displayed(self):
        pass

    def test_stepper_bar_has_correct_steps(self):
        pass

    def test_step_1_is_active(self):
        pass

    def test_step_2_is_inactive(self):
        pass

    def test_step_3_is_inactive(self):
        pass

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    def test_text_is_displayed(self):
        pass

    def test_text_is_correct(self):
        pass

    # -------------------------------------------------------------------------------------
    # Choose-image button tests
    # -------------------------------------------------------------------------------------
    def test_choose_image_button_is_displayed(self):
        pass

    def test_choose_image_button_is_active(self):
        pass
    
    def test_choose_image_button_has_correct_label_text(self):
        """
        Test whether the home page has a button for uploading images to the service,
        and whether the button contains the correct text.
        """
        cfg = self.ELEMS["HOME"]["UPLOAD_IMG_FORM"]["CHOOSE_IMG_LBL"]
        img_btn = self.browser.find_element_by_xpath(cfg["XPATH"])
        self.assertEqual(img_btn.get_attribute("innerText"), cfg["TEXT"])

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_next_button_is_displayed(self):        
        pass

    def test_next_button_is_active(self):
        # NOTE: should the button be *inactive* until an image is selected??
        # Without an image, there's no point in continuing.
        pass

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    def test_previous_button_is_not_visible(self):
        pass

    def test_previous_button_is_not_active(self):
        pass

    # -------------------------------------------------------------------------------------
    # Preview pane tests
    # -------------------------------------------------------------------------------------
    def test_preview_pane_is_rendered(self):
        pass

    def test_preview_pane_is_empty(self):
        pass


# =========================================================================================
# DYNAMIC TESTS
# =========================================================================================
class HomePageDynamicTests(base.DynamicTests):
    """
    Tests to check whether the interactive elements of the page work as expected; e.g. button-
    clicks, selections etc.

    These tests require isolation from each other, so a browser instance is created at the 
    start of each test and destroyed at the end.
    """
    # # -------------------------------------------------------------------------------------
    # # Page tests
    # # -------------------------------------------------------------------------------------
    # def test_resize_window(self):
    #     """
    #     NOTE: things to test on resize:
    #     - Navbar changes to burger menu
    #     - ...anything else?
    #     """
    #     pass

    # # -------------------------------------------------------------------------------------
    # # Navbar tests
    # # -------------------------------------------------------------------------------------
    # def test_clicking_logo_takes_user_to_home(self):
    #     pass

    # def test_clicking_about_takes_user_to_about_page(self):
    #     pass

    # def test_clicking_faq_takes_user_to_faq_page(self):
    #     pass

    # -------------------------------------------------------------------------------------
    # Stepper bar tests
    # -------------------------------------------------------------------------------------
    # None

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    # None

    # -------------------------------------------------------------------------------------
    # Choose-image button tests
    # -------------------------------------------------------------------------------------
    def test_only_image_files_can_be_selected(self):
        # Try adding several non-image files..?
        # Can't possibly test every option - will stick with trying a few
        pass

    def test_clicking_upload_button_gets_file(self):
        upload_button = self.browser.find_element_by_id(self.ELEMS["HOME"]["UPLOAD_IMG_FORM"]["CHOOSE_IMG_BTN"]["ID"])
        file_path = os.path.join(settings.MEDIA_DIR, self.PATHS["TEST_IMG"]["DIR"], self.PATHS["TEST_IMG"]["FILE"])
        upload_button.send_keys(file_path)
        # self.assertEqual(file_path)
        print(f"Inner text: {upload_button.get_attribute('innerText')}")

    # # -------------------------------------------------------------------------------------
    # # Next button tests
    # # -------------------------------------------------------------------------------------
    # def test_next_button_is_displayed(self):
    #     pass

    # def test_next_button_is_active(self):
    #     pass

    # # -------------------------------------------------------------------------------------
    # # Previous button tests
    # # -------------------------------------------------------------------------------------
    # def test_previous_button_is_not_visible(self):
    #     pass

    # def test_previous_button_is_not_active(self):
    #     pass

    # # -------------------------------------------------------------------------------------
    # # Preview pane tests
    # # -------------------------------------------------------------------------------------
    # def test_clicking_choose_image_file_button_opens_window(self):
    #     pass
