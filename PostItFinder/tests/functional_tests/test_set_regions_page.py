from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.color import Color

from django.conf import settings
from django.urls import reverse

import time
import os
from json import load
import base64
import math

from PostItFinder.tests.functional_tests import base

# =========================================================================================
# STATIC TESTS
# =========================================================================================
class StaticTests(base.StaticTests):
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
        self.assertEqual(base.ELEMS["SET_REGIONS"]["TITLE"], self.browser.title)
    
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
    
    def test_object_detection_modal_is_not_displayed(self):
        od_modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["OBJ_DET_MODAL"]["ID"]
        od_modal = self.browser.find_element_by_id(od_modal_id)
        self.assertFalse(od_modal.is_displayed())
    
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
        # path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', base.IMG_FILE)
        path = base.get_image_file_path(base.IMG_FILE)
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # compare the two strings
        self.assertEqual(src, f"data:image/jpeg;base64,{b64_msg}")


# =========================================================================================
# DYNAMIC TESTS
# =========================================================================================
class DynamicTests(base.DynamicTests):
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
    def test_returning_to_choose_image_sets_only_step_one_active(self):
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

        # wait until the modal is visible
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.ID, 
                base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGIONS_MODAL"]["ID"]))
        )

        # check to see if the modal has appeared
        modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGIONS_MODAL"]["ID"]
        modal = self.browser.find_element_by_id(modal_id)
        self.assertTrue(modal.is_displayed())

        # close the modal
        modal_close_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGIONS_MODAL"]["CLOSE_ID"]
        self.browser.find_element_by_id(modal_close_id).click()

        # wait until the modal has closed
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.invisibility_of_element_located((By.ID, 
                base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGIONS_MODAL"]["ID"]))
        )

        # check that the modal is no longer displayed
        self.assertFalse(modal.is_displayed())

    def test_obj_detection_modal_opens_and_closes_correctly(self):
        ex_txt = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]

        # click the <a> tag to open the modal
        self.browser.find_element_by_id(ex_txt["REGION_SETTING"]["OD_MODAL_ID"]).click()

        # wait until the modal is visible
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.ID, ex_txt["OBJ_DET_MODAL"]["ID"]))
        )

        # check to see if the modal has appeared
        modal = self.browser.find_element_by_id(ex_txt["OBJ_DET_MODAL"]["ID"])
        self.assertTrue(modal.is_displayed())

        # close the modal
        self.browser.find_element_by_id(ex_txt["OBJ_DET_MODAL"]["CLOSE_ID"]).click()

        # add a wait to ensure the modal has closed
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.invisibility_of_element_located((By.ID, ex_txt["OBJ_DET_MODAL"]["ID"]))
        )

        # check that the modal is no longer displayed
        self.assertFalse(modal.is_displayed())

    def test_region_editor_modal_opens_and_closes_correctly(self):
        # click the <a> tag to open the modal
        modal_link_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REGION_SETTING"]["RE_MODAL_ID"]
        self.browser.find_element_by_id(modal_link_id).click()

        modal_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REG_EDIT_MODAL"]["ID"]
        # wait until the modal has appeared
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.ID, modal_id))
        )

        # check to see if the modal has appeared
        modal = self.browser.find_element_by_id(modal_id)
        self.assertTrue(modal.is_displayed())

        # close the modal
        modal_close_id = base.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["REG_EDIT_MODAL"]["CLOSE_ID"]
        self.browser.find_element_by_id(modal_close_id).click()

        # add a wait to ensure the modal has closed
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.invisibility_of_element_located((By.ID, modal_id))
        )

        # check that the modal is no longer displayed
        self.assertFalse(modal.is_displayed())

    # -------------------------------------------------------------------------------------
    # Find-regions button tests
    # -------------------------------------------------------------------------------------
    def test_find_regions_button_gets_correct_region(self):
        # click the Find Regions button
        find_rgns_id = base.ELEMS["SET_REGIONS"]["FIND_REGIONS_BTN"]["ID"]
        self.browser.find_element_by_id(find_rgns_id).click()

        # add a long sleep, to account for the time taken for Azure to respond
        # wait for the results to be returned
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["REGION"]))
        )

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
        
        # Check that the values are correct
        self.assertAlmostEqual(float(rect.get_attribute("x")), 0.290309846 * img.size["width"])
        self.assertAlmostEqual(float(rect.get_attribute("y")), 0.310755759 * img.size["height"])
        self.assertAlmostEqual(float(rect.get_attribute("width")), 0.408914924 * img.size["width"])
        self.assertAlmostEqual(float(rect.get_attribute("height")), 0.355182737 * img.size["height"])

    def test_find_regions_button_alerts_user_on_timeout(self):
        # NOTE: how to do this?! 
        # Detting a sleep won't work; it won't actually make the AJAX request sleep, it just 
        # makes the browser wait while the AJAX request completes happily in the background.
        # More Googling required!
        pass


    # -------------------------------------------------------------------------------------
    # Add-region button tests
    # -------------------------------------------------------------------------------------
    def test_add_region_button_creates_new_region(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # we expect 1 x rect element and 2 x circle elements to be created
        rects = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        self.assertEqual(len(rects), 1)

        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")
        self.assertEqual(len(circles), 2)
    
    def test_new_region_appears_in_top_left_corner(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # we expect 1 x rect element and 2 x circle elements to be created
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        tl_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["TOP_LEFT_HANDLE"])
        br_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BOTTOM_RIGHT_HANDLE"])
        
        # the rect coordinates will be (0,0), as will be the top-left handle. The bottom-right
        # handle coords will be rect_width + rect_height
        self.assertEqual(int(rect.get_attribute("x")), 0)
        self.assertEqual(int(rect.get_attribute("y")), 0)
        self.assertEqual(int(tl_handle.get_attribute("cx")), 0)
        self.assertEqual(int(tl_handle.get_attribute("cy")), 0)
        self.assertEqual(int(br_handle.get_attribute("cx")), base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"])
        self.assertEqual(int(br_handle.get_attribute("cy")), base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"])

    def test_regions_and_handles_have_correct_classes(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # we expect one element with class 'region' (the region group), and one with class
        # 'handle' (the region-resize handle *group*)
        regions = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["REGION"])
        self.assertEqual(len(regions), 1)

        handles = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["HANDLE"])
        self.assertEqual(len(handles), 1)

        # we expect one element with class 'top-left-handle' , and one with class
        # 'bottom-right-handle' 
        tl_handles = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["TOP_LEFT_HANDLE"])
        self.assertEqual(len(tl_handles), 1)

        br_handles = self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BOTTOM_RIGHT_HANDLE"])
        self.assertEqual(len(br_handles), 1)
    
    def test_limit_is_applied_to_number_of_new_regions(self):
        # The total number of regions plotted should be:
        # floor(image.width / region.width) * floor(image.height / region.height)
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        expected_num_regions = (math.floor(img.size["width"] / base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"]) * 
                                math.floor(img.size["height"] / base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"]))

        last_count = -1
        current_count = 0
        add_rgn_btn = self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"])
        while last_count != current_count:
            last_count = current_count
            # add a new region
            add_rgn_btn.click()
            
            # add a short wait to ensure the region is rendered
            time.sleep(0.5)

            # get the number of regions
            current_count = len(self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["REGION"]))
            
            # ensure we don't get an infinite loop (no need for an error msg, as the assert
            # will flag any issues)
            if current_count > expected_num_regions:
                break
        
        self.assertEqual(expected_num_regions, current_count)

    def test_region_sizes_are_correct(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the rect element
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        # check the width and height of the rect are correct
        self.assertEqual(int(rect.get_attribute("width")), base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"])
        self.assertEqual(int(rect.get_attribute("height")), base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"])

    def test_region_colours_are_correct(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the three SVG elements
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")

        # check the colours of the SVG elements       
        expected_fill_colour = base.CONST["COLOURS"]["REGION_COLOUR"]
        self.assertEqual(expected_fill_colour, 
                         Color.from_string(rect.value_of_css_property("fill")).hex.upper())        
        self.assertEqual(expected_fill_colour, 
                         Color.from_string(circles[0].value_of_css_property("fill")).hex.upper())
        self.assertEqual(expected_fill_colour, 
                         Color.from_string(circles[1].value_of_css_property("fill")).hex.upper())
        
        expected_stroke_colour = base.CONST["COLOURS"]["REGION_EDGE_COLOUR"]
        self.assertEqual(expected_stroke_colour, 
                         Color.from_string(rect.value_of_css_property("stroke")).hex.upper())        
        self.assertEqual(expected_stroke_colour, 
                         Color.from_string(circles[0].value_of_css_property("stroke")).hex.upper())
        self.assertEqual(expected_stroke_colour, 
                         Color.from_string(circles[1].value_of_css_property("stroke")).hex.upper())

    def test_regions_change_colour_on_mouseover(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the three SVG elements
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")

        # mouse-over the region
        ActionChains(self.browser).move_to_element(rect).perform()

        # check the colours of the SVG elements       
        expected_colour = base.CONST["COLOURS"]["REGION_HOVER_COLOUR"]
        self.assertEqual(expected_colour, 
                         Color.from_string(rect.value_of_css_property("fill")).hex.upper())        
        self.assertEqual(expected_colour, 
                         Color.from_string(circles[0].value_of_css_property("fill")).hex.upper())
        self.assertEqual(expected_colour, 
                         Color.from_string(circles[1].value_of_css_property("fill")).hex.upper())
        
    def test_regions_can_be_moved(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the three SVG elements
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")

        # NOTE: start positions of elements are: rect=[0,0]; tl-handle=[0,0]; br-handle=[rect-width, rect-height]

        # drag the region to a new position (old pos + [x_offset, y_offset])
        x_offset = 20
        y_offset = 30
        ActionChains(self.browser).drag_and_drop_by_offset(rect, x_offset, y_offset).perform()

        # get the positions of the elements after the drag
        rect_end_position = [rect.get_attribute("x"), rect.get_attribute("y")]
        circle1_end_position = [circles[0].get_attribute("cx"), circles[0].get_attribute("cy")]
        circle2_end_position = [circles[1].get_attribute("cx"), circles[1].get_attribute("cy")]

        # check that start_pos + offset = end_pos for all elements (both x and y coords)
        self.assertEqual(x_offset, int(rect_end_position[0]))
        self.assertEqual(y_offset, int(rect_end_position[1]))
        self.assertEqual(x_offset, int(circle1_end_position[0]))
        self.assertEqual(y_offset, int(circle1_end_position[1]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"] + x_offset, int(circle2_end_position[0]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"] + y_offset, int(circle2_end_position[1]))
    
    def test_regions_cannot_be_moved_outside_left_image_bound(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the three SVG elements
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")

        # NOTE: start positions of elements are: rect=[0,0]; tl-handle=[0,0]; br-handle=[rect-width, rect-height]

        # attempt to drag the region to a new position (old pos + [x_offset, y_offset])
        x_offset = -20
        y_offset = 0
        ActionChains(self.browser).drag_and_drop_by_offset(rect, x_offset, y_offset).perform()

        # get the positions of the elements after the drag
        rect_end_position = [rect.get_attribute("x"), rect.get_attribute("y")]
        circle1_end_position = [circles[0].get_attribute("cx"), circles[0].get_attribute("cy")]
        circle2_end_position = [circles[1].get_attribute("cx"), circles[1].get_attribute("cy")]

        # check that the region hasn't moved
        self.assertEqual(0, int(rect_end_position[0]))
        self.assertEqual(0, int(rect_end_position[1]))
        self.assertEqual(0, int(circle1_end_position[0]))
        self.assertEqual(0, int(circle1_end_position[1]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"], int(circle2_end_position[0]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"], int(circle2_end_position[1]))

    def test_regions_cannot_be_moved_outside_top_image_bound(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the three SVG elements
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")

        # NOTE: start positions of elements are: rect=[0,0]; tl-handle=[0,0]; br-handle=[rect-width, rect-height]

        # attempt to drag the region out of bounds upwards 
        x_offset = 0
        y_offset = -20
        ActionChains(self.browser).drag_and_drop_by_offset(rect, x_offset, y_offset).perform()

        # get the positions of the elements after the drag
        rect_end_position = [rect.get_attribute("x"), rect.get_attribute("y")]
        circle1_end_position = [circles[0].get_attribute("cx"), circles[0].get_attribute("cy")]
        circle2_end_position = [circles[1].get_attribute("cx"), circles[1].get_attribute("cy")]

        # check that the region hasn't moved
        self.assertEqual(0, int(rect_end_position[0]))
        self.assertEqual(0, int(rect_end_position[1]))
        self.assertEqual(0, int(circle1_end_position[0]))
        self.assertEqual(0, int(circle1_end_position[1]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"], int(circle2_end_position[0]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"], int(circle2_end_position[1]))

    def test_regions_cannot_be_moved_outside_right_image_bound(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the three SVG elements
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")

        # NOTE: start positions of elements are: rect=[0,0]; tl-handle=[0,0]; br-handle=[rect-width, rect-height]

        # attempt to drag the region out of bounds to the right
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        x_offset = img.size["width"] + 10   # offset is <width_of_image + anything>
        y_offset = 0
        ActionChains(self.browser).drag_and_drop_by_offset(rect, x_offset, y_offset).perform()

        # get the positions of the elements after the drag
        rect_end_position = [rect.get_attribute("x"), rect.get_attribute("y")]
        circle1_end_position = [circles[0].get_attribute("cx"), circles[0].get_attribute("cy")]
        circle2_end_position = [circles[1].get_attribute("cx"), circles[1].get_attribute("cy")]

        # the region should finish in the top-right corner of the image
        # *****
        # NOTE: for this test and the one below, math.ceil() is used because the image size may
        # be a floating point number, but the value returned by clientWidth and clientHeight
        # will ALWAYS be rounded up to an int. I'm comfortable with this.
        # *****
        self.assertEqual(math.ceil(img.size["width"] - base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"]),
                        int(rect_end_position[0]))
        self.assertEqual(0, int(rect_end_position[1]))
        self.assertEqual(math.ceil(img.size["width"] - base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"]), 
                        int(circle1_end_position[0]))
        self.assertEqual(0, int(circle1_end_position[1]))
        self.assertEqual(math.ceil(img.size["width"]), int(circle2_end_position[0]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"], int(circle2_end_position[1]))

    def test_regions_cannot_be_moved_outside_bottom_image_bound(self):
        # scroll to the bottom of the window (otherwise Selenium throws an off-page exception)
        self.browser.find_element_by_tag_name('body').send_keys(Keys.END)
        # brief wait to ensure the scroll has registered
        time.sleep(1)

        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()

        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the three SVG elements
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        circles = self.browser.find_elements_by_xpath("//*[local-name()='circle']")

        # NOTE: start positions of elements are: rect=[0,0]; tl-handle=[0,0]; br-handle=[rect-width, rect-height]

        # attempt to drag the region out of bounds to the bottom
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        x_offset = 0
        y_offset = img.size["height"] + 10   # offset is <height_of_image + anything>         
        ActionChains(self.browser).drag_and_drop_by_offset(rect, x_offset, y_offset).perform()

        # get the positions of the elements after the drag
        rect_end_position = [rect.get_attribute("x"), rect.get_attribute("y")]
        circle1_end_position = [circles[0].get_attribute("cx"), circles[0].get_attribute("cy")]
        circle2_end_position = [circles[1].get_attribute("cx"), circles[1].get_attribute("cy")]

        # the region should finish in the bottom-left corner of the image
        self.assertEqual(0, int(rect_end_position[0]))
        self.assertEqual(math.ceil(img.size["height"] - base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"]),
                        int(rect_end_position[1]))
        self.assertEqual(0, int(circle1_end_position[0]))
        self.assertEqual(math.ceil(img.size["height"] - base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"]), 
                        int(circle1_end_position[1]))
        self.assertEqual(base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"], int(circle2_end_position[0]))
        self.assertEqual(math.ceil(img.size["height"]), int(circle2_end_position[1]))

    def test_regions_can_be_resized_using_tl_handle(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )

        # get the rect element and the top-left handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        tl_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["TOP_LEFT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js

        # move the rect away from the TL corner, then change the size by clicking and dragging
        x_offset = 20
        y_offset = 20
        (ActionChains(self.browser).drag_and_drop_by_offset(rect, x_offset, y_offset)
                                   .drag_and_drop_by_offset(tl_handle, x_offset, y_offset)
                                   .perform())

        # check that the new width and height of the rect element are correct
        # NOTE: we subtract the offsets here because we're dragging the TL corner down and 
        # right by using positive offsets, i.e. making the rect smaller
        self.assertEqual(int(rect.get_attribute("width")), 
                        base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"] - x_offset)
        self.assertEqual(int(rect.get_attribute("height")),
                        base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"] - y_offset)

    def test_regions_can_be_resized_using_br_handle(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element and the bottom-right handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        br_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BOTTOM_RIGHT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js
         
        # change the size of the rect by clicking and dragging
        x_offset = 20
        y_offset = 20
        ActionChains(self.browser).drag_and_drop_by_offset(br_handle, x_offset, y_offset).perform()

        # check that the new width and height of the rect element are correct
        self.assertEqual(int(rect.get_attribute("width")), 
                        base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"] + x_offset)
        self.assertEqual(int(rect.get_attribute("height")),
                        base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"] + y_offset)

    def test_regions_cannot_be_resized_below_min_using_tl_handle(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element and the top-left handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        tl_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["TOP_LEFT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js

        # change the size of the rect by clicking and dragging the handle. Attempted offsets are
        # the width & height of the rect (so if the min isn't applied, the region will have size=0)
        x_offset = base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"]
        y_offset = base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"]
        ActionChains(self.browser).drag_and_drop_by_offset(tl_handle, x_offset, y_offset).perform()

        # check that the new width and height of the rect element are the min values
        self.assertEqual(int(rect.get_attribute("width")), base.CONST["VALUES"]["MIN_RECT_WIDTH"])
        self.assertEqual(int(rect.get_attribute("height")), base.CONST["VALUES"]["MIN_RECT_HEIGHT"])

    def test_regions_cannot_be_resized_below_min_using_br_handle(self):
         # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element and the top-left handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        br_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BOTTOM_RIGHT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js

        # change the size of the rect by clicking and dragging the handle. Attempted offsets are
        # the width & height of the rect (so if the min isn't applied, the region will have size=0).
        # Offsets are -ve because we want to move the BR-handle up and left, not down and right.
        x_offset = -base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"]
        y_offset = -base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"]
        ActionChains(self.browser).drag_and_drop_by_offset(br_handle, x_offset, y_offset).perform()

        # check that the new width and height of the rect element are the min values
        self.assertEqual(int(rect.get_attribute("width")), base.CONST["VALUES"]["MIN_RECT_WIDTH"])
        self.assertEqual(int(rect.get_attribute("height")), base.CONST["VALUES"]["MIN_RECT_HEIGHT"])


    def test_regions_cannot_be_resized_outside_top_image_bound(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element and the top-left handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        tl_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["TOP_LEFT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js

        # change the rect size by clicking and dragging the top-left handle
        # NOTE: -ve offset because we want to move the handle upwards
        x_offset = 0
        y_offset = -20
        ActionChains(self.browser).drag_and_drop_by_offset(tl_handle, x_offset, y_offset).perform()

        # check that the new width and height of the rect element haven't changed
        self.assertEqual(int(rect.get_attribute("width")), base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"])
        self.assertEqual(int(rect.get_attribute("height")), base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"])

    def test_regions_cannot_be_resized_outside_left_image_bound(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element and the top-left handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        tl_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["TOP_LEFT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js

        # change the rect size by clicking and dragging the top-left handle
        # NOTE: -ve offset because we want to move the handle upwards
        x_offset = -20
        y_offset = 0
        ActionChains(self.browser).drag_and_drop_by_offset(tl_handle, x_offset, y_offset).perform()

        # check that the new width and height of the rect element haven't changed
        self.assertEqual(int(rect.get_attribute("width")), base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"])
        self.assertEqual(int(rect.get_attribute("height")), base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"])

    def test_regions_cannot_be_resized_outside_bottom_image_bound(self):
        # scroll to the bottom of the window (otherwise Selenium throws an off-page exception)
        self.browser.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(1)

        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element and the top-left handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        br_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BOTTOM_RIGHT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js

        # change the rect size by clicking and dragging the bottom-right handle
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        x_offset = 0
        y_offset = img.size["height"]
        ActionChains(self.browser).drag_and_drop_by_offset(br_handle, x_offset, y_offset).perform()

        # check that the width of the rect hasn't changed, and that the height is now the height 
        # of the image
        # ***** 
        # NOTE: as with the move-region-down and move-region-right tests, using math.ceil here
        # to avoid errors between an int region-size and a potentially float image-size
        # *****
        self.assertEqual(int(rect.get_attribute("width")), base.CONST["VALUES"]["DEFAULT_RECT_WIDTH"])
        self.assertEqual(int(rect.get_attribute("height")), math.ceil(img.size["height"]))

    def test_regions_cannot_be_resized_outside_right_image_bound(self):
        # add a new region
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element and the top-left handle
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        br_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BOTTOM_RIGHT_HANDLE"])

        # NOTE: the initial size of the rect is known (and tested) to be the default width, height from config.js

        # change the rect size by clicking and dragging the bottom-right handle
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        x_offset = img.size["width"]
        y_offset = 0
        ActionChains(self.browser).drag_and_drop_by_offset(br_handle, x_offset, y_offset).perform()

        # check that the width of the rect hasn't changed, and that the height is now the height 
        # of the image
        self.assertEqual(int(rect.get_attribute("width")), math.ceil(img.size["width"]))
        self.assertEqual(int(rect.get_attribute("height")), base.CONST["VALUES"]["DEFAULT_RECT_HEIGHT"])

    def test_regions_can_be_deleted(self):
        # add a new region 
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        
        # get the rect element
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        # double-click the rect to delete the region
        ActionChains(self.browser).double_click(rect).perform()

        # confirm that there aren't any of either element in the DOM
        # (If there are no elements then find_elements_by_xpath() will return [], which is False])
        self.assertFalse(self.browser.find_elements_by_class_name(base.CONST["CLASSES"]["BODY_RECT"]))
        self.assertFalse(self.browser.find_elements_by_xpath("//*[local-name()='circles']"))
    
    def test_browser_window_resize_changes_region_size_correctly(self):
        # maximise the browser window
        self.browser.maximize_window()
        
        # scroll to the bottom of the window (otherwise Selenium throws an off-page exception)
        self.browser.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(3)

        # create a new region and get rect, bottom-right handle elements
        self.browser.find_element_by_id(base.ELEMS["SET_REGIONS"]["ADD_REGION_BTN"]["ID"]).click()
        # wait for the region to be rendered
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])
        br_handle = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BOTTOM_RIGHT_HANDLE"])

        # move the region to pre-set coordinates, and resize the region to a pre-set size
        drag_br_x = 195 - float(rect.get_attribute("width"))
        drag_br_y = 175 - float(rect.get_attribute("height"))
        (ActionChains(self.browser).drag_and_drop_by_offset(rect, 241, 175)
                                  .drag_and_drop_by_offset(br_handle, drag_br_x, drag_br_y)
                                  .perform())

        # change the browser width, height to pre-set values and ensure the window is scrolled-down
        self.browser.set_window_size(1075, 786)
        self.browser.find_element_by_tag_name('body').send_keys(Keys.END)

        # the original rect is deleted on resize, so get the new one
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, base.CONST["CLASSES"]["BODY_RECT"]))
        )
        rect = self.browser.find_element_by_class_name(base.CONST["CLASSES"]["BODY_RECT"])

        # check that the region x, y, width, height match to pre-set values
        # use assertAlmostEqual to account for float rounding differences
        self.assertAlmostEqual(float(rect.get_attribute("x")), 201.3835616438356)
        self.assertAlmostEqual(float(rect.get_attribute("y")), 146.25912408759126)
        self.assertAlmostEqual(float(rect.get_attribute("width")), 162.94520547945206)
        self.assertAlmostEqual(float(rect.get_attribute("height")), 146.25912408759126)
        

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
        
        # wait for the page to render
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.title_is(base.ELEMS["CHOOSE_IMAGE"]["TITLE"])
        )
        
        # get the src data for the image as a UTF-8 string decoded from base64
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src_string = img.get_attribute("src")

        # get the same UTF-8 string from the original image.        
        # path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', base.IMG_FILE)
        path = base.get_image_file_path(base.IMG_FILE)
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # compare the two strings
        self.assertEqual(src_string, f"data:image/jpeg;base64,{b64_msg}")