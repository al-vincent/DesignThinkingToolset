from selenium.webdriver.support.ui import Select
from django.conf import settings
from django.urls import reverse

import time
import os
from json import load
import base64

# from functional_tests import base
from project_tests.functional_tests import base

# arbitrarily use test_png.png as our setup image throughout
IMG_FILE = "test_jpg.jpg"

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

        # arbitrarily use test_png.png as our test image
        input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input elements and update with the file path
        input_elem = self.browser.find_element_by_id(input_id)
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', IMG_FILE)
        input_elem.send_keys(path)

        # wait a few seconds for the image to render
        time.sleep(2)

        # click the Next button
        nxt_btn = self.browser.find_element_by_id(self.ELEMS["APP"]["NEXT_BTN"]["ID"])
        nxt_btn.click()

        # wait for the new page to render
        time.sleep(2)

    # -------------------------------------------------------------------------------------
    # Page tests
    # -------------------------------------------------------------------------------------
    def test_page_uses_app_template(self):
        """
        Check that the app uses the set-regions.html template.
        """
        response = self.client.get(reverse(self.ELEMS["SET_REGIONS"]["URL"]))
        self.assertTemplateUsed(response, self.PATHS["SET_REGIONS"])

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

    def test_navbar_items_are_displayed(self):
        for nav_item in self.ELEMS["BASE"]["NAVBAR"]["PAGES"]:
            link = self.browser.find_element_by_id(nav_item["ID"])
            self.assertTrue(link.is_displayed())

    def test_navbar_items_show_correct_text(self):
        for nav_item in self.ELEMS["BASE"]["NAVBAR"]["PAGES"]:
            element = self.browser.find_element_by_id(nav_item["ID"])
            self.assertEqual(element.get_attribute("innerText"), nav_item["TEXT"])
    
    # -------------------------------------------------------------------------------------
    # Stepper bar tests
    # -------------------------------------------------------------------------------------
    def test_stepper_bar_is_displayed(self):
        stepper = self.browser.find_element_by_id(self.ELEMS["APP"]["STEPPER_BAR"]["ID"])
        self.assertTrue(stepper.is_displayed())

    def test_stepper_bar_has_correct_class(self):
        stepper = self.browser.find_element_by_id(self.ELEMS["APP"]["STEPPER_BAR"]["ID"])
        intended_class = self.ELEMS["APP"]["STEPPER_BAR"]["CLASS"]
        self.assertEqual(stepper.get_attribute("class"), intended_class)

    def test_stepper_bar_has_correct_number_of_steps(self):
        stepper = self.browser.find_element_by_id(self.ELEMS["APP"]["STEPPER_BAR"]["ID"])
        steps = stepper.find_elements_by_tag_name("li")
        self.assertEqual(len(steps), len(self.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]))
    
    def test_steps_have_correct_text(self):
        items = self.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]
        for item in items:
            step = self.browser.find_element_by_id(item["ID"])
            self.assertEqual(step.get_attribute("innerText"), item["TEXT"])
    
    def test_correct_steps_are_active(self):
        items = self.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]
        for item in items:
            step = self.browser.find_element_by_id(item["ID"])
            if items.index(item) <= 1:            
                self.assertIn("active", step.get_attribute("class"))
            else:
                self.assertNotIn("active", step.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    def test_explain_text_is_displayed(self):
        explain_txt = self.browser.find_element_by_id(self.ELEMS["APP"]["EXPLAIN_TEXT"]["ID"])
        self.assertTrue(explain_txt.is_displayed())

    def test_explain_text_is_correct(self):
        explain_txt = self.browser.find_element_by_id(self.ELEMS["APP"]["EXPLAIN_TEXT"]["ID"])
        intended_text = self.ELEMS["SET_REGIONS"]["EXPLAIN_TEXT"]["TEXT"]
        self.assertEqual(explain_txt.get_attribute("innerText"), intended_text)

    # -------------------------------------------------------------------------------------
    # Choose-image button tests
    # -------------------------------------------------------------------------------------    
    # def test_choose_image_input_is_active(self):
    #     img_input = self.browser.find_element_by_id(self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"])
    #     self.assertTrue(img_input.is_enabled())
    
    # def test_choose_image_label_has_correct_label_text(self):
    #     """
    #     Test whether the home page has a button for uploading images to the service,
    #     and whether the button contains the correct text.

    #     The label element has no ID of its own, so use XPath to find / select it.
    #     """
    #     cfg = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]
    #     input_id = cfg["ID"]
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')
    #     self.assertEqual(img_label.get_attribute("innerText"), cfg["TEXT"])

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_next_button_is_displayed(self):        
        next_btn = self.browser.find_element_by_id(self.ELEMS["APP"]["NEXT_BTN"]["ID"])
        self.assertTrue(next_btn.is_displayed())

    def test_next_button_is_enabled(self):        
        next_btn = self.browser.find_element_by_id(self.ELEMS["APP"]["NEXT_BTN"]["ID"])
        self.assertFalse(next_btn.get_attribute("aria-disabled"))
        self.assertNotIn("disabled", next_btn.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    def test_previous_button_is_displayed(self):        
        prev_btn = self.browser.find_element_by_id(self.ELEMS["APP"]["PREVIOUS_BTN"]["ID"])
        self.assertTrue(prev_btn.is_displayed())

    def test_previous_button_is_enabled(self):        
        prev_btn = self.browser.find_element_by_id(self.ELEMS["APP"]["PREVIOUS_BTN"]["ID"])
        self.assertFalse(prev_btn.get_attribute("aria-disabled"))
        self.assertNotIn("disabled", prev_btn.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Preview pane tests
    # -------------------------------------------------------------------------------------
    def test_image_pane_exists(self):
        img_pane = self.browser.find_elements_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
        self.assertTrue(img_pane)

    def test_image_pane_contains_correct_(self):
        img = self.browser.find_element_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
        src = img.get_attribute("src")

        # get the sam UTF-8 string from the original image.        
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', IMG_FILE)
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

        # arbitrarily use test_png.png as our test image
        input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input elements and update with the file path
        input_elem = self.browser.find_element_by_id(input_id)
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', IMG_FILE)
        input_elem.send_keys(path)

        # wait a few seconds for the image to render
        time.sleep(2)

        # click the Next button
        nxt_btn = self.browser.find_element_by_id(self.ELEMS["APP"]["NEXT_BTN"]["ID"])
        nxt_btn.click()

        # wait for the new page to render
        time.sleep(2)

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
        page = self.ELEMS["BASE"]["NAVBAR"]["PAGES"][0]        
        page_elem = self.browser.find_element_by_id(page["ID"]).click()
        self.assertEqual(self.browser.current_url, base_url + reverse(page["URL"]))

    def test_clicking_faq_takes_user_to_faq_page(self):
        base_url = self.live_server_url
        page = self.ELEMS["BASE"]["NAVBAR"]["PAGES"][1]        
        page_elem = self.browser.find_element_by_id(page["ID"]).click()
        self.assertEqual(self.browser.current_url, base_url + reverse(page["URL"]))

    # -------------------------------------------------------------------------------------
    # Stepper bar tests
    # -------------------------------------------------------------------------------------
    def test_returning_to_home_sets_only_step_one_active(self):
        # browse back to the home page
        self.browser.find_element_by_id(self.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()

        # check classes of all stepper bar items
        items = self.ELEMS["APP"]["STEPPER_BAR"]["ITEMS"]
        for item in items:
            step = self.browser.find_element_by_id(item["ID"])
            if items.index(item) <= 0:            
                self.assertIn("active", step.get_attribute("class"))
            else:
                self.assertNotIn("active", step.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    # None

    # -------------------------------------------------------------------------------------
    # Choose-image button tests and preview pane tests
    # -------------------------------------------------------------------------------------
    # N.B. we don't want to run the test below! The dialog opened is an OS dialog, which 
    # Selenium can't interact with (including closing the dialog)
    # def test_clicking_choose_image_opens_dialog(self):
    #     pass

    # def test_jpg_can_be_selected(self):
    #     img_file = "test_jpg.jpg"
    #     input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input and label elements
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
    #     # update the input directly with the file path
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
    #     input_elem.send_keys(path)
    #     self.assertEqual(img_label.get_attribute("innerText"), img_file)

    #     # wait a few seconds for the image to render
    #     time.sleep(3)

    #     # check whether the image src attribute is no longer '#'
    #     img = self.browser.find_element_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
    #     self.assertNotIn("#", img.get_attribute("src"))
    
    # def test_png_can_be_selected(self):
    #     img_file = "test_png.png"
    #     input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input and label elements
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
    #     # update the input directly with the file path
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
    #     input_elem.send_keys(path)
    #     self.assertEqual(img_label.get_attribute("innerText"), img_file)

    #     # wait a few seconds for the image to render
    #     time.sleep(3)

    #     # check whether the image src attribute is no longer '#'
    #     img = self.browser.find_element_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
    #     self.assertNotIn("#", img.get_attribute("src"))
    
    # def test_bmp_can_be_selected(self):
    #     img_file = "test_bmp.bmp"
    #     input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input and label elements
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
    #     # update the input directly with the file path
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
    #     input_elem.send_keys(path)
    #     self.assertEqual(img_label.get_attribute("innerText"), img_file)

    #     # wait a few seconds for the image to render
    #     time.sleep(3)

    #     # check whether the image src attribute is no longer '#'
    #     img = self.browser.find_element_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
    #     self.assertNotIn("#", img.get_attribute("src"))
    
    # def test_gif_can_be_selected(self):
    #     img_file = "test_gif.gif"
    #     input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input and label elements
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
    #     # update the input directly with the file path
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
    #     input_elem.send_keys(path)
    #     self.assertEqual(img_label.get_attribute("innerText"), img_file)

    #     # wait a few seconds for the image to render
    #     time.sleep(3)

    #     # check whether the image src attribute is no longer '#'
    #     img = self.browser.find_element_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
    #     self.assertNotIn("#", img.get_attribute("src"))

    # def test_tif_cannot_be_selected(self):
    #     img_file = "test_tif.tif"
    #     input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input and label elements
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
    #     # update the input directly with the file path
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
    #     input_elem.send_keys(path)
    #     self.assertEqual(img_label.get_attribute("innerText"), img_file)

    #     # wait a few seconds for the image to render
    #     time.sleep(3)

    #     # check whether the image src attribute is no longer '#'
    #     img = self.browser.find_element_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
    #     self.assertIn("#", img.get_attribute("src"))

    # def test_file_info_put_in_sessionStorage(self):
    #     img_file = "test_jpg.jpg"
    #     input_id = self.ELEMS["HOME"]["CHOOSE_IMG_BTN"]["ID"]

    #     # get the input and label elements
    #     input_elem = self.browser.find_element_by_id(input_id)
    #     img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
    #     # update the input directly with the file path
    #     path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
    #     input_elem.send_keys(path)

    #     # wait a few seconds for the image to render
    #     time.sleep(3)

    #     # check whether there is anything in sessionStorage
    #     key = self.ELEMS['HOME']['IMAGE_PANE']['FILE_STORE_KEY']
    #     script = f"return sessionStorage.getItem('{key}');"
    #     self.assertIsNotNone(self.browser.execute_script(script))

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_clicking_next_button_takes_user_to_analyse_text_page(self):
        base_url = self.live_server_url        
        self.browser.find_element_by_id(self.ELEMS["APP"]["NEXT_BTN"]["ID"]).click()
        expected_url = reverse(self.ELEMS["SET_REGIONS"]["NEXT_BTN"]["URL"])
        self.assertEqual(self.browser.current_url, base_url + expected_url)

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    def test_clicking_previous_button_takes_user_to_choose_image_page(self):
        base_url = self.live_server_url   
        self.browser.find_element_by_id(self.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()
        expected_url = reverse(self.ELEMS["SET_REGIONS"]["PREVIOUS_BTN"]["URL"])
        self.assertEqual(self.browser.current_url, base_url + expected_url)
    
    def test_image_is_displayed_when_user_clicks_back_button(self):
        # browse back to the home page
        self.browser.find_element_by_id(self.ELEMS["APP"]["PREVIOUS_BTN"]["ID"]).click()
        
        # short wait to ensure the page is rendered
        time.sleep(2)

        # get the src data for the image as a UTF-8 string decoded from base64
        img = self.browser.find_element_by_id(self.ELEMS["APP"]["IMAGE_PANE"]["ID"])
        src_string = img.get_attribute("src")

        # get the sam UTF-8 string from the original image.        
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', IMG_FILE)
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # compare the two strings
        self.assertEqual(src_string, f"data:image/jpeg;base64,{b64_msg}")