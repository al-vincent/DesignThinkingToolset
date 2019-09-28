from django.conf import settings
import PostItFinder.azure_object_detection

import unittest
import os
from json import load


class TestAnalyseImage(unittest.TestCase):
    def setUp(self):
        with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
            IMG_PATH = load(f)["PATHS"]["TEST_IMG"]
        self.image_path = os.path.join(settings.MEDIA_DIR, IMG_PATH["DIR"], IMG_PATH["FILE"])
        print(self.image_path)

    def tearDown(self):
        pass

    def test_image_read(self):
        pass