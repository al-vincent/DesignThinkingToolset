from django.conf import settings

import http.client, urllib.request, urllib.parse, urllib.error
from json import load, loads
import os
import base64
import imghdr
from sys import getsizeof
import logging

# Get a logger instance
logger = logging.getLogger(__name__)

# ================================================================================================
# AZURE OBJECT DETECTION
# ================================================================================================
class ObjectDetector:
    def __init__(self, image_data, confidence_threshold=0.3, 
                prediction_key=None, base_url=None, obj_det_url=None, 
                max_image_size=4194304, ok_image_types=['jpeg', 'bmp', 'png', 'gif']):
        self.image_data = self.get_image_data(image_data)    
        self.confidence_threshold = confidence_threshold    
        self.PREDICTION_KEY = prediction_key if prediction_key is not None else settings.OBJ_DET_PREDICTION_KEY
        self.BASE_URL = base_url if base_url is not None else settings.OBJ_DET_BASE_URL
        self.OBJ_DET_URL = obj_det_url if obj_det_url is not None else settings.OBJ_DET_API_URL
        self.MAX_IMAGE_SIZE = max_image_size if max_image_size is not None else settings.DATA_UPLOAD_MAX_MEMORY_SIZE
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
            'Prediction-Key': self.PREDICTION_KEY,
            'Content-Type': 'application/octet-stream',
        }

        try:
            conn = http.client.HTTPSConnection(self.BASE_URL)
            conn.request("POST", self.OBJ_DET_URL, image_data, headers)
            data = conn.getresponse().read()
            conn.close()
            results = loads(data.decode("utf-8"))
            if "predictions" in results:
                return results
            else:
                logger.error(f"Unexpected Azure return, contains no 'predictions' key. Return provided: {results}")
                return None
        except Exception as err:
            logger.error(f"Exception raised; sys error message: {err}")
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
                        results.append({
                            "x": region["boundingBox"]["left"],
                            "y": region["boundingBox"]["top"],
                            "width": region["boundingBox"]["width"],
                            "height": region["boundingBox"]["height"]
                        })
                else:
                    logger.error(f"Input data does not contain required keys")        

        # The ternary operator below is using the truthiness of a list to return results
        # iff it's a non-empty list; else return None
        return {"threshold": self.confidence_threshold, "data": results if results else None}
    
    def analyse_and_process(self):
        """
        Convenience function to analyse and process the image data.
        """

        sticky_notes = None
        if self.image_data is not None:
            if self.image_data_is_valid(self.image_data):
                logger.info(f"AJAX POST request uses valid image data")
                sticky_notes = self.analyse_image()

                if sticky_notes is not None:                
                    logger.info(f"Receieved response from Azure")
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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proj_path = os.path.join(current_dir, os.pardir)
    config_path = os.path.join(proj_path, "static", 'PostItFinder', 'js', 'config.json')
    img_path = os.path.join(current_dir, "tests", "resources", "test_images", "test_jpg.jpg")

    with open(config_path, "r") as f:
        CONFIG = load(f)        
        OBJ_DET = CONFIG["CONSTANTS"]["AZURE"]["OBJ_DET"]

    prediction_key = os.environ.get("SNIP_OBJ_DET_PRED_KEY")
    project_id = os.environ.get("SNIP_OBJ_DET_PROJ_ID")
    published_name = os.environ.get("SNIP_OBJ_DET_PUB_NAME")
    base_url = "snip-object-detection.cognitiveservices.azure.com"
    api_url = f"/customvision/v3.0/Prediction/{project_id}/detect/iterations/{published_name}/image"

    image_data = get_file_bytes(img_path)
    aod = ObjectDetector(image_data=image_data, 
                        prediction_key=prediction_key,                       
                        base_url=base_url,
                        obj_det_url=api_url)
    output = aod.analyse_and_process()
    print(output)

if __name__ == "__main__":
    main()
