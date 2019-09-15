from django.urls import resolve
from django.test import TestCase
from django.conf import settings

import os
from json import load

from PostItFinder.views import index

# with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
#         CONFIG = load(f)["HTML"]

class HomePageTests(TestCase):

    def test_root_url_resolves_to_index_view(self):
        url_found = resolve("/")
        self.assertEqual(url_found.func, index)
    
    def test_index_uses_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'PostItFinder/index.html')

    def test_get_image_file(self):
        # response = self.client.post('/', data={'item_text': 'A new list item'})
        # self.assertIn('A new list item', response.content.decode())
        pass