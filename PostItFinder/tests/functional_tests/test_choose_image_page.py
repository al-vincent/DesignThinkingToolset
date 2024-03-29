from django.conf import settings
from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import unittest
import time
import os
from json import load
import base64

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
        # call the 'normal' setUp from the base class
        super().setUp()

        # navigate from the home page to the choose-image page
        base.navigate_to_choose_image_page(self.browser)
        
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
        response = self.client.get(reverse(base.ELEMS["CHOOSE_IMAGE"]["URL"]))
        self.assertTemplateUsed(response, base.PATHS["CHOOSE_IMAGE"])

    def test_page_has_correct_title(self):
        """
        Ensure that the page title includes the correct text.
        """
        self.assertEqual(base.ELEMS["CHOOSE_IMAGE"]["TITLE"], self.browser.title)
    
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
            if items.index(item) <= 0:            
                self.assertIn("active", step.get_attribute("class"))
            else:
                self.assertNotIn("active", step.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Explanatory text tests
    # -------------------------------------------------------------------------------------
    def test_explain_text_is_displayed(self):
        explain_txt = self.browser.find_element_by_id(base.ELEMS["APP"]["EXPLAIN_TEXT"]["ID"])
        self.assertTrue(explain_txt.is_displayed())

    def test_explain_text_is_correct(self):
        explain_txt = self.browser.find_element_by_id(base.ELEMS["APP"]["EXPLAIN_TEXT"]["ID"])
        intended_text = base.ELEMS["CHOOSE_IMAGE"]["EXPLAIN_TEXT"]["TEXT"]
        self.assertEqual(explain_txt.get_attribute("innerText"), intended_text)

    # -------------------------------------------------------------------------------------
    # Choose-image button tests
    # -------------------------------------------------------------------------------------    
    def test_choose_image_input_is_active(self):
        img_input = self.browser.find_element_by_id(base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"])
        self.assertTrue(img_input.is_enabled())
    
    def test_choose_image_label_has_correct_label_text(self):
        """
        Test whether the choose-image page has a button for uploading images to the service,
        and whether the button contains the correct text.

        The label element has no ID of its own, so use XPath to find / select it.
        """
        cfg = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]
        input_id = cfg["ID"]
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')
        self.assertEqual(img_label.get_attribute("innerText"), cfg["TEXT"])

    # -------------------------------------------------------------------------------------
    # Upload-image button tests
    # -------------------------------------------------------------------------------------    
    def test_upload_image_button_is_disabled(self):
        upload_img_btn = self.browser.find_element_by_id(base.ELEMS["CHOOSE_IMAGE"]["UPLOAD_IMG_BTN"]["ID"])
        self.assertFalse(upload_img_btn.is_enabled())

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_next_button_is_displayed(self):        
        next_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"])
        self.assertTrue(next_btn.is_displayed())

    def test_next_button_is_disabled(self):        
        next_btn = self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"])
        self.assertTrue(next_btn.get_attribute("aria-disabled"))
        self.assertIn("disabled", next_btn.get_attribute("class"))

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    def test_previous_button_does_not_exist(self):
        # NOTE: this works as follows:
        #   - find_elements_by_id will return a list.
        #   - if there are no elements in the DOM with the ID, it'll be an empty list
        #   - an empty list is falsey, so can use assertFalse directly
        prev_btn = self.browser.find_elements_by_id(base.ELEMS["APP"]["PREVIOUS_BTN"]["ID"])
        self.assertFalse(prev_btn)

    # -------------------------------------------------------------------------------------
    # Preview pane tests
    # -------------------------------------------------------------------------------------
    def test_image_pane_exists(self):
        img_pane = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertTrue(img_pane)

    def test_image_pane_does_not_contain_img(self):
        img_pane = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        imgs = img_pane.find_elements_by_tag_name("img")
        self.assertFalse(imgs)


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
        # call the 'normal' setUp from the base class
        super().setUp()

        # navigate from the home page to the choose-image page
        base.navigate_to_choose_image_page(self.browser)
        
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
    def test_clicking_logo_takes_user_to_home(self):
        base_url = self.live_server_url
        logo = base.ELEMS["BASE"]["NAVBAR"]["LOGO"]
        self.browser.find_element_by_id(logo["ID"]).click()
        self.assertEqual(self.browser.current_url, base_url + reverse(logo["URL"]))

    def test_clicking_about_takes_user_to_faq_page(self):
        base_url = self.live_server_url
        page = base.ELEMS["BASE"]["NAVBAR"]["PAGES"][0]        
        self.browser.find_element_by_id(page["ID"]).click()
        self.assertEqual(self.browser.current_url, base_url + reverse(page["URL"]))

    def test_clicking_faq_takes_user_to_faq_page(self):
        base_url = self.live_server_url
        page = base.ELEMS["BASE"]["NAVBAR"]["PAGES"][1]        
        self.browser.find_element_by_id(page["ID"]).click()
        self.assertEqual(self.browser.current_url, base_url + reverse(page["URL"]))

    # -------------------------------------------------------------------------------------
    # Stepper bar tests
    # -------------------------------------------------------------------------------------
    # None

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

    def test_selecting_image_enables_upload_image_btn_and_next_btn(self):
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check that both the Upload Image button and the Next button are enabled
        upload_img_btn_id = base.ELEMS["CHOOSE_IMAGE"]["UPLOAD_IMG_BTN"]["ID"]
        upload_img_btn = self.browser.find_element_by_id(upload_img_btn_id)
        self.assertTrue(upload_img_btn.is_enabled())

        next_btn_id = base.ELEMS["APP"]["NEXT_BTN"]["ID"]
        next_btn = self.browser.find_element_by_id(next_btn_id)
        self.assertTrue(next_btn.is_enabled())
    
    def test_jpg_can_be_selected(self):
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the image src attribute is no longer '#'
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertNotIn("#", img.get_attribute("src"))
    
    def test_png_can_be_selected(self):
        img_file = "test_png.png"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the image src attribute is no longer '#'
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertNotIn("#", img.get_attribute("src"))
    
    def test_bmp_can_be_selected(self):
        img_file = "test_bmp_small.bmp"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the image src attribute is no longer '#'
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertNotIn("#", img.get_attribute("src"))
    
    def test_gif_cannot_be_selected(self):
        img_file = "test_gif.gif"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        
        # update the input directly with the file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)

        # wait for the alert to fire
        try: 
            WebDriverWait(self.browser, base.MAX_WAIT).until(EC.alert_is_present(),
                                   "Timed out waiting for alert to appear.")
            alert = self.browser.switch_to.alert
            alert.accept()            
        except TimeoutException:
            self.fail("ERROR - alert was not fired")

        # check that the image src attribute is still the default pic
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertIn("no-image.png", img.get_attribute("src"))

    def test_tif_cannot_be_selected(self):
        img_file = "test_tif.tif"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        
        # update the input directly with the file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)
        
        # wait for the alert to fire
        try: 
            WebDriverWait(self.browser, base.MAX_WAIT).until(EC.alert_is_present(),
                                   "Timed out waiting for alert to appear.")
            alert = self.browser.switch_to.alert
            alert.accept()            
        except TimeoutException:
            self.fail("ERROR - alert was not fired")

        # check that the image src attribute is still the default
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertIn("no-image.png", img.get_attribute("src"))

    def test_image_src_updates_correctly(self):
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the base64-encoded string of the image is correct 
        # encode the image in base64 and convert to utf-8
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # get the src data for the image as a UTF-8 string decoded from base64
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src_string = img.get_attribute("src")

        # compare the two (with short string added to start of python encoding)
        self.assertEqual(src_string, f"data:image/jpeg;base64,{b64_msg}")

    def test_selecting_new_image_overwrites_previous_image(self):
        img1 = "test_png.png"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]
        
        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))

        # update the input directly with the file path
        path = os.path.join(test_path, "resources", "test_images", img1)
        input_elem.send_keys(path)

        # short wait to allow image to update
        time.sleep(2)

        # get the src data for the image as a UTF-8 string decoded from base64
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src_string = img.get_attribute("src")

        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        self.assertEqual(src_string, f"data:image/png;base64,{b64_msg}")

        # update the input with the file path for img2
        img2 = "test_jpg.jpg"
        path = os.path.join(test_path, "resources", "test_images", img2)
        input_elem.send_keys(path)

        # short wait to allow image to update
        time.sleep(2)

        # get the src data for the image as a UTF-8 string decoded from base64
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src_string = img.get_attribute("src")

        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')
        
        # compare the string for img2 to the src for the current image
        self.assertEqual(src_string, f"data:image/jpeg;base64,{b64_msg}")

    def test_too_large_file_throws_alert_and_is_rejected(self):
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        initial_img_src = img.get_attribute("src")

        img_file = "test_bmp.bmp"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        # path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)
        # self.assertEqual(img_label.get_attribute("innerText"), img_file)

        try: 
            WebDriverWait(self.browser, base.MAX_WAIT).until(EC.alert_is_present(),
                                   "Timed out waiting for alert to appear.")
            alert = self.browser.switch_to.alert
            alert.accept()            
        except TimeoutException:
            self.fail("ERROR - alert was not fired")

        # check whether the image src attribute has changed (it shouldn't have!)
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertEqual(initial_img_src, img.get_attribute("src"))

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_clicking_next_button_takes_user_to_set_regions_page(self):
        # load an image so enable the button
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        # path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        path = os.path.join(test_path, "resources", "test_images", img_file)
        input_elem.send_keys(path)

        # wait a few seconds for the image to render
        time.sleep(3)

        # click the 'upload-image' button, and wait for the button text to change
        self.browser.find_element_by_id(base.ELEMS["CHOOSE_IMAGE"]["UPLOAD_IMG_BTN"]["ID"]).click()
        WebDriverWait(self.browser, base.MAX_WAIT).until(
            EC.text_to_be_present_in_element((By.ID, base.ELEMS["CHOOSE_IMAGE"]["UPLOAD_IMG_BTN"]["ID"]),
                                            base.ELEMS["CHOOSE_IMAGE"]["UPLOAD_IMG_BTN"]["SUCCESS_TEXT"])
        )

        # click the Next button
        base_url = self.live_server_url        
        self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"]).click()
        expected_url = reverse(base.ELEMS["CHOOSE_IMAGE"]["NEXT_BTN"]["URL"])
        self.assertEqual(self.browser.current_url, base_url + expected_url)

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    # None; Previous button is not displayed