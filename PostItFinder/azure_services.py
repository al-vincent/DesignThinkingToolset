import http.client, urllib.request, urllib.parse, urllib.error
from json import load, loads
import os

class ObjectDetector:
    def __init__(self, base_url, image_data, prediction_key, subscription_key, 
                project_id, published_name, confidence_threshold):
        self.base_url = base_url
        self.image_data = image_data
        self.prediction_key = prediction_key
        self.subscription_key = subscription_key
        self.project_id = project_id
        self.published_name = published_name
        self.confidence_threshold = confidence_threshold

    def analyse_image(self):
        """
        Access the Azure Custom Vision service to process an image.

        Returns:
            - JSON-style dict containing the results of the analysis (e.g. bounding
            box coordinates of images detected, name of the tag detected, 
            probability of correct detection etc.)
        """

        headers = {
            # Request headers
            'Prediction-Key': self.prediction_key,
            'Content-Type': 'application/octet-stream',
            'Prediction-key': self.subscription_key
        }

        try:
            conn = http.client.HTTPSConnection(self.base_url)
            conn.request("POST", f"/customvision/v3.0/Prediction/{self.project_id}/detect/iterations/{self.published_name}/image", self.image_data, headers)
            data = conn.getresponse().read()
            conn.close()
            results = loads(data.decode("utf-8"))
            if "predictions" in results:
                return results
            else:
                print(f"*** ERROR, analyse_image,  unexpected return: {results}")
                return None
        except Exception as err:
            print(f"*** ERROR: analyse_image, {err} ***")
            return None
    
    def process_output(self, azure_results):
        regions = azure_results.get("predictions", None)
        if regions is not None:
            results = []
            for region in regions:
                if region["probability"] >= self.confidence_threshold:
                    results.append({
                        "x": region["boundingBox"]["left"],
                        "y": region["boundingBox"]["top"],
                        "width": region["boundingBox"]["width"],
                        "height": region["boundingBox"]["height"]
                    })
            
            return {"threshold": self.confidence_threshold, "data": results}
        else:
            print("***** ERROR: ObjectDetector.process_output, no data returned *****")
            {"threshold": self.confidence_threshold, "data": None}


def get_image_bytes(image_path):
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

def run_image_analysis(image_bytes):
    """
    Example runner for the function 
    """
    with open("C:/Users/al_vi/OneDrive/Code/DesignThinkingToolset/static/PostItFinder/js/config.json", "r") as f:
        CONFIG = load(f)        
        OBJ_DET = CONFIG["CONSTANTS"]["AZURE"]["OBJ_DET"]

    # Azure Custom Vision parameters
    BASE_URL = OBJ_DET["BASE_URL"]
    PREDICTION_KEY = os.environ.get(OBJ_DET["PREDICTION_KEY"]) 
    SUBSCRIPTION_KEY = os.environ.get(OBJ_DET["SUBSCRIPTION_KEY"])
    PROJECT_ID = os.environ.get(OBJ_DET["PROJECT_ID"]) 
    PUBLISHED_NAME = os.environ.get(OBJ_DET["PUBLISHED_NAME"])

    obj_det = ObjectDetector(base_url=BASE_URL,
                             data=image_bytes,
                             prediction_key=PREDICTION_KEY,
                             subscription_key=SUBSCRIPTION_KEY,
                             project_id=PROJECT_ID,
                             published_name=PUBLISHED_NAME)

    image_data = obj_det.analyse_image()
    
    return image_data

def main():
    IMAGE_PATH = "C:/Users/al_vi/OneDrive/Pictures/PostIts/persona.jpg"
    image_bytes = get_image_bytes(IMAGE_PATH)

    output = run_image_analysis(image_bytes)
    print(output)

if __name__ == "__main__":
    main()
