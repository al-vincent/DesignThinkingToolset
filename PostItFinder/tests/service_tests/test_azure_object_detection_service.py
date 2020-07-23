from django.conf import settings
from PostItFinder import azure_services
import unittest
import os
from json import load
import base64

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
class TestGetImageData(unittest.TestCase):
    def setUp(self):       
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.confidence_threshold = 0.3
        self.aod = azure_services.ObjectDetector(image_data=self.img_bytes,                                            
                                            confidence_threshold=self.confidence_threshold)

    def tearDown(self):
        pass

    def test_b64_encoded_img_correctly_converted_to_bytes(self):
        # get the image as base64-encoded bytes
        with open(self.image_path, "rb") as f:
            img_bytes = f.read()
            img_str = base64.b64encode(img_bytes).decode("utf-8")
        
        # make sure that the image is actually a str (otherwise the test won't mean anything)
        self.assertTrue(isinstance(img_str, str))
        
        # convert the str to bytes and check the return type is correct
        encoded_bytes = self.aod.get_image_data(img_str)
        self.assertTrue(isinstance(encoded_bytes, bytes))

        # finally, make sure that the bytes returned are correct by comparing the output of the 
        # function to the output of file.read() as binary
        self.assertEqual(img_bytes, encoded_bytes)
    
    def test_non_b64_encoded_str_returns_none(self):
        random_str = "Hello world"
        encoded_bytes = self.aod.get_image_data(random_str)
        self.assertIsNone(encoded_bytes)
    
    def test_incomplete_b64_encoded_str_returns_none(self):
        """
        NOTE: this test is slightly rigged, in that it slices off 5 characters from 
        the end of the input string. HOWEVER, if the number of characters sliced off
        is a multiple of 4 then None *WILL NOT* be returned.
        """
        with open(self.image_path, "rb") as f:
            img_str = base64.b64encode(f.read()).decode("utf-8")
        self.assertIsNone(self.aod.get_image_data(img_str[:-5]))

    def test_bytestream_input_is_returned_unchanged(self):
        # first run the test with image bytes as the input
        with open(self.image_path, "rb") as f:
            img_bytes = f.read()
        self.assertEqual(img_bytes, self.aod.get_image_data(img_bytes))

        # now rerun with text bytes as input
        with open(get_file_path("test_file.txt"), "rb") as f:
            txt_bytes = f.read()
        self.assertEqual(txt_bytes, self.aod.get_image_data(txt_bytes))

    def test_non_str_or_bytes_input_returns_none(self):
        # provide a range of data types
        for input in [1, {"a": 123, "b": 456}, ["a", "b", "c"], None]:
            self.assertIsNone(self.aod.get_image_data(input))
    
    # def test_non_image_b64_encoded_str_returns_none(self):
    #     """
    #     The get_image_data method makes no distinction between an image file and any other form 
    #     of base64-encoded binary data (provided the encoding is correct), so the 
    #     """
    #     with open(get_file_path("test_file.txt"), "rb") as f:
    #         txt_str = base64.b64encode(f.read()).decode("utf-8")
        
    #     # make sure that the image is actually a str (otherwise the test won't mean anything)
    #     self.assertTrue(isinstance(txt_str, str))

    #     # finally, check that get_image_data correctly spots that the input is not an image,
    #     # and returns None
    #     self.assertIsNone(self.aod.get_image_data(txt_str))

# ------------------------------------

class TestImageDataIsValid(unittest.TestCase):
    def setUp(self):      
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.confidence_threshold = 0.3
        self.aod = azure_services.ObjectDetector(image_data=self.img_bytes,                                            
                                            confidence_threshold=self.confidence_threshold)

    def tearDown(self):
        pass

    def test_acceptable_image_validates_correctly(self):
        with open(self.image_path, "rb") as f:
            img_bytes = f.read()
    
        self.assertTrue(self.aod.image_data_is_valid(img_bytes))

    def test_too_large_image_is_invalid(self):
        with open(get_file_path("test_gif.gif"), "rb") as f:
            img_bytes = f.read()

        self.assertFalse(self.aod.image_data_is_valid(img_bytes))

    def test_non_image_is_invalid(self):
        pass
    
    def test_wrong_image_type_is_invalid(self):
        pass

    # ...Anything else??!

# ------------------------------------

class TestAnalyseImage(unittest.TestCase):
    def setUp(self):       
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.confidence_threshold = 0.3

    def tearDown(self):
        # del(IMG_PATH, self.image_path)
        pass    

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
        aod = azure_services.ObjectDetector(image_data=self.img_bytes)
        results = aod.analyse_image()

        expected_bbox = {'left': 0.0130759329, 'top': 0.00716819149, 'width': 0.0930388942, 'height': 0.0273961946}
        self.assertDictEqual(results["predictions"][0]["boundingBox"], expected_bbox)
    
    def test_analyse_image_returns_none_with_bad_image_path(self):
        """
        Check that analyse_image returns None when image_path == None
        """
        aod = azure_services.ObjectDetector(image_data=None)
        results = aod.analyse_image()
        self.assertIsNone(results)

    def test_analyse_image_returns_none_with_non_image_input(self):
        txt_bytes = azure_services.get_file_bytes(get_file_path("test_file.txt"))
        aod = azure_services.ObjectDetector(image_data=txt_bytes)
        results = aod.analyse_image()
        self.assertIsNone(results)
                            
    def test_analyse_image_returns_none_with_bad_prediction_key(self):
        """
        Check that analyse_image returns None when prediction_key == None
        """
        aod = azure_services.ObjectDetector(image_data=self.img_bytes,
                                            prediction_key="invalid_pred_key")
        results = aod.analyse_image()
        self.assertIsNone(results)

    def test_analyse_image_returns_none_with_bad_base_url(self):
        """
        Check that analyse_image returns None when project_id == None
        """
        aod = azure_services.ObjectDetector(image_data=self.img_bytes,
                                            base_url="www.invalid_base_url.com")
        results = aod.analyse_image()
        self.assertIsNone(results)
    
    def test_analyse_image_returns_none_with_bad_api_url(self):
        """
        Check that analyse_image returns None when published_name == None
        """
        aod = azure_services.ObjectDetector(image_data=self.img_bytes,
                                            obj_det_url="invalid/api/url")
        results = aod.analyse_image()
        self.assertIsNone(results)

    def test_analyse_image_returns_none_with_no_predictions_in_results(self):
        # NOTE: I can't think of any way to test this?! The 'predictions' key in the
        # json is part of the Azure results, and handled within analyse_image - I 
        # can'tprovide a way of malforming the input to replicate this (should never 
        # happen, but 'should' != 'will'...)
        pass



# ------------------------------------

class TestProcessOutput(unittest.TestCase):
    def setUp(self):        
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.aod = azure_services.ObjectDetector(image_data=self.img_bytes)

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
        expected_output = {"threshold": 0.3, 
                            "data": [{"x": 0.290309846, "y": 0.310755759, "width": 0.408914924, "height": 0.355182737}]}      
        self.assertDictEqual(processed_results, expected_output)
    
    def test_process_output_returns_none_if_azure_output_contains_no_predictions_key(self):
        malformed_results = {"id": "594a913a-f079-47ec-a04e-0accbad2662e",
                            "project": "214f209e-99cf-4412-b942-7cfc0e6f445a",
                            "iteration": "f579bf38-1cb5-4a92-ac48-cf504475d573",
                            "created": "2020-07-16T12:11:50.062Z"}

        processed_results = self.aod.process_output(malformed_results)
        expected_output = {"threshold": 0.3, "data": None}
        self.assertDictEqual(processed_results, expected_output)
        
    def test_process_output_returns_none_if_azure_output_is_not_a_dict(self):
        malformed_results = [None, "my_str", ["list", "of", "things"], 3, 2.145]
        for result in malformed_results:
            processed_results = self.aod.process_output(result)
            expected_output = {"threshold": 0.3, "data": None}
            self.assertDictEqual(processed_results, expected_output)
    
    def test_process_output_returns_none_if_azure_output_is_empty_dict(self):
        malformed_results = {}
        processed_results = self.aod.process_output(malformed_results)
        expected_output = {"threshold": 0.3, "data": None}
        self.assertDictEqual(processed_results, expected_output)
    
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
        expected_output = {"threshold": 0.3, "data": None}
        self.assertDictEqual(processed_results, expected_output)
    
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
        expected_output = {"threshold": 0.3, 
                        "data": [{"x": 0.290309846, "y": 0.310755759, "width": 0.408914924, "height": 0.355182737}]}
        self.assertDictEqual(processed_results, expected_output)
    
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
        expected_output = {"threshold": 0.3, "data": None}
        self.assertDictEqual(processed_results, expected_output)

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
        expected_output = {"threshold": 0.3, 
                        "data": [{"x": 0.290309846, "y": 0.310755759, "width": 0.408914924, "height": 0.355182737}]}
        self.assertDictEqual(processed_results, expected_output)

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
        expected_output = {"threshold": 0.3, "data": None}
        self.assertDictEqual(processed_results, expected_output)


# ------------------------------------
        


    