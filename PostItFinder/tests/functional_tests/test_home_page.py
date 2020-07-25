from django.conf import settings
from django.urls import reverse

import time
import os
from json import load

from PostItFinder.tests.functional_tests import base


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
        
    # -------------------------------------------------------------------------------------
    # Page tests
    # -------------------------------------------------------------------------------------
    def test_page_uses_app_template(self):
        """
        Check that the app uses the index.html template.
        
        NOTE that although index.html will inherit from the base template, we don't have 
        to test this explicitly. If the inheritance works, the page will be rendered 
        correctly and the tests will pass; if it doesn't work correctly, the tests will 
        fail and we'll need to fix.
        """        
        response = self.client.get(reverse(base.ELEMS["HOME"]["URL"]))
        self.assertTemplateUsed(response, base.PATHS["HOME"])

    def test_page_has_correct_title(self):
        """
        Ensure that the page title includes the correct text.
        """
        self.assertIn(base.ELEMS["TITLE"], self.browser.title)
    
    # -------------------------------------------------------------------------------------
    # Navbar tests
    # -------------------------------------------------------------------------------------
    def test_navbar_is_displayed(self):
        navbar = self.browser.find_element_by_id(base.ELEMS["BASE"]["NAVBAR"]["ID"])
        self.assertTrue(navbar.is_displayed())

    def test_navbar_has_logo(self):
        pass

    def test_navbar_uses_correct_logo(self):
        pass

    def test_navbar_items_are_displayed(self):
        for nav_item in base.ELEMS["BASE"]["NAVBAR"]["PAGES"]:
            link = self.browser.find_element_by_id(nav_item["ID"])
            self.assertTrue(link.is_displayed())

    def test_navbar_items_show_correct_text(self):
        for nav_item in base.ELEMS["BASE"]["NAVBAR"]["PAGES"]:
            element = self.browser.find_element_by_id(nav_item["ID"])
            self.assertEqual(element.get_attribute("innerText"), nav_item["TEXT"])
    
    # -------------------------------------------------------------------------------------
    # Start button tests
    # -------------------------------------------------------------------------------------    
    def test_start_button_is_displayed(self):
        start_btn = self.browser.find_element_by_id(base.ELEMS["HOME"]["START_BTN"]["ID"])
        self.assertTrue(start_btn.is_displayed())

    def test_start_button_is_enabled(self):
        start_btn = self.browser.find_element_by_id(base.ELEMS["HOME"]["START_BTN"]["ID"])
        self.assertTrue(start_btn.is_enabled())
    
    def test_start_button_has_correct_label_text(self):
        """
        Test whether the choose-image page has a button for uploading images to the service,
        and whether the button contains the correct text.

        The label element has no ID of its own, so use XPath to find / select it.
        """
        start_btn = self.browser.find_element_by_id(base.ELEMS["HOME"]["START_BTN"]["ID"])
        expected_text = base.ELEMS["HOME"]["START_BTN"]["TEXT"]
        self.assertEqual(start_btn.get_attribute("innerText"), expected_text)

    
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
       
    # -------------------------------------------------------------------------------------
    # Page tests
    # -------------------------------------------------------------------------------------
    # def test_resize_window(self):
    #     """
    #     NOTE: things to test on resize:
    #     - Navbar changes to burger menu
    #     - ...anything else?
    #     """
    #     pass

    # -------------------------------------------------------------------------------------
    # Navbar tests
    # -------------------------------------------------------------------------------------
    # def test_clicking_logo_takes_user_to_home(self):
    #     pass

    def test_clicking_about_takes_user_to_faq_page(self):
        base_url = self.live_server_url
        page = base.ELEMS["BASE"]["NAVBAR"]["PAGES"][0]        
        page_elem = self.browser.find_element_by_id(page["ID"]).click()
        self.assertEqual(self.browser.current_url, base_url + reverse(page["URL"]))

    def test_clicking_faq_takes_user_to_faq_page(self):
        base_url = self.live_server_url
        page = base.ELEMS["BASE"]["NAVBAR"]["PAGES"][1]        
        page_elem = self.browser.find_element_by_id(page["ID"]).click()
        self.assertEqual(self.browser.current_url, base_url + reverse(page["URL"]))

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    # None

    # -------------------------------------------------------------------------------------
    # Start button tests
    # -------------------------------------------------------------------------------------
    def test_clicking_start_button_redirects_to_choose_image_page(self):
        base_url = self.live_server_url
        self.browser.find_element_by_id(base.ELEMS["HOME"]["START_BTN"]["ID"]).click()
        expected_url = reverse(base.ELEMS["HOME"]["START_BTN"]["URL"])
        self.assertEqual(self.browser.current_url, base_url + expected_url)

class HomePageExceptionTests(base.ExceptionTests):
    """
    These dynamic tests inherit from a slightly different class, as they
    need some extra options configured.
    """
 
    def test_clicking_start_with_cookies_disabled_fires_alert(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException

        # click the Start button
        self.browser.find_element_by_id(base.ELEMS["HOME"]["START_BTN"]["ID"]).click()

        try: 
            WebDriverWait(self.browser, 3).until(EC.alert_is_present(),
                                   "Timed out waiting for alert to appear.")
            alert = self.browser.switch_to.alert
            alert.accept()            
        except TimeoutException:
            self.fail("ERROR - alert was not fired")