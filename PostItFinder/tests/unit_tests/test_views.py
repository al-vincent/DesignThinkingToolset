from django.urls import resolve, reverse
from django.test import TestCase
from django.conf import settings

import os
from json import load

from PostItFinder.views import index, about, faq, choose_image, set_regions, analyse_text

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

class ChooseImagePageTests(TestCase):
    def test_set_regions_url_resolves_to_set_regions_view(self):
        url_found = resolve(reverse(HTML["CHOOSE_IMAGE"]["URL"]))
        self.assertEqual(url_found.func, choose_image)
    
    def test_set_regions_uses_template(self):
        response = self.client.get(reverse(HTML["CHOOSE_IMAGE"]["URL"]))
        self.assertTemplateUsed(response, PATHS["CHOOSE_IMAGE"])


class SetRegionsPageTests(TestCase):
    def test_set_regions_url_resolves_to_set_regions_view(self):
        url_found = resolve(reverse(HTML["SET_REGIONS"]["URL"]))
        self.assertEqual(url_found.func, set_regions)
    
    def test_set_regions_uses_template(self):
        response = self.client.get(reverse(HTML["SET_REGIONS"]["URL"]))
        self.assertTemplateUsed(response, PATHS["SET_REGIONS"])

class AnalyseTextPageTests(TestCase):
    def test_analyse_text_url_resolves_to_analyse_text_view(self):
        url_found = resolve(reverse(HTML["ANALYSE_TEXT"]["URL"]))
        self.assertEqual(url_found.func, analyse_text)
    
    def test_analyse_text_uses_template(self):
        response = self.client.get(reverse(HTML["ANALYSE_TEXT"]["URL"]))
        self.assertTemplateUsed(response, PATHS["ANALYSE_TEXT"])
