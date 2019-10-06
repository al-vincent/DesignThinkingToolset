from django.conf import settings
from PostItFinder import azure_object_detection

import unittest
import os
from json import load


class TestAnalyseImage(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
            IMG_PATH = load(f)["PATHS"]["TEST_IMG"]
        self.image_path = os.path.join(settings.MEDIA_DIR, IMG_PATH["DIR"], IMG_PATH["FILE"]) 

    def tearDown(self):
        # del(IMG_PATH, self.image_path)
        pass

    def test_get_image_bytes_returns_bytes_with_correct_path(self):
        img = azure_object_detection.get_image_bytes(self.image_path)
        self.assertTrue(isinstance(img, bytes))