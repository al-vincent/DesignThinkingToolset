from django.urls import resolve
from django.test import TestCase
from PostItFinder.views import index

class HomePageTests(TestCase):

    def test_root_url_resolves_to_index_view(self):
        url_found = resolve("/")
        self.assertEqual(url_found.func, index)