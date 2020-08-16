from django.conf import settings

from json import load
import os
import base64
import imghdr
from sys import getsizeof
import logging
import requests
from requests.exceptions import HTTPError
import time

# Get a logger instance
logger = logging.getLogger(__name__)

# ================================================================================================
# BASE CLASS
# ================================================================================================
class BasisFunctions:
    def __init__(self, max_image_size=4194304, ok_image_types=['jpeg', 'bmp', 'png']):
        self.MAX_IMAGE_SIZE = max_image_size if max_image_size is not None else settings.MAX_IMAGE_SIZE
        self.OK_IMAGE_TYPES = ok_image_types if ok_image_types is not None else settings.OK_IMAGE_TYPES
        
    def get_image_data(self, input_data):
        """
        Convert a string encoded as base64 into bytes. 

        Parameters:
            input_data (str or bytes); a string of base64-encoded data, or bytes.
        
        Returns:
            bytes representing the binary form of the input, or None.
        """
        
        data_bytes = None
        if isinstance(input_data, str):
            try:
                data_bytes = base64.decodebytes(input_data.encode("utf-8"))
            except base64.binascii.Error as err:
                logger.error(f"binascii.Error; str is not a valid base64 encoding. Sys error: '{err}'.")
            except base64.binascii.Incomplete as err:
                logger.error(f"binascii.Incomplete; str is incomplete. Sys error: '{err}'.")
            except Exception as err:
                logger.error(f"Another error occurred: {err}")
        elif isinstance(input_data, bytes):
            data_bytes = input_data
        else:
            logger.error(f"Input data is of type {type(input_data)}. Should be of type str or bytes.")
        
        return data_bytes

    def image_data_is_valid(self, bytestream):
        """
        Check whether a bytestream is valid; i.e. is an image, is either a jpeg, 
        gif, bmp or png, and is of size <= 4MB.

        Parameters:
        - bytestream (bytes), the data to be checked.

        Returns:
        - boolean, True if the data is valid and false if not.
        """              
        result = False

        # check if bytestream is <= 4MB
        if getsizeof(bytestream) > self.MAX_IMAGE_SIZE:
            logger.error(f"Image size is {getsizeof(bytestream)}, outside permitted bounds")
        else:
            img_type = imghdr.what("", bytestream)
            # check whether the bytestream is an image            
            if img_type is not None:
                # check whether the bytestream is of an acceptable type
                if img_type not in self.OK_IMAGE_TYPES:                    
                    logger.error(f"Image is of type {img_type}, which is not in {self.OK_IMAGE_TYPES}")
                else:
                    result = True
            else:
                logger.error(f"Bytestream provided is not an image.")

        return result

# ================================================================================================
# AZURE OBJECT DETECTION
# ================================================================================================
class ObjectDetector(BasisFunctions):
    def __init__(self, image_data, prediction_key, obj_det_url, confidence_threshold=0.3):
        super().__init__()
        self.image_data = self.get_image_data(image_data)    
        self.confidence_threshold = confidence_threshold    
        self.prediction_key = prediction_key
        self.obj_det_url = obj_det_url

    def analyse_image(self, image_data=None):
        """
        Access the Azure Custom Vision service to process an image.

        Returns:
            Dict containing the results of the analysis, or None
        
        NOTE: if results are a dict, the format will be as defined in the Custom Vision API:
        https://southcentralus.dev.cognitive.microsoft.com/docs/services/Custom_Vision_Prediction_3.1/operations/5eb37d24548b571998fde5f3
        """

        # Allow the object's
        if image_data is None:
            image_data = self.image_data

        headers = {
            # Request headers
            'Prediction-Key': self.prediction_key,
            'Content-Type': 'application/octet-stream',
        }

        try:
            response = requests.post(self.obj_det_url, headers=headers, data=image_data)
            response.raise_for_status()
        except Exception as err:
            logger.error(f"Exception raised; sys error message: {err}")
            return None
        
        results = response.json()
        if "predictions" in results:
            return results
        else:
            logger.error(f"Unexpected Azure return, contains no 'predictions' key. Return provided: {results}")
            return None
    
    def process_output(self, azure_results):
        """
        Processor to convert Azure object detection output into a format that is useful 
        for SNIP. 
        
        Parameters:
            azure_results (dict or None); the data returned by Azure Custom Vision object
                detection. Dict if Custom Vision returned results; None if there was an 
                error or no objects were detected in the image.
        
        Returns:
            dict, either of the form:
                {"threshold": (float), 
                "data":[{"x": (float), "y": (float), }, "width": (float), "height": (float)}, 
                        {"x": ..., "y": ..., "width": ..., "height": ... }, etc. ] }, 
            or    
                {"threshold": (float), "data": None}
            
            The first format is used if the Azure return contains legitimate results; the 
            second format is used if no results are provided or if the results are in an
            incorrect format.
        """
        try:
            regions = azure_results.get("predictions", None)
        except AttributeError as err:
            logger.error(f"Azure return contains no predictions. Sys error message: {err}")
            regions = None

        results = []
        if regions is not None:
            for region in regions:
                if all(key in region for key in ("probability", "boundingBox")):
                    if region["probability"] >= self.confidence_threshold:
                        try:
                            results.append({
                                "x": region["boundingBox"]["left"],
                                "y": region["boundingBox"]["top"],
                                "width": region["boundingBox"]["width"],
                                "height": region["boundingBox"]["height"]
                            })
                        except Exception as err:
                            logger.warning(f"An exception occurred; region={region}, error={err}")
                else:
                    logger.error(f"Input data does not contain required keys")        

        # The ternary operator below is using the truthiness of a list to return results
        # iff it's a non-empty list; else return None
        return {"threshold": self.confidence_threshold, "data": results if results else None}
    
    def analyse_and_process(self):
        """
        Convenience function to analyse and process the image data.

        Returns the output from process_output()
        """
        sticky_notes = None
        if self.image_data is not None:
            if self.image_data_is_valid(self.image_data):
                logger.info(f"Object Detection request uses valid image data")
                sticky_notes = self.analyse_image()

                if sticky_notes is not None:                
                    logger.info(f"Received response from Azure")
                else:
                    logger.error(f"Azure did not process image successfully")
            else:
                logger.error(f"AJAX POST request uses invalid bytestream")
        else:
            logger.error(f"No image data received from client")

        return self.process_output(sticky_notes)


# ================================================================================================
# AZURE TEXT ANALYSIS
# ================================================================================================
class TextAnalyser(BasisFunctions):
    # Documentation: 
    # https://westcentralus.dev.cognitive.microsoft.com/docs/services/computer-vision-v3-ga/operations/5d9869604be85dee480c8750
    # Example:
    # https://docs.microsoft.com/en-gb/azure/cognitive-services/computer-vision/quickstarts/python-hand-text
    def __init__(self, image_data, subscription_key, api_url, use_words=True):
        super().__init__()
        self.image_data = self.get_image_data(image_data)    
        self.subscription_key = subscription_key
        self.api_url = api_url
        self.headers = {"Ocp-Apim-Subscription-Key": self.subscription_key,
                        "Content-Type": "application/octet-stream"}
        self.use_words = use_words
    
    def submit_image_for_processing(self):
        """
        Use the Azure Computer Vision service to find text in an image bytestream.
        
        Returns: 
            - response object from requests library POST, or None.
            None is returned if an error is encountered.
        """ 

        try:
            response = requests.post(self.api_url, headers=self.headers, data=self.image_data)
            # raise_for_status will raise an exception if the response is unsuccessful
            response.raise_for_status()
        except HTTPError as err:
            logger.error(f"An HTTP error occurred while submitting the image for processing. Sys error: {err}")
            return None
        except Exception as err:
            logger.error(f"Another error occurred while submitting the image for processing. Sys error: {err}")
            return None
        else:
            logger.info("Image successfully submitted for processing.")
            return response

    def get_results(self, response):
        # The recognized text isn't immediately available, so poll to wait 
        # for completion.
        results = {}
        poll = True
        time_elapsed = 0
        while(poll):
            try:
                response_final = requests.get(response.headers["Operation-Location"], 
                                            headers=self.headers)
                response_final.raise_for_status()
            except HTTPError as err:
                logger.error(f"HTTP error occurred while connecting to OCR URL. Sys error: {err}")
                return None
            except Exception as err:
                logger.error(f"Another error occured while connecting to OCR URL. Sys error: {err}")
                return None  

            results = response_final.json()
            time.sleep(1)
            time_elapsed += 1
            # check the status of the results 
            results, poll = self.check_results(results, time_elapsed)
        
        return results

    def check_results(self, results, time_elapsed, max_time=30):
        
        if "status" in results: 
            # In this case, we've got our results
            if results["status"] == "succeeded":
                logger.info("OCR results successfully returned from Azure.")
                return (results, False)
            # in this case, the analysis has completed but failed to work
            elif results["status"] == "failed":
                logger.warning("The Azure service failed to return any results.")
                return (None, False)
        else:
            logger.warning(f"Azure results missing expected key 'status': {results}")
            return (None, False)

        # in this case it's taken too long for the service to work, so exit
        if time_elapsed >= max_time:
            logger.warning("The Azure OCR service exceeded the max response time.")
            return (None, False)            

        # Otherwise, we're still waiting
        return (results, True)

    def analyse_image(self):
        response = self.submit_image_for_processing()
        if response is not None:
            return self.get_results(response)
        else:
            return None

    def process_output(self, azure_results):
        if azure_results is not None:
            # if any of these entries are missing, the analysis has failed; return None.
            try:
                results_pages = azure_results["analyzeResult"]["readResults"]
                # Key assumption - the [0] index below is a ref to the page analysed.
                # This is relevant for PDF docs, which can be multi-page; but not for
                # the images we're processing, which will only ever be one page long.
                results_page = results_pages[0]
                lines = results_page["lines"]
                width = results_page["width"]
                height = results_page["height"]
            except KeyError as k:
                logger.error(f"Azure OCR results do not contain the key {k}.")
                return None
            except IndexError as err:
                logger.error(f"Azure OCR readResults list is empty. Sys error: {err}")
                return None
            except Exception as err:
                logger.error(f"Another error occurred: {err}")
                return None

            # process the lines or words (depending on whether the user has provided
            # any regions)
            processed_results = []
            if len(lines) > 0:
                for line in lines:
                    # if we want to find individual words (e.g. because the user has
                    # selected some regions), take this path
                    if self.use_words:
                        if "words" in line:
                            for word in line["words"]:
                                # each word is run through process_json
                                word_info = self.process_json(word, width, height)
                                if word_info is not None:
                                    processed_results.append(word_info)
                        else:
                            logger.warning(f"Azure OCR results line does not contain any words.")
                    # otherwise, let Azure group words together into lines
                    else:
                        line_info = self.process_json(line, width, height)
                        if line_info is not None:
                            processed_results.append(line_info)
                    
                # At this point, processed_results could be an empty list. If so,
                # return None (we're not interested if there're no results).
                return {"data":processed_results} if processed_results else None
            # In this case, no actual OCR data (i.e. lines of text) have been returned
            else:
                return None
  
            # a couple of warnings to the server
            if len(results_pages) > 1:
                logger.warning(f"Azure OCR has returned {len(results_pages)} pages (one page expected)")
            try:
                if results_page["unit"] != "pixel":
                    logger.warning(f"Azure OCR is using an unexpected unit: {results_page['unit']}")
            except KeyError as k:
                logger.warning(f"Azure OCR results do not contain the key {k}.")
            except Exception as err:
                logger.warning(f"Another exception occured.")
        else:
            logger.warning("Input parameter azure_results is None")
            return None
    
    def process_json(self, json, max_width, max_height):
        try:
            bbox = json["boundingBox"]
            text = json["text"]
            confidence = json.get("confidence", None)                    
        # Handle any exceptions, returning None if required keys don't exist
        # (as there are no results )
        except KeyError as k:
            logger.warning(f"'json' does not contain the key {k}.")
            return None
        except TypeError as err:
            logger.warning(f"'json' is of type {type(json)}; should be dict.")
            return None
        except Exception as err:
            logger.warning(f"Another error occurred: {err}")
            return None
        
        w = self.convert_bounds(bbox, max_width, max_height) 
        if w is not None:
            # use word.get() for confidence, as it's nice-to-have for words
            # and doesn't apply to lines
            w.update({"text": text, "confidence": confidence})
            return w
        else:
            return None
        
    def convert_bounds(self, bounding_coords, max_width, max_height):
        """
        Convert a list of 8 numbers representing pairs of (x,y) coordinates for a
        bounding quadrilateral, to a dict which represents the bounds as a 
        rectangle. The coordinates are also converted from absolute values to 
        normalised values (i.e. in range [0,1], normalised by the width and height
        of the whole coordinate space).

        The rectangle returned will be 'flat' (i.e. no rotation), and will be 
        completely bound the quadrilateral, e.g. (in poor ASCII-art):
        -------
        |  /\ |
        | /  \|
        |/   /|
        |\  / |
        | \/  | 
        -------
        
        Parameters:
            - bounding_coords [list], a list of 8 numbers. The first two numbers
            represent the (x,y) coords of the top-left point of the bounding 
            quadrilateral; the next two are the (x,y) coords of the top-right point;
            the next two are the (x,y) coords of the bottom-right point; and the
            last two are the (x,y) coords of the bottom-left point.
            - max_width [int or float], the width of the whole canvas / image
            - max_height [int or float], the height of the whole canvas / image

        Returns: 
            - dict or None.
            If dict, will be of form {"x": <x-coord of top-left point>,
                                    "y": <y-coord of top-left point>,
                                    "width": <width of bounding box>,
                                    "height": <height of bounding box>}
        """
        # some initial error- / sanity-checking on the parameters
        try:
            assert len(bounding_coords) == 8, f"bounding_coords should have 8 elements; it has {len(bounding_coords)} elements"
            assert max_width > 0, f"max_width={max_width}, which is <= 0"
            assert max_height > 0, f"max_height={max_height}, which is <= 0"
            assert all(i >= 0 for i in bounding_coords), f"One of bounding_coords < 0: {bounding_coords}"            
        except AssertionError as err:
            logger.error(err)
            return None
        except TypeError as err:
            logger.error(err)
            return None
        except Exception as err:
            logger.error(err)
            return None

        try:
            all_x = [i for i in bounding_coords[::2]]
            all_y = [i for i in bounding_coords[1::2]]

            assert all(i <= max_width for i in all_x), f"Some of all_x > max_width; all_x: {all_x}, max_width: {max_width}"
            assert all(i <= max_height for i in all_y), f"Some of all_y > max_height; all_y: {all_y}, max_height: {max_height}"

            x = min(all_x) / max_width
            y = min(all_y) / max_height
            width = (max(all_x) - min(all_x)) / max_width
            height = (max(all_y) - min(all_y)) / max_height
        except AssertionError as err:
            logger.error(err)
            return None
        except TypeError as err:
            logger.error(err)
            return None
        except Exception as err:
            logger.error(err)
            return None

        # some sanity-checking on the output
        try:
            assert x >= 0, f"Calculated x <= 0, which is impossible; {x}"
            assert y >= 0, f"Calculated y <= 0, which is impossible; {y}"
            assert width > 0, f"Calculated width <= 0, which is impossible; {width}"
            assert height > 0, f"Calculated height <= 0, which is impossible; {height}"
        except AssertionError as err:
            logger.error(err)
            return None
        except Exception as err:
            logger.error(err)
            return None

        return {"x": x, "y": y, "width": width, "height": height}
    
    def analyse_and_process(self):
        """
        Convenience function to analyse and process the image data.

        Returns the output from process_words() or process_lines()
        """
        text = None
        if self.image_data is not None:
            if self.image_data_is_valid(self.image_data):
                logger.info(f"OCR request from client uses valid image data")
                text = self.analyse_image()

                if text is not None:                
                    logger.info(f"Received response from Azure")
                else:
                    logger.error(f"Azure did not process image successfully")
            else:
                logger.error(f"OCR request from client uses invalid bytestream")
        else:
            logger.error(f"No image data received from client")

        return self.process_output(text)

# ================================================================================================
# MATCHING WORDS TO REGIONS
# ================================================================================================
class MatchWordsToRegions:
    def __init__(self, region_data, word_data):
        self.regions = region_data
        self.words = word_data

    def match(self):
        # 1. Iterate through each region
        # 2. Get the words that are within the region:
        #    - if word.x, .y  >= region.x, .y, and word.width, .height <= region.width, .height then inside
        # 3. Order the words correctly into a single string:
        #    - bit tricky, due to lots boundary issues. However, find min(words.y) 
        #      and go from there...?
        # 4. Add the string to the region data, as an extra field ('text')
        # 5. At the end; each original region now has a 'text' field, with a string as
        #    the value

        for region in self.regions:
            words_in_region = self.get_words_in_region(region)
            sentence = self.order_words_into_sentence(words_in_region)
            region["text"] = sentence
        
        return self.regions
    
    def get_words_in_region(self, region):
        words = []
        for word in self.words:
            if (word["x"] >= region["x"] and 
                word["y"] >= region["y"] and
                word["x"] + word["width"] <= region["x"] + region["width"] and 
                word["y"]+ word["height"] <= region["y"] + region["height"]):
            
                words.append(word["text"])
        return words

    def order_words_into_sentence(self, words):
        # NOTE: below is a simple placeholder for a more complex ordering algorithm.
        # HOWEVER - is a more complex algorithm necessary?? E.g. if the Azure service
        # finds word entries from top-to-bottom and left-to-right automatically, then 
        # would the below suffice...?!
        # 
        # UPDATE: I don't think keeping it this simple is sensible, for what I want. 
        # From the docs, Azure *does* order top-bottom and left-right; but also
        # considers stuff like proximity in some cases. But would be easy to test.
        sentence = " ".join(word for word in words)
        # sentence = ""        
        # while 
        # first_word = None
        # for word in words:
        #     if first_word is None:
        #         first_word = word
        #     else:
        #         # word is *definitely* higher than first_word
        #         if word["y"] > first_word["y"] + first_word["height"]:
        #             first_word = word
        return sentence

# ================================================================================================
# HELPER FUNCTIONS
# ================================================================================================
def get_file_bytes(image_path):
    # Read the image into a byte array
    try:
        with open(image_path, "rb") as f:
            return f.read()
    except FileNotFoundError:
        print(f"*** ERROR: the file '{image_path}' was not found. ***")
        # exit(1)
        return None
    except Exception as err:
        print(f"*** ERROR: {err}")
        # exit(2)
        return None

# ================================================================================================
# DRIVER
# ================================================================================================
def main():
    # get the image data
    current_dir = os.path.dirname(os.path.abspath(__file__))    
    img_path = os.path.join(current_dir, "tests", "resources", "test_images", "lines_of_words.jpg")
    image_data = get_file_bytes(img_path)

    # --- OBJECT DETECTION ---
    prediction_key = os.environ.get("SNIP_OBJ_DET_PRED_KEY")
    project_id = os.environ.get("SNIP_OBJ_DET_PROJ_ID")
    published_name = os.environ.get("SNIP_OBJ_DET_PUB_NAME")
    api_url = f"https://snip-object-detection.cognitiveservices.azure.com/customvision/v3.0/Prediction/{project_id}/detect/iterations/{published_name}/image"

    aod = ObjectDetector(image_data=image_data, 
                        prediction_key=prediction_key,                       
                        obj_det_url=api_url)
    regions = aod.analyse_and_process()
    print(f"{'-'*24}\nObject Detection output:\n{'-'*24}\n{regions}\n")
    # --- /OBJECT DETECTION ---

    # --- TEXT ANALYSIS ---
    subscription_key = os.environ.get("SNIP_OCR_SUBS_KEY")
    api_url = "https://snip-ocr.cognitiveservices.azure.com/vision/v3.0/read/analyze"
    ta = TextAnalyser(image_data=image_data, 
                    subscription_key=subscription_key, 
                    api_url=api_url,
                    use_words=True)
    words = ta.analyse_and_process()
    print(f"{'-'*11}\nOCR output:\n{'-'*11}\n{words}\n")
    # --- /TEXT ANALYSIS ---

    # --- MATCH WORDS TO REGIONS ---
    mwtr = MatchWordsToRegions(regions["data"], words["data"])
    new_regions = mwtr.match()
    print(f"{'-'*19}\nRegions with words:\n{'-'*19}\n{new_regions}\n")
    # --- MATCH WORDS TO REGIONS ---

if __name__ == "__main__":
    main()
