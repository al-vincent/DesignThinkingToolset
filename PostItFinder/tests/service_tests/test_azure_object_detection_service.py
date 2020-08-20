from django.conf import settings
from PostItFinder import azure_services
import PostItFinder.tests.resources.test_results.azure_obj_det_results as RESULTS
import unittest
import os

# ================================================================================================
# HELPER FUNCTIONS
# ================================================================================================
def get_file_path(file_name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_path = os.path.abspath(os.path.join(current_dir, os.pardir))
    return os.path.join(test_path, "resources", "test_images", file_name)

# ================================================================================================
# TEST CLASSES
# ================================================================================================
class TestAnalyseImage(unittest.TestCase):
    def setUp(self):       
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)

    def tearDown(self):
        del(self.image_path, self.img_bytes)

    def test_get_file_bytes_correct_path_returns_bytes(self):
        """
        Check that get_file_bytes returns a bytes object when provided with the correct path     
        """
        img = azure_services.get_file_bytes(self.image_path)
        self.assertTrue(isinstance(img, bytes))
    
    def test_get_file_bytes_wrong_path_returns_none(self):
        """
        Check that get_file_bytes returns none with an incorrect image path
        """
        img = azure_services.get_file_bytes("fake_file.jpg")
        self.assertIsNone(img)

    def test_analyse_image_returns_correct_data(self):
        """
        Check that analyse_image returns the correct results when provided the correct arguments 
        """
        # get actual results from Azure service
        aod = azure_services.ObjectDetector(image_data=self.img_bytes, 
                                            prediction_key=settings.OBJ_DET_PREDICTION_KEY,
                                            obj_det_url=settings.OBJ_DET_API_URL)
        results = aod.analyse_image()
        # get expected results from features file
        expected_results = RESULTS.OBJ_DET_RESULTS

        # we cannot compare the two at the top level, because the results 
        # include timestamps, UUIDs etc. that will differ. But the predictions
        # should be the same.
        self.assertListEqual(results["predictions"], expected_results["predictions"])
    
    def test_analyse_image_returns_none_with_bad_image_path(self):
        """
        Check that analyse_image returns None when image_path == None
        """
        aod = azure_services.ObjectDetector(image_data=None, 
                                            prediction_key=settings.OBJ_DET_PREDICTION_KEY,
                                            obj_det_url=settings.OBJ_DET_API_URL)
        results = aod.analyse_image()
        self.assertIsNone(results)

    def test_analyse_image_returns_none_with_non_image_input(self):
        txt_bytes = azure_services.get_file_bytes(get_file_path("test_file.txt"))
        aod = azure_services.ObjectDetector(image_data=txt_bytes, 
                                            prediction_key=settings.OBJ_DET_PREDICTION_KEY,
                                            obj_det_url=settings.OBJ_DET_API_URL)
        results = aod.analyse_image()
        self.assertIsNone(results)
                            
    def test_analyse_image_returns_none_with_bad_prediction_key(self):
        """
        Check that analyse_image returns None when prediction_key == None
        """
        aod = azure_services.ObjectDetector(image_data=self.img_bytes,
                                            prediction_key="invalid_pred_key",
                                            obj_det_url=settings.OBJ_DET_API_URL)
        results = aod.analyse_image()
        self.assertIsNone(results)

    
    def test_analyse_image_returns_none_with_bad_api_url(self):
        """
        Check that analyse_image returns None when obj_det_url is invalid
        """
        # slice the last digit off the actual API URL
        invalid_url = settings.OBJ_DET_API_URL[:-1]        
        aod = azure_services.ObjectDetector(image_data=self.img_bytes, 
                                            prediction_key=settings.OBJ_DET_PREDICTION_KEY,
                                            obj_det_url=invalid_url)
        results = aod.analyse_image()
        self.assertIsNone(results)

# ------------------------------------

class TestProcessOutput(unittest.TestCase):
    def setUp(self):        
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.aod = azure_services.ObjectDetector(image_data=self.img_bytes, 
                                                prediction_key=settings.OBJ_DET_PREDICTION_KEY,
                                                obj_det_url=settings.OBJ_DET_API_URL)
    
    def tearDown(self):
        del(self.image_path, self.img_bytes, self.aod)

    def test_process_output_provides_correct_results(self):
        """
        Check that process_output returns expected results with default confidence threshold
        """        
        results = {
            "id": "594a913a-f079-47ec-a04e-0accbad2662e",
            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
            "created": "2020-07-16T12:11:50.062Z",
            "predictions": [{
                "probability": 0.2305683,                
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note", 
                "boundingBox": {
                    "left": 0.290309846,
                    "top": 0.310755759,
                    "width": 0.408914924,
                    "height": 0.355182737
                }               
            },
            {
                "probability": 0.9305683,
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",
                "boundingBox": {
                    "left": 0.290309846,
                    "top": 0.310755759,
                    "width": 0.408914924,
                    "height": 0.355182737
                }
            }]
        }
        processed_results = self.aod.process_output(results)
        expected_output = [{"x": 0.290309846, "y": 0.310755759, "width": 0.408914924, "height": 0.355182737}]
        self.assertListEqual(processed_results, expected_output)
    
    def test_process_output_returns_none_if_azure_output_contains_no_predictions_key(self):
        malformed_results = {"id": "594a913a-f079-47ec-a04e-0accbad2662e",
                            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
                            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
                            "created": "2020-07-16T12:11:50.062Z"}

        processed_results = self.aod.process_output(malformed_results)
        self.assertIsNone(processed_results)
        
    def test_process_output_returns_none_if_azure_output_is_not_a_dict(self):
        malformed_results = [None, "my_str", ["list", "of", "things"], 3, 2.145]
        for result in malformed_results:
            processed_results = self.aod.process_output(result)
            self.assertIsNone(processed_results)
    
    def test_process_output_returns_none_if_azure_output_is_empty_dict(self):
        malformed_results = {}
        processed_results = self.aod.process_output(malformed_results)
        self.assertIsNone(processed_results)
    
    def test_process_output_returns_none_if_azure_output_contains_no_probability_key(self):
        malformed_results = {
            "id": "594a913a-f079-47ec-a04e-0accbad2662e",
            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
            "created": "2020-07-16T12:11:50.062Z",
            "predictions": [{
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",
                "boundingBox": {
                    "left": 0.0130759329,
                    "top": 0.00716819149,
                    "width": 0.0930388942,
                    "height": 0.0273961946
                }
            }]
        }

        processed_results = self.aod.process_output(malformed_results)
        self.assertIsNone(processed_results)
    
    def test_process_output_returns_results_if_azure_output_contains_some_probability_keys(self):
        # In the dict below, the first sticky note doesn't have a probability but the second one does
        malformed_results = {
            "id": "594a913a-f079-47ec-a04e-0accbad2662e",
            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
            "created": "2020-07-16T12:11:50.062Z",
            "predictions": [{                
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",
                "boundingBox": {
                    "left": 0.0130759329,
                    "top": 0.00716819149,
                    "width": 0.0930388942,
                    "height": 0.0273961946
                }
            },
            {
                "probability": 0.9305683,
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",
                "boundingBox": {
                    "left": 0.290309846,
                    "top": 0.310755759,
                    "width": 0.408914924,
                    "height": 0.355182737
                }
            }]
        }

        processed_results = self.aod.process_output(malformed_results)
        expected_output = [{"x": 0.290309846, "y": 0.310755759, "width": 0.408914924, "height": 0.355182737}]
        self.assertListEqual(processed_results, expected_output)
    
    def test_process_output_returns_none_if_azure_output_contains_no_boundingBox_key(self):
        # In the dict below, the first sticky note doesn't have a probability but the second one does
        malformed_results = {
            "id": "594a913a-f079-47ec-a04e-0accbad2662e",
            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
            "created": "2020-07-16T12:11:50.062Z",
            "predictions": [{     
                "probability": 0.9305683,           
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",
            }]
        }

        processed_results = self.aod.process_output(malformed_results)
        self.assertIsNone(processed_results)

    def test_process_output_returns_results_if_azure_output_contains_some_boundingBox_keys(self):
        # In the dict below, the first sticky note doesn't have a boundingBox but the second one does
        malformed_results = {
            "id": "594a913a-f079-47ec-a04e-0accbad2662e",
            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
            "created": "2020-07-16T12:11:50.062Z",
            "predictions": [{
                "probability": 0.9305683,                
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",                
            },
            {
                "probability": 0.9305683,
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",
                "boundingBox": {
                    "left": 0.290309846,
                    "top": 0.310755759,
                    "width": 0.408914924,
                    "height": 0.355182737
                }
            }]
        }

        processed_results = self.aod.process_output(malformed_results)
        expected_output =  [{"x": 0.290309846, "y": 0.310755759, "width": 0.408914924, "height": 0.355182737}]
        self.assertListEqual(processed_results, expected_output)

    def test_process_output_returns_none_if_all_regions_are_below_confidence_threshold(self):
        # Neither sticky note has a high enough probability to be included in the results
        results = {
            "id": "594a913a-f079-47ec-a04e-0accbad2662e",
            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
            "created": "2020-07-16T12:11:50.062Z",
            "predictions": [{
                "probability": 0.2305683,                
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note", 
                "boundingBox": {
                    "left": 0.290309846,
                    "top": 0.310755759,
                    "width": 0.408914924,
                    "height": 0.355182737
                }               
            },
            {
                "probability": 0.0305683,
                "tagId": "faf8ea2f-571f-4315-a138-2366624c5281",
                "tagName": "sticky note",
                "boundingBox": {
                    "left": 0.290309846,
                    "top": 0.310755759,
                    "width": 0.408914924,
                    "height": 0.355182737
                }
            }]
        }

        processed_results = self.aod.process_output(results)
        self.assertIsNone(processed_results)
