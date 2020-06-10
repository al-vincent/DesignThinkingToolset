from selenium.webdriver.support.ui import Select
from django.conf import settings
from django.urls import reverse

import time
import os
from json import load
import base64

# from functional_tests import base
from project_tests.functional_tests import base


# =========================================================================================
# STATIC TESTS
# =========================================================================================
class ChooseImagePageStaticTests(base.StaticTests):
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
        self.navigate_to_choose_image_page()

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
class ChooseImagePageDynamicTests(base.DynamicTests):
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
        self.navigate_to_choose_image_page()
        
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

    def test_jpg_can_be_selected(self):
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
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
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the image src attribute is no longer '#'
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertNotIn("#", img.get_attribute("src"))
    
    def test_bmp_can_be_selected(self):
        img_file = "test_bmp.bmp"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the image src attribute is no longer '#'
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertNotIn("#", img.get_attribute("src"))
    
    def test_gif_can_be_selected(self):
        img_file = "test_gif.gif"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the image src attribute is no longer '#'
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertNotIn("#", img.get_attribute("src"))

    def test_tif_cannot_be_selected(self):
        img_file = "test_tif.tif"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        input_elem.send_keys(path)
        self.assertEqual(img_label.get_attribute("innerText"), img_file)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the image src attribute is no longer '#'
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        self.assertIn("#", img.get_attribute("src"))

    def test_file_info_put_in_sessionStorage(self):    
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        input_elem.send_keys(path)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the base64-encoded string of the image held in sessionStorage 
        # is correct 
        # encode the image in base64 and convert to utf-8
        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')

        # get the file encoding from sessionStorage
        data_key = base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["FILE_DATA_KEY"]
        script = f"return sessionStorage.getItem('{data_key}');"
        # compare the two (with short string added to start of python encoding)
        self.assertEqual(self.browser.execute_script(script), 
                        f"data:image/jpeg;base64,{b64_msg}")

        # check whether the file name is in sessionStorage
        name_key = base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["FILE_NAME_KEY"]
        script = f"return sessionStorage.getItem('{name_key}');"
        self.assertEqual(self.browser.execute_script(script), img_file)

    def test_image_src_updates_correctly(self):
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        input_elem.send_keys(path)

        # wait a few seconds for the image to render
        time.sleep(3)

        # check whether the base64-encoded string of the image held in sessionStorage 
        # is correct 
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
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img1)
        input_elem.send_keys(path)

        # short wait
        time.sleep(2)

        # update the input with the file path for img2
        img2 = "test_jpg.jpg"
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img2)
        input_elem.send_keys(path)

        # get the src data for the image as a UTF-8 string decoded from base64
        img = self.browser.find_element_by_id(base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["ID"])
        src_string = img.get_attribute("src")

        with open(path, "rb") as f:
            b64_encoded_img = base64.b64encode(f.read())
            b64_msg = b64_encoded_img.decode('utf-8')
        
        # compare the string for img2 to the src for the current image
        self.assertEqual(src_string, f"data:image/jpeg;base64,{b64_msg}")

        # get the encoding from sessionStorage
        data_key = base.ELEMS["APP"]["IMAGE_PANE"]["IMAGE"]["FILE_DATA_KEY"]
        script = f"return sessionStorage.getItem('{data_key}');"

        # compare the two (with short string added to start of python encoding)
        self.assertEqual(self.browser.execute_script(script), 
                        f"data:image/jpeg;base64,{b64_msg}")

    # -------------------------------------------------------------------------------------
    # Next button tests
    # -------------------------------------------------------------------------------------
    def test_clicking_next_button_takes_user_to_set_regions_page(self):
        # load an image so enable the button
        img_file = "test_jpg.jpg"
        input_id = base.ELEMS["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"]["ID"]

        # get the input and label elements
        input_elem = self.browser.find_element_by_id(input_id)
        img_label = self.browser.find_element_by_xpath(f'//label[@for="{input_id}"]')      
        
        # update the input directly with the file path
        path = os.path.join(settings.STATIC, 'PostItFinder', 'img', 'test_images', img_file)
        input_elem.send_keys(path)

        # wait a few seconds for the image to render
        time.sleep(3)

        # click the Next button
        base_url = self.live_server_url        
        self.browser.find_element_by_id(base.ELEMS["APP"]["NEXT_BTN"]["ID"]).click()
        expected_url = reverse(base.ELEMS["CHOOSE_IMAGE"]["NEXT_BTN"]["URL"])
        self.assertEqual(self.browser.current_url, base_url + expected_url)

    # -------------------------------------------------------------------------------------
    # Previous button tests
    # -------------------------------------------------------------------------------------
    # None