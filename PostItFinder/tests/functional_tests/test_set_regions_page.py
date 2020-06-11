from selenium.webdriver.support.ui import Select
from django.conf import settings
from django.urls import reverse

import time
import os
from json import load
import base64

from PostItFinder.tests.functional_tests import base

# =========================================================================================
# STATIC TESTS
# =========================================================================================
class SetRegionsPageStaticTests(base.StaticTests):
    """
    Tests to check whether the main page elements exist and render correctly when the 
    user first browses to the page.
    
    None of the tests change any values / run any javascript / etc., so the order in
    which the tests are run is irrelevant. This also means that the browser does *NOT*
    need to be created and destroyed after each test; instead, it can be spun up once
    at the start of the test suite and torn down at the end.
    """

    def setUp(self):
        """
        setUp() in base.py navigates to the home page. We then need to select an image
        and click the Next button.
        """                
        # call the 'normal' setUp from the base class
        super().setUp()

        # navigate to the set-regions page, via home and choose-image
        base.navigate_to_set_regions_page(self.browser)

    # -------------------------------------------------------------------------------------
    # Page tests
    # -------------------------------------------------------------------------------------
    def test_page_uses_app_template(self):
        """
        Check that the app uses the set-regions.html template.
        """
        response = self.client.get(reverse(base.ELEMS["SET_REGIONS"]["URL"]))
        self.assertTemplateUsed(response, base.PATHS["SET_REGIONS"])

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
    # Stepper bar tests
    # -------------------------------------------------------------------------------------
    def test_stepper_bar_is_displayed(self):
        stepper = self.browser.find_element_by_id(base.ELEMS["APP"]["STEPPER_BAR"]["ID"])
        self.assertTrue(stepper.is_displayed())

    def test_stepper_bar_has_correct_class(self):
        stepper = self.browser.find_element_by_id(base.ELEMS["APP"]["STEPPER_BAR"]["ID"])
        intended_class = base.ELEMS["APP"]["STEPPER_BAR"]["CLASS"]
        self.assertEqual(stepper.get_attribute("class"), intended_class)

    def test_stepper_bar_has_correct_number_of_steps(self):
        stepper = self.browser.find_element_by_id(base.ELEMS["APP"]["STEPPER_BAR"]["ID"])
        steps = stepper.find_elements_by_tag_name("li")
        self.assertEqual(len(steps), len(base.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]))
    
    def test_steps_have_correct_text(self):
        items = base.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]
        for item in items:
            step = self.browser.find_element_by_id(item["ID"])
            self.assertEqual(step.get_attribute("innerText"), item["TEXT"])
    
    def test_correct_steps_are_active(self):
        items = base.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]
        for item in items:
            step = self.browser.find_element_by_id(item["ID"])
            if items.index(item) <= 1:            
                self.assertIn("active", step.get_attribute("class"))
            else:
                self.assertNotIn("active", step.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    def test_intro_text_is_displayed(self):
        intro_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["INTRO"]["ID"]
        intro_txt = self.browser.find_element_by_id(intro_id)
        self.assertTrue(intro_txt.is_displayed())

    def test_region_setter_text_is_displayed(self):
        regions_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGION_SETTING"]["ID"]
        regions_txt = self.browser.find_element_by_id(regions_id)
        self.assertTrue(regions_txt.is_displayed())

    def test_regions_modal_is_not_displayed(self):
        regions_modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGIONS_MODAL"]["ID"]
        regions_modal = self.browser.find_element_by_id(regions_modal_id)        
        self.assertFalse(regions_modal.is_displayed())
    
    def test_object_recognition_modal_is_not_displayed(self):
        or_modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["OBJ_REC_MODAL"]["ID"]
        or_modal = self.browser.find_element_by_id(or_modal_id)
        self.assertFalse(or_modal.is_displayed())
    
    def test_region_editor_modal_is_not_displayed(self):
        re_modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REG_EDIT_MODAL"]["ID"]
        re_modal = self.browser.find_element_by_id(re_modal_id)
        self.assertFalse(re_modal.is_displayed())

    # -------------------------------------------------------------------------------------
    # Find-regions button tests
    # -------------------------------------------------------------------------------------    
    def test_find_regions_button_is_displayed(self):
        find_rgns_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["FIND_REGIONS_BTN"]["ID"])
        self.assertTrue(find_rgns_btn.is_displayed())

    def test_add_region_button_is_enabled(self):
        find_rgns_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["FIND_REGIONS_BTN"]["ID"])
        self.assertTrue(find_rgns_btn.is_enabled())

    def test_add_region_button_has_correct_text(self):
        find_rgns_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["FIND_REGIONS_BTN"]["ID"])
        intended_text = base.ELEMS["SET_REGIONS"]["FIND_REGIONS_BTN"]["TEXT"]
        self.assertEqual(find_rgns_btn.get_attribute("innerText"), intended_text)

    # -------------------------------------------------------------------------------------
    # Add-region button tests
    # -------------------------------------------------------------------------------------    
    def test_add_region_button_is_displayed(self):
        add_rgn_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"])
        self.assertTrue(add_rgn_btn.is_displayed())

    def test_add_region_button_is_enabled(self):
        add_rgn_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"])
        self.assertTrue(add_rgn_btn.is_enabled())

    def test_add_region_button_has_correct_text(self):
        add_rgn_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"])
        intended_text = base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["TEXT"]
        self.assertEqual(add_rgn_btn.get_attribute("innerText"), intended_text)
    
    # def test_choose_image_label_has_correct_label_text(self):
    #     """
    #     Test whether the home page has a button for uploading images to the service,
    #     and whether the button contains the correct text.

    #     The label element has no ID of its own, so use XPath to find / select it.
    #     """
    #     cfg = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]
    #     input_id = cfg["ID"]
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')
    #     self.assertEqual(img_label.get_attribute("innerText"), cfg["TEXT"])

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_next_button_is_displayed(self):        
        next_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"])
        self.assertTrue(next_btn.is_displayed())

    def test_next_button_is_enabled(self):        
        next_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"])
        self.assertFalse(next_btn.get_attribute("aria-disabled"))
        self.assertNotIn("disabled", next_btn.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    def test_previous_button_is_displayed(self):        
        prev_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"])
        self.assertTrue(prev_btn.is_displayed())

    def test_previous_button_is_enabled(self):        
        prev_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"])
        self.assertFalse(prev_btn.get_attribute("aria-disabled"))
        self.assertNotIn("disabled", prev_btn.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Preview pane tests
    # -------------------------------------------------------------------------------------
    def test_image_pane_exists(self):
        img_pane = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertTrue(img_pane)

    def test_image_pane_contains_correct_image(self):
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src = img.get_attribute("src")

        # get the sam UTF-8 string from the original image.        
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', base.IMG_FILE)
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # compare the two strings
        self.assertEqual(src, f"data:image/jpeg;base64,{b64_msg}")


# =========================================================================================
# DYNAMIC TESTS
# =========================================================================================
class SetRegionsPageDynamicTests(base.DynamicTests):
    """
    Tests to check whether the interactive elements of the page work as expected; e.g. button-
    clicks, selections etc.

    These tests require isolation from each other, so a browser instance is created at the 
    start of each test and destroyed at the end.
    """
    def setUp(self):
        """
        setUp() in base.py navigates to the home page. We then need to select an image
        and click the Next button.
        """
        # call the 'normal' setUp from the base class
        super().setUp()

        base.navigate_to_set_regions_page(self.browser)
    

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
    # Stepper bar tests
    # -------------------------------------------------------------------------------------
    def test_returning_to_home_sets_only_step_one_active(self):
        # browse back to the home page
        self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()

        # check classes of all stepper bar items
        items = base.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]
        for item in items:
            step = self.browser.find_element_by_id(item["ID"])
            if items.index(item) <= 0:            
                self.assertIn("active", step.get_attribute("class"))
            else:
                self.assertNotIn("active", step.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    def test_intro_modal_opens_and_closes_correctly(self):
        # click the <a> tag to open the modal
        modal_link_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["INTRO"]["MODAL_ID"]
        self.browser.find_element_by_id(modal_link_id).click()

        # add a brief wait
        time.sleep(2)

        # check to see if the modal has appeared
        modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGIONS_MODAL"]["ID"]
        modal = self.browser.find_element_by_id(modal_id)
        self.assertTrue(modal.is_displayed())

        # close the modal
        modal_close_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGIONS_MODAL"]["CLOSE_ID"]
        self.browser.find_element_by_id(modal_close_id).click()

        # add a wait to ensure the modal has closed
        time.sleep(2)

        # check that the modal is no longer displayed
        self.assertFalse(modal.is_displayed())

    def test_obj_recog_modal_opens_and_closes_correctly(self):
        ex_txt = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]

        # click the <a> tag to open the modal
        self.browser.find_element_by_id(ex_txt["REGION_SETTING"]["OR_MODAL_ID"]).click()

        # add a brief wait to ensure the modal has opened
        time.sleep(2)

        # check to see if the modal has appeared
        modal = self.browser.find_element_by_id(ex_txt["OBJ_REC_MODAL"]["ID"])
        self.assertTrue(modal.is_displayed())

        # close the modal
        self.browser.find_element_by_id(ex_txt["OBJ_REC_MODAL"]["CLOSE_ID"]).click()

        # add a wait to ensure the modal has closed
        time.sleep(2)

        # check that the modal is no longer displayed
        self.assertFalse(modal.is_displayed())

    def test_reg_editor_modal_opens_and_closes_correctly(self):
        # click the <a> tag to open the modal
        modal_link_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGION_SETTING"]["RE_MODAL_ID"]
        self.browser.find_element_by_id(modal_link_id).click()

        # add a brief wait
        time.sleep(2)

        # check to see if the modal has appeared
        modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REG_EDIT_MODAL"]["ID"]
        modal = self.browser.find_element_by_id(modal_id)
        self.assertTrue(modal.is_displayed())

        # close the modal
        modal_close_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REG_EDIT_MODAL"]["CLOSE_ID"]
        self.browser.find_element_by_id(modal_close_id).click()

        # add a wait to ensure the modal has closed
        time.sleep(2)

        # check that the modal is no longer displayed
        self.assertFalse(modal.is_displayed())

    # -------------------------------------------------------------------------------------
    # Add-region button tests
    # -------------------------------------------------------------------------------------    
    # def test_add_region_button_creates_console_msg(self):
    #     add_rgn_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"])
    #     self.assertTrue(add_rgn_btn.is_displayed())

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_clicking_next_button_takes_user_to_analyse_text_page(self):
        base_url = self.live_server_url        
        self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"]).click()
        expected_url = reverse(base.ELEMS["SET_REGIONS"]["NEXT_BTN"]["URL"])
        self.assertEqual(self.browser.current_url, base_url + expected_url)

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    def test_clicking_previous_button_takes_user_to_choose_image_page(self):
        base_url = self.live_server_url   
        self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()
        expected_url = reverse(base.ELEMS["SET_REGIONS"]["PREVIOUS_BTN"]["URL"])
        self.assertEqual(self.browser.current_url, base_url + expected_url)
    
    def test_image_is_displayed_when_user_clicks_back_button(self):
        # browse back to the home page
        self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()
        
        # short wait to ensure the page is rendered
        time.sleep(2)

        # get the src data for the image as a UTF-8 string decoded from base64
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src_string = img.get_attribute("src")

        # get the sam UTF-8 string from the original image.        
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', base.IMG_FILE)
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # compare the two strings
        self.assertEqual(src_string, f"data:image/jpeg;base64,{b64_msg}")