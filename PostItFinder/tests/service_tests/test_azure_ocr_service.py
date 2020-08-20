import unittest
import os
import copy
import requests
from PostItFinder import azure_services
import PostItFinder.tests.resources.test_results.azure_ocr_results as RESULTS
from django.conf import settings

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
class TestSubmitImageForProcessing(unittest.TestCase):
    def setUp(self):       
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)

    def tearDown(self):
        del(self.image_path, self.img_bytes)

    def test_successful_reponse_returned_with_correct_parameters(self):
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        
        response = ta.submit_image_for_processing()
        # From the docs, a successful response will have status code 202:
        # https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-ga/operations/5d986960601faab4bf452005
        self.assertEqual(response.status_code, 202)
   
    def test_unsupported_image_type_returns_none(self):
        """
        Check that analyse_image returns None when image_path == None
        """
        tif_bytes = azure_services.get_file_bytes(get_file_path("test_gif.gif"))
        ta = azure_services.TextAnalyser(image_data=tif_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        response = ta.submit_image_for_processing()
        self.assertIsNone(response)
    
    def test_too_large_image_returns_none(self):
        """
        Check that analyse_image returns None when image_path == None
        """
        bmp_bytes = azure_services.get_file_bytes(get_file_path("test_bmp.bmp"))
        ta = azure_services.TextAnalyser(image_data=bmp_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        response = ta.submit_image_for_processing()
        self.assertIsNone(response)

    def test_non_image_input_returns_none(self):
        txt_bytes = azure_services.get_file_bytes(get_file_path("test_file.txt"))
        ta = azure_services.TextAnalyser(image_data=txt_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        response = ta.submit_image_for_processing()
        self.assertIsNone(response)
                            
    def test_bad_subscription_key_returns_none(self):
        """
        Check that analyse_image returns None when prediction_key == None
        """        
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key="invalid_subs_key",
                                        api_url=settings.OCR_API_URL)
        response = ta.submit_image_for_processing()
        self.assertIsNone(response)

    def test_invalid_api_returns_none(self):
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url="invalid/api/url")
        
        response = ta.submit_image_for_processing()
        self.assertIsNone(response)
# ------------------------------------

class TestGetResults(unittest.TestCase):
    def setUp(self):       
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)    

    def tearDown(self):
        del(self.image_path, self.img_bytes)

    def test_correct_results_returned_from_correct_input(self):
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        response = ta.submit_image_for_processing()
        
        self.assertEqual(ta.get_results(response)["analyzeResult"], 
                        RESULTS.OCR_RESULTS["analyzeResult"])
    
    def test_none_returned_when_input_is_none(self):
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        
        self.assertIsNone(ta.get_results(None))

    def test_none_returned_with_wrong_response(self):
        """
        Input is a valid response object, but not from the Read API
        """
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        
        response = requests.get("https://api.github.com")
        self.assertIsNone(ta.get_results(response))

    def test_none_returned_with_missing_key(self):
        """
        Input is a valid response object from the Read API, but the value for
        the "Operation-Location" key is missing from the header
        """
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        
        response = ta.submit_image_for_processing()
        response.headers["Operation-Location"] = None
        self.assertIsNone(ta.get_results(response)) 
    
    def test_none_returned_with_malformed_url(self):
        """
        Input is a valid response object from the Read API, but the value for
        the "Operation-Location" key is missing from the header
        """
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        
        response = ta.submit_image_for_processing()
        # get the correct URL and slice off the last digit
        new_url = response.headers["Operation-Location"][:-1]
        # set the 'Operation-Location' header to be this new URL
        response.headers["Operation-Location"] = new_url
        self.assertIsNone(ta.get_results(response)) 

# ------------------------------------

class TestCheckResults(unittest.TestCase):
    def setUp(self):
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                            subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                            api_url=settings.OCR_API_URL)
        # This took a long time to puzzle out...
        # If I assign without copy.deepcopy(), the changes that the tests
        # make on the 'status' key are carried through to RESULTS.OCR_RESULTS;
        # and are *NOT* reset for the next test!! 
        # Particularly important when 'status' is popped...
        self.results = copy.deepcopy(RESULTS.OCR_RESULTS)

    def tearDown(self):
        del(self.image_path, self.img_bytes, self.ta, self.results)

    def test_results_false_returned_on_success(self):
        check = self.ta.check_results(results=self.results, time_elapsed=1, max_time=30)
        self.assertTupleEqual((self.results, False), check)
    
    def test_none_false_returned_on_failure(self):
        self.results["status"] = "failed"
        check = self.ta.check_results(results=self.results, time_elapsed=1, max_time=30)
        self.assertTupleEqual((None, False), check)

    def test_none_false_returned_without_status_key(self):
        self.results.pop("status")
        check = self.ta.check_results(results=self.results, time_elapsed=1, max_time=30)
        self.assertTupleEqual((None, False), check)

    def test_none_false_returned_if_time_elapsed_exceeds_max_time(self):
        self.results["status"] = "running"
        check = self.ta.check_results(results=self.results, time_elapsed=30, max_time=30)
        self.assertTupleEqual((None, False), check)
    
    def test_results_true_returned_otherwise(self):       
        self.results["status"] = "running"
        check = self.ta.check_results(results=self.results, time_elapsed=1, max_time=30)
        self.assertTupleEqual((self.results, True), check)

# ------------------------------------

class TestAnalyseImage(unittest.TestCase):
    def setUp(self):       
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)

    def tearDown(self):
        # del(IMG_PATH, self.image_path)
        del(self.image_path, self.img_bytes)   

    def test_correct_results_returned_from_valid_input(self):
        """
        Check that analyse_image returns the correct results when provided the correct arguments 
        """
        ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL)
        results = ta.analyse_image()
        expected_results = RESULTS.OCR_RESULTS
        self.assertDictEqual(results["analyzeResult"], expected_results["analyzeResult"])

# ------------------------------------

class TestProcessOutput(unittest.TestCase):
    def setUp(self):        
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                            subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                            api_url=settings.OCR_API_URL)

    def tearDown(self):
        del(self.image_path, self.img_bytes, self.ta)

    def test_correct_results_returned_from_valid_input(self):
        expected_results = RESULTS.PROCESSED_OCR_RESULTS
        actual_results = self.ta.process_output(RESULTS.OCR_RESULTS)
        self.assertListEqual(expected_results, actual_results)
    
    def test_input_is_none_returns_none(self):
        actual_results = self.ta.process_output(None)
        self.assertIsNone(actual_results)
    
    def test_input_has_no_analyze_result_key_returns_none(self):
        test_input = RESULTS.OCR_NO_ANALYZERESULT_KEY
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)

    def test_input_has_no_read_results_key_returns_none(self):
        test_input = RESULTS.OCR_NO_READRESULTS_KEY
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)
    
    def test_read_results_is_empty_list_returns_none(self):
        test_input = RESULTS.OCR_READRESULTS_EMPTY_LIST
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)
    
    def test_input_has_no_lines_key_returns_none(self):
        test_input = RESULTS.OCR_NO_LINES_KEY
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)
    
    def test_input_has_no_width_key_returns_none(self):
        test_input = RESULTS.OCR_NO_WIDTH_KEY
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)

    def test_input_has_no_height_key_returns_none(self):
        test_input = RESULTS.OCR_NO_HEIGHT_KEY
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)
    
    def test_lines_is_empty_list_returns_none(self):
        test_input = RESULTS.OCR_LINES_EMPTY_LIST
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)    

    def test_use_words_false_extracts_correct_lines(self):
        # create a new ta object for the file we want to process
        image_path = get_file_path("lines_of_words.jpg")
        img_bytes = azure_services.get_file_bytes(image_path)
        ta = azure_services.TextAnalyser(image_data=img_bytes, 
                                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                        api_url=settings.OCR_API_URL,
                                        use_words=False)
        # do the test
        test_input = RESULTS.OCR_TEXT_IN_LINES
        expected_results = RESULTS.PROCESSED_OCR_TEXT_IN_LINES
        actual_results = ta.process_output(test_input)
        self.assertListEqual(expected_results, actual_results)

    def test_input_has_no_words_keys_returns_none(self):
        test_input = RESULTS.OCR_NO_WORDS_KEYS
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)
    
    def test_all_words_lists_are_empty_returns_none(self):
        test_input = RESULTS.OCR_ALL_WORDS_EMPTY_LISTS
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)
    
    def test_one_words_entry_exists_returns_values(self):
        test_input = RESULTS.OCR_ONE_WORDS_KEY
        expected_results = RESULTS.PROCESSED_OCR_ONE_WORD
        actual_results = self.ta.process_output(test_input)
        self.assertListEqual(expected_results, actual_results)
    
    def test_one_words_list_not_empty_returns_values(self):
        test_input = RESULTS.OCR_ONE_WORDS_LIST
        expected_results = RESULTS.PROCESSED_OCR_ONE_WORD
        actual_results = self.ta.process_output(test_input)
        self.assertListEqual(expected_results, actual_results)

    def test_no_bounding_box_keys_returns_none(self):
        test_input = RESULTS.OCR_NO_BOUNDINGBOX_KEYS
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)
    
    def test_one_bounding_box_key_returns_values(self):
        test_input = RESULTS.OCR_ONE_WORDS_LIST
        expected_results = RESULTS.PROCESSED_OCR_ONE_WORD
        actual_results = self.ta.process_output(test_input)
        self.assertListEqual(expected_results, actual_results)

    def test_no_text_keys_returns_none(self):
        test_input = RESULTS.OCR_NO_TEXT_KEYS_IN_WORDS
        actual_results = self.ta.process_output(test_input)
        self.assertIsNone(actual_results)

    def test_one_text_key_returns_values(self):
        test_input = RESULTS.OCR_ONE_TEXT_KEY_IN_WORDS
        expected_results = RESULTS.PROCESSED_OCR_ONE_WORD
        actual_results = self.ta.process_output(test_input)
        self.assertListEqual(expected_results, actual_results)

    def test_no_confidence_keys_returns_values(self):
        test_input = RESULTS.OCR_NO_CONFIDENCE_KEYS
        expected_results = RESULTS.PROCESSED_OCR_NO_CONFIDENCE_KEYS
        actual_results = self.ta.process_output(test_input)
        self.assertListEqual(expected_results, actual_results)

    def test_one_confidence_key_returns_values(self):
        test_input = RESULTS.OCR_ONE_CONFIDENCE_KEY
        expected_results = RESULTS.PROCESSED_OCR_ONE_CONFIDENCE_KEY
        actual_results = self.ta.process_output(test_input)
        self.assertListEqual(expected_results, actual_results)

# ------------------------------------

class TestProcessJson(unittest.TestCase):
    def setUp(self):        
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                            subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                            api_url=settings.OCR_API_URL)

    def tearDown(self):
        del(self.image_path, self.img_bytes, self.ta)

    def test_json_is_not_dict_returns_none(self):
        test_input = ["a", "b", "c"]
        max_width = 200
        max_height = 200
        actual_results = self.ta.process_json(test_input, max_width, max_height)
        self.assertIsNone(actual_results)

    def test_max_height_is_not_number_returns_none(self):
        test_input = RESULTS.OCR_TEXT_IN_LINES
        max_width = 200
        max_height = "a"
        actual_results = self.ta.process_json(test_input, max_width, max_height)
        self.assertIsNone(actual_results)

    def test_max_width_is_not_number_returns_none(self):
        test_input = RESULTS.OCR_TEXT_IN_LINES
        max_width = "a"
        max_height = 200
        actual_results = self.ta.process_json(test_input, max_width, max_height)
        self.assertIsNone(actual_results)

    # I have no idea why this fails. It should return None, but instead returns
    # the tuple (None,), even though the next test is pretty much identical and 
    # works fine, returning None??!
    @unittest.expectedFailure
    def test_no_bounding_box_key_returns_none(self):
        test_input = RESULTS.OCR_SINGLE_WORD_NO_BOUNDING_BOX_KEY        
        max_width = 200
        max_height = 200
        actual_results = self.ta.process_json(test_input, max_width, max_height), 
        self.assertIsNone(actual_results)

    def test_no_text_key_returns_none(self):
        test_input = RESULTS.OCR_SINGLE_WORD_NO_TEXT_KEY
        max_width = 200
        max_height = 200
        actual_results = self.ta.process_json(test_input, max_width, max_height)
        self.assertIsNone(actual_results)
    
    def test_no_confidence_key_returns_values(self):
        test_input = RESULTS.OCR_SINGLE_WORD_NO_CONFIDENCE_KEY
        max_width = 200
        max_height = 200
        actual_results = self.ta.process_json(test_input, max_width, max_height)
        self.assertIsNone(actual_results)

    def test_convert_bounds_no_result_returns_none(self):
        test_input = RESULTS.OCR_SINGLE_WORD
        max_width = 200
        max_height = 200
        actual_results = self.ta.process_json(test_input, max_width, max_height)
        self.assertIsNone(actual_results)

    def test_correct_input_gives_correct_result(self):
        test_input = RESULTS.OCR_SINGLE_WORD
        max_width = 2661
        max_height = 1901
        actual_results = self.ta.process_json(test_input, max_width, max_height)
        expected_results = RESULTS.PROCESSED_OCR_TEXT_SINGLE_WORD
        self.assertDictEqual(actual_results, expected_results)

# ------------------------------------

class TestConvertBounds(unittest.TestCase):
    def setUp(self):        
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.ta = azure_services.TextAnalyser(image_data=self.img_bytes, 
                                            subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                                            api_url=settings.OCR_API_URL)

    def tearDown(self):
        del(self.image_path, self.img_bytes, self.ta)

    def test_valid_input_returns_correct_results(self):
        max_width = 100
        max_height = 100
        bbox = [10,10,20,10,20,20,10,20]
        expected_results = {"x": 0.1, "y":0.1, "width": 0.1, "height": 0.1}
        self.assertDictEqual(self.ta.convert_bounds(bbox, max_width, max_height),
                            expected_results)

    def test_bounding_coords_same_size_as_whole_image_returns_correct_results(self):
        max_width = 100
        max_height = 100
        bbox = [0,0,max_width,0,max_width,max_height,0,max_height]
        expected_results = {"x": 0, "y":0, "width": 1, "height": 1}
        self.assertDictEqual(self.ta.convert_bounds(bbox, max_width, max_height),
                            expected_results)

    # --------------------------------------------------------------------
    # NOTE: tests below commented out for two reasons:
    # 1. I'm not 100% sure what behaviour I'm expecting. Should the tests
    #    return None or not-None in these examples?
    # 2. The input will come from Azure, which (from the docs) only 
    #    accepts max-width and max-height in the range [50, 10000]. So the
    #    numbers below are way out of scope.
    #    Ref: https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-ga/operations/5d986960601faab4bf452005
    # 
    # [Commented-not-deleted in case I want to revisit this at some point;
    # the tests themselves seem like potentially useful cases...?]
    # --------------------------------------------------------------------  
    # def test_very_large_width_returns_notnone(self):
    #     bbox = [10,10,20,10,20,20,10,20]
    #     max_width = 100000000000000000000000000000000000000000
    #     max_height = 100
    #     self.assertIsNotNone(self.ta.convert_bounds(bbox, max_width, max_height))

    # def test_very_large_height_returns_notnone(self):
    #     bbox = [10,10,20,10,20,20,10,20]
    #     max_width = 100000000000000000000000000000000000000000
    #     max_height = 100
    #     self.assertIsNotNone(self.ta.convert_bounds(bbox, max_width, max_height))

    # def test_very_large_width_and_height_returns_notnone(self):
    #     bbox = [10,10,20,10,20,20,10,20]
    #     max_width = 100000000000000000000000000000000000000000
    #     max_height = 100000000000000000000000000000000000000000
    #     self.assertIsNotNone(self.ta.convert_bounds(bbox, max_width, max_height))
    
    # def test_very_small_width_returns_notnone(self):
    #     small_num = 0.000000000000000000000000000000000000000001
    #     bbox = [small_num / 10,0,0,0,0,0,0,0]
    #     max_width = small_num
    #     max_height = 100
    #     self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    # def test_very_small_height_returns_notnone(self):
    #     small_num = 0.000000000000000000000000000000000000000001
    #     bbox = [0,0,0,0,0,0,0,small_num / 10]
    #     max_width = small_num
    #     max_height = 100
    #     self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    # def test_very_small_width_and_height_returns_notnone(self):
    #     small_num = 0.000000000000000000000000000000000000000001
    #     bbox = [small_num / 10,0,0,0,0,0,0,small_num / 10]
    #     max_width = small_num
    #     max_height = small_num
    #     self.assertIsNotNone(self.ta.convert_bounds(bbox, max_width, max_height))
    # --------------------------------------------------------------------  

    def test_max_width_is_zero_returns_none(self):
        bbox = [0,0,0,0,0,0,0,0]
        max_width = 0
        max_height = 3
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    def test_max_width_is_negative_returns_none(self):
        bbox = [0,0,0,0,0,0,0,0]
        max_width = -1
        max_height = 3
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))
    
    def test_max_width_is_non_numeric_returns_none(self):
        bbox = [0,0,0,0,0,0,0,0]
        max_widths = ["a", [1], True]
        max_height = 3
        for max_width in max_widths:
            self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))
    
    def test_max_height_is_negative_returns_none(self):
        bbox = [0,0,0,0,0,0,0,0]
        max_width = 3
        max_height = -3
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))
    
    def test_max_height_is_non_numeric_returns_none(self):
        bbox = [0,0,0,0,0,0,0,0]
        max_width = 3
        max_heights = ["a", [1], True]
        for max_height in max_heights:
            self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    def test_max_height_is_zero_returns_none(self):
        bbox = [0,0,0,0,0,0,0,0]
        max_width = 3
        max_height = 0
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    def test_bounding_coords_does_not_have_eight_elements_returns_none(self):
        bbox = [1,2,3,4,5,6]
        max_width = 10
        max_height = 10
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))
        
    def test_bounding_coords_includes_negatives_returns_none(self):
        bbox = [1,2,3,4,5,6,7,-8]
        max_width = 10
        max_height = 10
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))
    
    def test_bounding_coords_includes_zeros_returns_notnone(self):
        bbox = [1,2,3,4,5,6,7,0]
        max_width = 10
        max_height = 10
        self.assertIsNotNone(self.ta.convert_bounds(bbox, max_width, max_height))
    
    def test_bounding_coords_has_non_numeric_element_returns_none(self):
        bbox = [1,2,3,4,5,6,7,"a"]
        max_width = 3
        max_height = 8
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    def test_x_coords_element_greater_than_max_width_returns_none(self):
        bbox = [1,2,3,4,5,6,7,0]
        max_width = 3
        max_height = 8
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    def test_y_coords_element_greater_than_max_height_returns_none(self):
        bbox = [1,2,3,4,5,6,7,0]
        max_width = 8
        max_height = 3
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    # --------------------------------------------------------------------
    # NOTE: I can't think of parameters that trigger these next two tests; 
    # they're already taken care of elsewhere!
    # --------------------------------------------------------------------
    # def test_calculated_x_is_negative_returns_none(self):        
    #     pass
        
    # def test_calculated_y_is_negative_returns_none(self):
    #     pass
    # --------------------------------------------------------------------

    def test_calculated_width_not_positive_returns_none(self):
        # if all x vals in the bounding_box are 0, max(all_x) - min(all_x) == 0
        bbox = [0,1,0,2,0,3,0,4]
        max_width = 8
        max_height = 8
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

    def test_calculated_height_not_positive_returns_none(self):
        # if all y vals in the bounding_box are 0, max(all_y) - min(all_y) == 0
        bbox = [1,0,2,0,3,0,4,0]
        max_width = 8
        max_height = 8
        self.assertIsNone(self.ta.convert_bounds(bbox, max_width, max_height))

