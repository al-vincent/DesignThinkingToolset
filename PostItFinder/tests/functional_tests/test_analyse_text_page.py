from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color
from selenium.common.exceptions import NoSuchElementException

from django.conf import settings
from django.urls import reverse

import time
import os
from json import load
import base64
import math

from PostItFinder.tests.functional_tests import base

# =========================================================================================
# DYNAMIC TESTS
# =========================================================================================
class DynamicTests(base.DynamicTests):
    """
    Several session variables are set in previous steps, so to ensure test isolation,
    only dynamic tests are used (i.e. the browser is cleanly set-up and torn-down 
    at the end of each test).
    """

    def setUp(self):
        """
        setUp() in base.py navigates to the home page. We then need to select an image
        and click the Next button.
        """                
        # call the 'normal' setUp from the base class; navigate to analyse-text
        super().setUp()
        base.navigate_to_analyse_text_page(self.browser)

# -------------------------------------------------------------------------------------
# Page tests
# -------------------------------------------------------------------------------------
class TestPage(DynamicTests):
    def test_page_uses_app_template(self):
        """
        Check that the app uses the set-regions.html template.
        """
        response = self.client.get(reverse(base.ELEMS["ANALYSE_TEXT"]["URL"]))
        self.assertTemplateUsed(response, base.PATHS["ANALYSE_TEXT"])

    def test_page_has_correct_title(self):
        """
        Ensure that the page title includes the correct text.
        """
        self.assertEqual(base.ELEMS["ANALYSE_TEXT"]["TITLE"], self.browser.title)
    
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
class TestNavbar(DynamicTests):
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
    
    # def test_clicking_logo_takes_user_to_home(self):
    #     pass

    def test_clicking_about_takes_user_to_about_page(self):
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
class TestStepperBar(DynamicTests):
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
            if items.index(item) <= 2:          
                self.assertIn("active", step.get_attribute("class"))
            else:
                self.assertNotIn("active", step.get_attribute("class"))
        
    def test_returning_to_set_regions_sets_steps_one_and_two_active(self):
        # browse back to the home page
        self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()

        # check classes of all stepper bar items
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
class TestExplanatoryText(DynamicTests):
    def test_intro_text_is_displayed(self):
        intro_id = base.ELEMS["ANALYSE_TEXT"]["EXPLAIN_TEXT"]["INTRO"]["ID"]
        intro_txt = self.browser.find_element_by_id(intro_id)
        self.assertTrue(intro_txt.is_displayed())

    def test_ocr_modal_is_not_displayed(self):
        ocr_modal_id = base.ELEMS["ANALYSE_TEXT"]["EXPLAIN_TEXT"]["OCR_MODAL"]["ID"]
        ocr_modal = self.browser.find_element_by_id(ocr_modal_id)
        self.assertFalse(ocr_modal.is_displayed())

    def test_ocr_modal_opens_and_closes_correctly(self):
        # click the <a> tag to open the modal
        modal_link_id = base.ELEMS["ANALYSE_TEXT"]["EXPLAIN_TEXT"]["INTRO"]["MODAL_ID"]
        self.browser.find_element_by_id(modal_link_id).click()

        # wait for the modal to appear
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.ID, 
                base.ELEMS["ANALYSE_TEXT"]["EXPLAIN_TEXT"]["OCR_MODAL"]["ID"]))
        )

        # check to see if the modal has appeared
        modal_id = base.ELEMS["ANALYSE_TEXT"]["EXPLAIN_TEXT"]["OCR_MODAL"]["ID"]
        modal = self.browser.find_element_by_id(modal_id)
        self.assertTrue(modal.is_displayed())

        # close the modal
        modal_close_id = base.ELEMS["ANALYSE_TEXT"]["EXPLAIN_TEXT"]["OCR_MODAL"]["CLOSE_ID"]
        self.browser.find_element_by_id(modal_close_id).click()

        # wait for the modal to disappear
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.invisibility_of_element_located((By.ID, 
                base.ELEMS["ANALYSE_TEXT"]["EXPLAIN_TEXT"]["OCR_MODAL"]["ID"]))
        )

        # check that the modal is no longer displayed
        self.assertFalse(modal.is_displayed())


# -------------------------------------------------------------------------------------
# Analyse Text button tests
# -------------------------------------------------------------------------------------
class TestAnalyseTextButton(DynamicTests):
    def test_button_is_displayed(self):
        analyse_txt_btn = self.browser.find_element_by_id(base.ELEMS["ANALYSE_TEXT"]["ANALYSE_TEXT_BTN"]["ID"])
        self.assertTrue(analyse_txt_btn.is_displayed())

    def test_button_is_enabled(self):
        analyse_txt_btn = self.browser.find_element_by_id(base.ELEMS["ANALYSE_TEXT"]["ANALYSE_TEXT_BTN"]["ID"])
        self.assertTrue(analyse_txt_btn.is_enabled())

    def test_button_has_correct_text(self):
        analyse_txt_btn = self.browser.find_element_by_id(base.ELEMS["ANALYSE_TEXT"]["ANALYSE_TEXT_BTN"]["ID"])
        intended_text = base.ELEMS["ANALYSE_TEXT"]["ANALYSE_TEXT_BTN"]["TEXT"]
        self.assertEqual(analyse_txt_btn.get_attribute("innerText"), intended_text)

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    # def test_next_button_is_displayed(self):        
    #     next_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"])
    #     self.assertTrue(next_btn.is_displayed())

    # def test_next_button_is_enabled(self):        
    #     next_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"])
    #     self.assertFalse(next_btn.get_attribute("aria-disabled"))
    #     self.assertNotIn("disabled", next_btn.get_attribute("class"))
    
    # def test_clicking_next_button_takes_user_to_output_results_page(self):
    #     base_url = self.live_server_url        
    #     self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"]).click()
    #     expected_url = reverse(base.ELEMS["SET_REGIONS"]["NEXT_BTN"]["URL"])
    #     self.assertEqual(self.browser.current_url, base_url + expected_url)

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    # def test_previous_button_is_displayed(self):        
    #     prev_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"])
    #     self.assertTrue(prev_btn.is_displayed())

    # def test_previous_button_is_enabled(self):        
    #     prev_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"])
    #     self.assertFalse(prev_btn.get_attribute("aria-disabled"))
    #     self.assertNotIn("disabled", prev_btn.get_attribute("class"))

    # def test_clicking_previous_button_takes_user_to_set_regions_page(self):
    #     base_url = self.live_server_url   
    #     self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()
    #     expected_url = reverse(base.ELEMS["ANALYSE_TEXT"]["PREVIOUS_BTN"]["URL"])
    #     self.assertEqual(self.browser.current_url, base_url + expected_url)
    
    # def test_image_and_regions_are_displayed_when_user_clicks_back_button(self):
    #     # browse back to the home page
    #     self.browser.find_element_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()
        
    #     # short wait to ensure the page is rendered
    #     time.sleep(2)

    #     # get the src data for the image as a UTF-8 string decoded from base64
    #     img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
    #     src_string = img.get_attribute("src")

    #     # get the same UTF-8 string from the original image.        
    #     # path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', base.IMG_FILE)
    #     path = base.get_image_file_path(base.IMG_FILE)
    #     with open(path, "rb") as f:
    #         b64_encoded_img = base64.b64encode(f.read())
    #         b64_msg = b64_encoded_img.decode('utf-8')

    #     # compare the two strings
    #     self.assertEqual(src_string, f"data:image/jpeg;base64,{b64_msg}")

# -------------------------------------------------------------------------------------
# Image pane tests
# -------------------------------------------------------------------------------------
class TestImagePane(DynamicTests):
    def test_image_pane_exists(self):
        img_pane = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertTrue(img_pane)

    def test_image_pane_contains_correct_image(self):
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src = img.get_attribute("src")

        # get the sam UTF-8 string from the original image.                
        path = base.get_image_file_path(base.IMG_FILE)
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # compare the two strings
        self.assertEqual(src, f"data:image/jpeg;base64,{b64_msg}")
    
    def test_image_pane_renders_region_correctly(self):
        pass

# -------------------------------------------------------------------------------------
# Detailed tests on the results of the Analyse Text button, with a region included
# -------------------------------------------------------------------------------------
class TestAnalyseTextButtonWithRegion(base.DynamicTests):
    def setUp(self):
        """
        setUp() in base.py navigates to the home page. We then need to select an image;
        navigate to set-regions; create a region; resize it; and nav to analyse-text
        """                
        # call the 'normal' setUp from the base class; navigate to set-regions
        super().setUp()
        base.navigate_to_set_regions_page(self.browser)
        # click the Find Regions button
        find_rgns_id = base.ELEMS["SET_REGIONS"]["FIND_REGIONS_BTN"]["ID"]
        self.browser.find_element_by_id(find_rgns_id).click()
        # wait for the region to be rendered and get the rect
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        # click the Next button to get to analyse-text
        self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"]).click()

        # click the Analyse Text button
        analyse_txt_id = base.ELEMS["ANALYSE_TEXT"]["ANALYSE_TEXT_BTN"]["ID"]
        self.browser.find_element_by_id(analyse_txt_id).click()

        # wait for the results to be returned and regions to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["REGION"]))
        )

    def test_mouseover_shows_expected_text(self):
        # get the rect element
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        # Hover on region, and wait for tooltip to appear
        ActionChains(self.browser).move_to_element(rect).perform()
        tooltip = WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["TOOLTIP"]))
        )
        self.assertEqual(tooltip.text, "WORDS HERE")
        
    def test_mouseover_and_mouseout_correctly_change_region_colour(self):
        # get the rect element
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        # Hover on region, and wait for tooltip to appear
        ActionChains(self.browser).move_to_element(rect).perform()
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["TOOLTIP"]))
        )
        # check that the rect has changed colour on hover
        self.assertEqual(base.CONST["COLOURS"]["REGION_HOVER_COLOUR"], 
                         Color.from_string(rect.value_of_css_property("fill")).hex.upper())
        # move the mouse outside the rect, and check the rect colour has changed back
        ActionChains(self.browser).move_to_element_with_offset(rect, -10, -10).perform()
        self.assertEqual(base.CONST["COLOURS"]["REGION_COLOUR"], 
                         Color.from_string(rect.value_of_css_property("fill")).hex.upper())

    def test_region_rendered_is_in_correct_location(self):
        # if successful, a single region should be created at specific points
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        self.assertEqual(len(rects), 1)  
        # get the rect and ensure that it's x, y, width, height are correct
        rect = rects[0]
        
        # The azure return, when run standalone, return the below (relative coords, range [0,1]):
        # {'x': 0.290309846, 'y': 0.310755759, 'width': 0.408914924, 'height': 0.355182737}. Need 
        # to convert these to absolute coords using the width & height of the image.

        # We don't know the image width and height in the browser, so get the image element
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        
        # Check that the region location is correct
        self.assertAlmostEqual(float(rect.get_attribute("x")), 0.290309846 * img.size["width"])
        self.assertAlmostEqual(float(rect.get_attribute("y")), 0.310755759 * img.size["height"])
        self.assertAlmostEqual(float(rect.get_attribute("width")), 0.408914924 * img.size["width"])
        self.assertAlmostEqual(float(rect.get_attribute("height")), 0.355182737 * img.size["height"])

        
    def test_region_has_no_handles(self):
        # Best way to test is to look for handles and not find any...?!
        # NOTE: find_elements_by_class_name() doesn't raise NoSuchElementException;
        # if it doesn't find any elements, it returns an empty list.
        handles = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["HANDLE"])
        if len(handles) != 0:
            self.fail("Handles should not be rendered")
        else:
            # pass the test
            pass

    def test_region_cannot_be_moved(self):
        # get the rect element
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        # get it's original coords
        x = rect.get_attribute("x")
        y = rect.get_attribute("y")

        # try to move the rect
        ActionChains(self.browser).drag_and_drop_by_offset(rect, 20, 20).perform()

        # get the 'new' coords
        new_x = rect.get_attribute("x")
        new_y = rect.get_attribute("y")

        # check they're the same as the originals
        self.assertEqual(x, new_x)
        self.assertEqual(y, new_y)


    def test_region_cannot_be_resized(self):
        # NOTE: have established that no handles exist, so I think this is ok...?
        pass
            
    def test_region_cannot_be_deleted(self):
        # count the rect elements
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        num_rects_start = len(rects)
        rect = rects[0]

        # double-click on it
        ActionChains(self.browser).double_click(rect).perform()

        # count the number of rects again
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        num_rects_end = len(rects)

        # confirm that the number of rects hasn't changed
        self.assertEqual(num_rects_start, num_rects_end)

# -------------------------------------------------------------------------------------
# Detailed tests on the results of the Analyse Text button, with no regions
# -------------------------------------------------------------------------------------
class TestAnalyseTextButtonWithNoRegions(base.DynamicTests):
    def setUp(self):
        """
        setUp() in base.py navigates to the home page. We then need to select an image;
        navigate to set-regions; create a region; resize it; and nav to analyse-text
        """                
        # call the 'normal' setUp from the base class; navigate to set-regions
        super().setUp()
        base.navigate_to_set_regions_page(self.browser)
        
        # click the Next button to get to analyse-text
        self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"]).click()

        # click the Analyse Text button
        analyse_txt_id = base.ELEMS["ANALYSE_TEXT"]["ANALYSE_TEXT_BTN"]["ID"]
        self.browser.find_element_by_id(analyse_txt_id).click()

        # wait for the results to be returned and regions to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["REGION"]))
        )

    def test_two_regions_are_rendered(self):
        # if successful, two regions should be created
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        self.assertEqual(len(rects), 2)  

    def test_mouseover_shows_expected_text(self):
        # get the rect elements
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        # for each region, check that mousing-over displays the correct text
        for rect in rects:
            # Hover on region, and wait for tooltip to appear
            ActionChains(self.browser).move_to_element(rect).perform()
            tooltip = WebDriverWait(self.browser, base.MAX_WAIT).until(
                EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["TOOLTIP"]))
            )
            # I don't believe there's any way to predict which rect will be moused-over first
            # so assert that the tooltip-text is *one* of the expected words.
            self.assertIn(tooltip.text, ["WORDS", "HERE"])
        
    def test_mouseover_and_mouseout_correctly_change_region_colour(self):
        # get the rect elements
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        for rect in rects:
            # Hover on region, and wait for tooltip to appear
            ActionChains(self.browser).move_to_element(rect).perform()
            WebDriverWait(self.browser, base.MAX_WAIT).until(
                EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["TOOLTIP"]))
            )
            # check that the rect has changed colour on hover
            self.assertEqual(base.CONST["COLOURS"]["REGION_HOVER_COLOUR"], 
                            Color.from_string(rect.value_of_css_property("fill")).hex.upper())
            # move the mouse outside the rect, and check the rect colour has changed back
            ActionChains(self.browser).move_to_element_with_offset(rect, -10, -10).perform()
            self.assertEqual(base.CONST["COLOURS"]["REGION_COLOUR"], 
                            Color.from_string(rect.value_of_css_property("fill")).hex.upper())
        
    def test_regions_have_no_handles(self):
        # Best way to test is to look for handles and not find any...?!
        # NOTE: find_elements_by_class_name() doesn't raise NoSuchElementException;
        # if it doesn't find any elements, it returns an empty list.
        handles = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["HANDLE"])
        if len(handles) != 0:
            self.fail("Handles should not be rendered")
        else:
            # pass the test
            pass

    def test_regions_cannot_be_moved(self):
        # get the rect elements
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        for rect in rects:
            # get it's original coords
            x = rect.get_attribute("x")
            y = rect.get_attribute("y")

            # try to move the rect
            ActionChains(self.browser).drag_and_drop_by_offset(rect, 5, 5).perform()

            # get the 'new' coords
            new_x = rect.get_attribute("x")
            new_y = rect.get_attribute("y")

            # check they're the same as the originals
            self.assertEqual(x, new_x)
            self.assertEqual(y, new_y)

    def test_region_cannot_be_resized(self):
        # NOTE: have established that no handles exist, so I think this is ok...?
        pass
            
    def test_region_cannot_be_deleted(self):
        # count the rect elements
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        num_rects_start = len(rects)

        # get one of the rects
        rect = rects[0]

        # double-click on it
        ActionChains(self.browser).double_click(rect).perform()

        # count the number of rects again
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        num_rects_end = len(rects)

        # confirm that the number of rects hasn't changed
        self.assertEqual(num_rects_start, num_rects_end)