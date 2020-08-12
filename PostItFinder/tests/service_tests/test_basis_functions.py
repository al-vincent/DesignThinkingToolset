from PostItFinder import azure_services
import unittest
import os
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
        self.bf = azure_services.BasisFunctions()

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
        encoded_bytes = self.bf.get_image_data(img_str) 
        self.assertTrue(isinstance(encoded_bytes, bytes))

        # finally, make sure that the bytes returned are correct by comparing the output of the 
        # function to the output of file.read() as binary
        self.assertEqual(img_bytes, encoded_bytes)
    
    def test_non_b64_encoded_str_returns_none(self):
        random_str = "Hello world"
        encoded_bytes = self.bf.get_image_data(random_str)
        self.assertIsNone(encoded_bytes)
    
    def test_incomplete_b64_encoded_str_returns_none(self):
        """
        NOTE: this test is slightly rigged, in that it slices off 5 characters from 
        the end of the input string. HOWEVER, if the number of characters sliced off
        is a multiple of 4 then None *WILL NOT* be returned.
        """
        with open(self.image_path, "rb") as f:
            img_str = base64.b64encode(f.read()).decode("utf-8")
        self.assertIsNone(self.bf.get_image_data(img_str[:-5]))

    def test_bytestream_input_is_returned_unchanged(self):
        # first run the test with image bytes as the input
        with open(self.image_path, "rb") as f:
            img_bytes = f.read()
        self.assertEqual(img_bytes, self.bf.get_image_data(img_bytes))

        # now rerun with text bytes as input
        with open(get_file_path("test_file.txt"), "rb") as f:
            txt_bytes = f.read()
        self.assertEqual(txt_bytes, self.bf.get_image_data(txt_bytes))

    def test_non_str_or_bytes_input_returns_none(self):
        # provide a range of data types
        for input in [1, {"a": 123, "b": 456}, ["a", "b", "c"], None]:
            self.assertIsNone(self.bf.get_image_data(input))
    
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
    #     self.assertIsNone(self.bf.get_image_data(txt_str))

# ------------------------------------

class TestImageDataIsValid(unittest.TestCase):
    def setUp(self):      
        self.image_path = get_file_path("test_jpg.jpg")
        self.img_bytes = azure_services.get_file_bytes(self.image_path)
        self.bf = azure_services.BasisFunctions()

    def tearDown(self):
        pass

    def test_acceptable_image_validates_correctly(self):
        with open(self.image_path, "rb") as f:
            img_bytes = f.read()
    
        self.assertTrue(self.bf.image_data_is_valid(img_bytes))

    def test_too_large_image_is_invalid(self):
        with open(get_file_path("test_gif.gif"), "rb") as f:
            img_bytes = f.read()

        self.assertFalse(self.bf.image_data_is_valid(img_bytes))

    def test_non_image_is_invalid(self):
        with open(get_file_path("test_file.txt"), "rb") as f:
            img_bytes = f.read()

        self.assertFalse(self.bf.image_data_is_valid(img_bytes))
    
    def test_wrong_image_type_is_invalid(self):
        with open(get_file_path("test_tif.tif"), "rb") as f:
            img_bytes = f.read()

        self.assertFalse(self.bf.image_data_is_valid(img_bytes))

    # ...Anything else??!

