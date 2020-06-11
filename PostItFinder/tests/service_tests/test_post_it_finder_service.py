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

    def test_get_image_bytes_correct_path_returns_bytes(self):
        """
        Check that get_image_bytes returns a bytes object when provided with the correct path     
        """
        img = azure_object_detection.get_image_bytes(self.image_path)
        self.assertTrue(isinstance(img, bytes))
    
    def test_get_image_bytes_wrong_path_returns_none(self):
        """
        Check that get_image_bytes returns none with an incorrect image path
        """
        img = azure_object_detection.get_image_bytes("fake_file.jpg")
        self.assertIsNone(img)

    def test_analyse_image_returns_correct_data(self):
        """
        Check that analyse_image returns the correct results when provided the correct arguments 
        """
        img_bytes = azure_object_detection.get_image_bytes(self.image_path)
        data = azure_object_detection.analyse_image(prediction_key=os.getenv("PREDICTION_KEY"),
                                                    subscription_key=os.getenv("SUBSCRIPTION_KEY"),
                                                    project_id=os.getenv("PROJECT_ID"),
                                                    published_name=os.getenv("PUBLISHED_NAME"),
                                                    image_bytes = img_bytes)
        expected_bbox = {'left': 0.240892157, 'top': 0.29552865, 'width': 0.48589474, 'height': 0.3891474}
        self.assertDictEqual(data['predictions'][0]['boundingBox'], expected_bbox)
    
    def test_analyse_image_returns_none_with_bad_prediction_key(self):
        """
        Check that analyse_image returns None when prediction_key == None
        """
        img_bytes = azure_object_detection.get_image_bytes(self.image_path)
        data = azure_object_detection.analyse_image(prediction_key=None,
                                                    subscription_key=os.getenv("SUBSCRIPTION_KEY"),
                                                    project_id=os.getenv("PROJECT_ID"),
                                                    published_name=os.getenv("PUBLISHED_NAME"),
                                                    image_bytes = img_bytes)
        self.assertIsNone(data)
    
    
    def test_analyse_image_returns_none_with_bad_subscription_key(self):
        """
        Check that analyse_image returns None when subscription_key == None
        """
        img_bytes = azure_object_detection.get_image_bytes(self.image_path)
        data = azure_object_detection.analyse_image(prediction_key=os.getenv("PREDICTION_KEY"),
                                                    subscription_key=None,
                                                    project_id=os.getenv("PROJECT_ID"),
                                                    published_name=os.getenv("PUBLISHED_NAME"),
                                                    image_bytes = img_bytes)
        self.assertIsNone(data)

    def test_analyse_image_returns_none_with_bad_project_id(self):
        """
        Check that analyse_image returns None when project_id == None
        """
        img_bytes = azure_object_detection.get_image_bytes(self.image_path)
        data = azure_object_detection.analyse_image(prediction_key=os.getenv("PREDICTION_KEY"),
                                                    subscription_key=os.getenv("SUBSCRIPTION_KEY"),
                                                    project_id=None,
                                                    published_name=os.getenv("PUBLISHED_NAME"),
                                                    image_bytes = img_bytes)
        self.assertIsNone(data)
    
    def test_analyse_image_returns_none_with_bad_published_name(self):
        """
        Check that analyse_image returns None when published_name == None
        """
        img_bytes = azure_object_detection.get_image_bytes(self.image_path)
        data = azure_object_detection.analyse_image(prediction_key=os.getenv("PREDICTION_KEY"),
                                                    subscription_key=os.getenv("SUBSCRIPTION_KEY"),
                                                    project_id=os.getenv("PROJECT_ID"),
                                                    published_name=None,
                                                    image_bytes = img_bytes)
        self.assertIsNone(data)

    def test_analyse_image_returns_none_with_bad_image_path(self):
        """
        Check that analyse_image returns None when image_path == None
        """
        data = azure_object_detection.analyse_image(prediction_key=os.getenv("PREDICTION_KEY"),
                                                    subscription_key=os.getenv("SUBSCRIPTION_KEY"),
                                                    project_id=os.getenv("PROJECT_ID"),
                                                    published_name=os.getenv("PUBLISHED_NAME"),
                                                    image_bytes = None)
        self.assertIsNone(data)