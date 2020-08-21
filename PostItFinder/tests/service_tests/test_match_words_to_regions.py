import unittest
import os
from PostItFinder import azure_services
import PostItFinder.tests.resources.test_results.match_words_to_regions_results as RESULTS
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
class TestInputIsValid(unittest.TestCase):
    def test_worddata_is_empty_list_returns_false(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        word_data = []
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_worddata_is_none_returns_false(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        word_data = None
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_worddata_is_dict_returns_false(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        word_data = {
            "x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9
        }
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_worddata_is_list_of_lists_returns_false(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        word_data = [
            ["x", 0.51, "y", 0.31, "width", 0.2, "height", 0.2, "text", "hello", "confidence", 0.9],
            ["x", 0.52, "y", 0.6, "width", 0.2, "height", 0.05, "text", "world", "confidence", 0.9]
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_worddata_is_list_of_tuples_returns_false(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        word_data = [
            ("x", 0.51, "y", 0.31, "width", 0.2, "height", 0.2, "text", "hello", "confidence", 0.9),
            ("x", 0.52, "y", 0.6, "width", 0.2, "height", 0.05, "text", "world", "confidence", 0.9)
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_worddata_is_list_of_dicts_returns_true(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        word_data = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertTrue(actual_output)

    def test_regiondata_is_empty_list_returns_false(self):
        region_data = []
        word_data = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_regiondata_is_none_returns_false(self):
        region_data = None
        word_data = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)
    
    def test_regiondata_is_dict_returns_false(self):
        region_data = {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4}
        word_data = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_regiondata_is_list_of_lists_returns_false(self):
        region_data = [
            ["x", 0.5, "y", 0.3, "width", 0.3, "height", 0.4]
        ]
        word_data = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_regiondata_is_list_of_tuples_returns_false(self):
        region_data = [
            ("x", 0.5, "y", 0.3, "width", 0.3, "height", 0.4)
        ]
        word_data = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertFalse(actual_output)

    def test_regiondata_is_list_of_dicts_returns_true(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]

        word_data = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]

        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.input_is_valid()
        self.assertTrue(actual_output)

# ------------------------------------

class TestGetWordsInRegion(unittest.TestCase):
    def test_selfwords_is_empty_list_returns_none(self):
        # use legitimate regions for constructor
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4}
        ]
        words = []
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_selfwords_is_none_returns_none(self):
        # use legitimate regions for constructor
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4}
        ]
        words = None
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)
    
    def test_region_is_empty_dict_returns_none(self):
        # use legitimate regions, words for constructor
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4}
        ]
        words = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4, "text": "hello", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region({})
        self.assertIsNone(actual_output)

    def test_region_is_none_returns_none(self):
        # use legitimate regions, words for constructor
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4}
        ]
        words = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4, "text": "hello", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(None)
        self.assertIsNone(actual_output)

    def test_all_words_are_in_region_returns_all_words(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = ["hello", "world"]
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertListEqual(expected_output, actual_output)

    def test_some_words_are_in_region_returns_those_words(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # the second region is outside the region boundary
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.4, "y": 0.6, "width": 0.2, "height": 0.8, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = ["hello"]
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertListEqual(expected_output, actual_output)

    def test_no_words_are_in_region_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both regions are outside the region boundary
        words = [
            {"x": 0.41, "y": 0.21, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.4, "y": 0.2, "width": 0.2, "height": 0.8, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_no_words_contain_x_key_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_some_words_contain_x_key_returns_values(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = ["hello"]
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertListEqual(expected_output, actual_output)

    def test_no_words_contain_y_key_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_some_words_contain_y_key_returns_values(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = ["hello"]
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertListEqual(expected_output, actual_output)

    def test_no_words_contain_width_key_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_some_words_contain_width_key_returns_values(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = ["hello"]
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertListEqual(expected_output, actual_output)

    def test_no_words_contain_height_key_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_some_words_contain_height_key_returns_values(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = ["hello"]
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertListEqual(expected_output, actual_output)

    def test_no_words_contain_text_key_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)
    
    def test_some_words_contain_text_key_returns_values(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = ["hello"]
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertListEqual(expected_output, actual_output)

    def test_region_has_no_x_key_returns_none(self):
        regions = [
            {"y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_region_has_no_y_key_returns_none(self):
        regions = [
            {"x": 0.5, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_region_has_no_width_key_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "height": 0.4},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_region_has_no_height_key_returns_none(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3},
        ]
        # both words are inside the region boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

# ------------------------------------

class TestOrderWordsIntoSentence(unittest.TestCase):
    """
    The order_words_into_sentence() method is (currently) pretty trivial. This 
    is because of some of the tests below, which indicate that the default 
    Azure word ordering provides what we want.
    """
    def setUp(self):
        self.mwtr = azure_services.MatchWordsToRegions([], [])

    def tearDown(self):
        del(self.mwtr)
    
    def test_list_of_words_correctly_combined_into_sentence(self):
        words = ["hello", "world"]
        expected_output = "hello world"
        actual_output = self.mwtr.order_words_into_sentence(words)
        self.assertEqual(expected_output, actual_output)

    def test_words_is_not_list_returns_none(self):
        words = ("hello", "world")
        actual_output = self.mwtr.order_words_into_sentence(words)
        self.assertIsNone(actual_output)

    def test_words_is_empty_list_returns_none(self):
        words = []
        actual_output = self.mwtr.order_words_into_sentence(words)
        self.assertIsNone(actual_output)
    
    def test_words_is_none_returns_none(self):
        words = None
        actual_output = self.mwtr.order_words_into_sentence(words)
        self.assertIsNone(actual_output)

    def test_words_includes_non_str_returns_none(self):
        words = [1, "hello", True, {"a":1, "b":2}]
        actual_output = self.mwtr.order_words_into_sentence(words)
        self.assertIsNone(actual_output)

# ------------------------------------

class TestMatch(unittest.TestCase):
    def test_invalid_input_returns_none(self):
        region_data = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        word_data = []
        mwtr = azure_services.MatchWordsToRegions(region_data=region_data, 
                                                  word_data=word_data)
        actual_output = mwtr.match()
        self.assertIsNone(actual_output)

    def test_words_in_region_is_none_sets_text_none_for_all_regions(self):
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are outside the region boundaries
        words = [
            {"x": 0.41, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.42, "y": 0.6, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        actual_output = mwtr.get_words_in_region(regions[0])
        self.assertIsNone(actual_output)

    def test_words_in_region_is_none_sets_text_none_for_those_regions_only(self):
        """
        For two regions, test that if one region does contain text, but the other 
        doesn't, the 'text' key in one region will have the correct sentence as its
        value and the 'text' key in the other region will have a value of None.
        """
        regions = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4},
            {"x": 0.6, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the boundaries or region#1, but outside region#2
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.31, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = [
            {"x": 0.5, "y": 0.3, "width": 0.3, "height": 0.4, "text": "hello world"},
            {"x": 0.6, "y": 0.3, "width": 0.3, "height": 0.4, "text": None},
        ]
        actual_output = mwtr.match()
        self.assertListEqual(expected_output, actual_output)
    
    def test_words_in_region_is_none_sets_text_none_for_all_regions(self):
        """
        For two regions, test that if both regions don't contain text, then the 
        value for both 'text' keys is None
        """
        regions = [
            {"x": 0.6, "y": 0.3, "width": 0.3, "height": 0.4},
            {"x": 0.6, "y": 0.3, "width": 0.3, "height": 0.4},
        ]
        # both words are inside the  boundaries
        words = [
            {"x": 0.51, "y": 0.31, "width": 0.2, "height": 0.2, "text": "hello", "confidence": 0.9},
            {"x": 0.52, "y": 0.31, "width": 0.2, "height": 0.05, "text": "world", "confidence": 0.9}
        ]
        mwtr = azure_services.MatchWordsToRegions(regions, words)
        expected_output = [
            {"x": 0.6, "y": 0.3, "width": 0.3, "height": 0.4, "text": None},
            {"x": 0.6, "y": 0.3, "width": 0.3, "height": 0.4, "text": None},
        ]
        actual_output = mwtr.match()
        self.assertListEqual(expected_output, actual_output)

    # NOTE: these next four methods provide a fairly robust (I believe) test of 
    # correct behaviour for the match() method
    def file_checker(self, file):
        """
        Runner for the three tests below
        """
        mwtr = azure_services.MatchWordsToRegions(region_data=file["regions"]["data"], 
                                                    word_data=file["text"])
        new_regions = mwtr.match()
        self.assertListEqual(new_regions, file["expected_results"])
    
    def test_match_words_regions_1(self):
        self.file_checker(RESULTS.MATCH_WORDS_REGIONS_1)
    
    def test_match_words_regions_2(self):
        self.file_checker(RESULTS.MATCH_WORDS_REGIONS_2)
    
    def test_match_words_regions_3(self):
        self.file_checker(RESULTS.MATCH_WORDS_REGIONS_3)