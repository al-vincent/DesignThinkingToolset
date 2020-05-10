from django.urls import resolve, reverse
from django.test import TestCase
from django.conf import settings

import os
from json import load

from PostItFinder.views import index, about, faq, set_regions

with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
        CONFIG = load(f)
        PATHS = CONFIG["PATHS"]
        HTML = CONFIG["HTML"]

class HomePageTests(TestCase):

    def test_root_url_resolves_to_index_view(self):
        url_found = resolve("/")
        self.assertEqual(url_found.func, index)
    
    def test_index_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, PATHS["HOME"])

    # def test_get_image_file(self):         
        # response = self.client.post('/', data={"img_file": 'A new list item'
        # self.assertIn('A new list item', response.content.decode())
        # pass

class AboutPageTests(TestCase):

    def test_about_url_resolves_to_about_view(self):        
        url_found = resolve(reverse(HTML["BASE"]["NAVBAR"]["PAGES"][0]["URL"]))
        self.assertEqual(url_found.func, about)
    
    def test_about_uses_template(self):
        response = self.client.get(reverse(HTML["BASE"]["NAVBAR"]["PAGES"][0]["URL"]))
        self.assertTemplateUsed(response, PATHS["ABOUT"])

class FaqPageTests(TestCase):

    def test_faq_url_resolves_to_faq_view(self):        
        url_found = resolve(reverse(HTML["BASE"]["NAVBAR"]["PAGES"][1]["URL"]))
        self.assertEqual(url_found.func, faq)
    
    def test_faq_uses_template(self):
        response = self.client.get(reverse(HTML["BASE"]["NAVBAR"]["PAGES"][1]["URL"]))
        self.assertTemplateUsed(response, PATHS["FAQ"])

class SetRegionsPageTests(TestCase):

    def test_set_regions_url_resolves_to_set_regions_view(self):
        url_found = resolve(reverse(HTML["HOME"]["NEXT_BTN"]["URL"]))
        self.assertEqual(url_found.func, set_regions)
    
    def test_set_regions_uses_template(self):
        response = self.client.get(reverse(HTML["HOME"]["NEXT_BTN"]["URL"]))
        self.assertTemplateUsed(response, PATHS["SET_REGIONS"])