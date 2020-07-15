from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse

from PostItFinder.azure_services import ObjectDetector

import os
from json import load
import base64


# ================================================================================================
# GLOBALS
# ================================================================================================
with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
    CONFIG = load(f)
    PATHS = CONFIG["PATHS"]
    HTML = CONFIG["HTML"]
    CONST = CONFIG["CONSTANTS"]
NULL_RESULT = {"threshold": CONST["AZURE"]["OBJ_DET"]["CONFIDENCE_THRESHOLD"], "data": None}


# ================================================================================================
# HELPER FUNCTIONS
# ================================================================================================
def get_sticky_notes(image_data_b64):
    results = NULL_RESULT
    if image_data_b64 is not None:
        print("***** AJAX POST request includes image data *****")
        # convert 'b64data' from a base64-encoded string to bytes
        data_bytes = base64.decodebytes(image_data_b64.encode('utf-8'))
        # send the bytes to the Azure object detection service for analysis
        OBJ_DET = CONST["AZURE"]["OBJ_DET"]
        obj_det = ObjectDetector(base_url=OBJ_DET["BASE_URL"],
                                image_data=data_bytes,
                                prediction_key=os.environ.get(OBJ_DET["PREDICTION_KEY"]),
                                subscription_key=os.environ.get(OBJ_DET["SUBSCRIPTION_KEY"]),
                                project_id=os.environ.get(OBJ_DET["PROJECT_ID"]),
                                published_name=os.environ.get(OBJ_DET["PUBLISHED_NAME"]),
                                confidence_threshold=OBJ_DET["CONFIDENCE_THRESHOLD"])
        image_json = obj_det.analyse_image()

        # pass the results back to the view
        if image_json is not None:
            print(f"***** RECEIVED AZURE RESPONSE *****")
            results = obj_det.process_output(image_json)
        else: 
            print(f"***** AZURE DIDN'T ANALYSE IMAGE SUCCESSFULLY *****")
    else:
        print(f"***** NO IMAGE DATA RECEIVED FROM CLIENT *****")

    return results

# ================================================================================================
# ROUTES
# ================================================================================================
def index(request):

    context = {
        "title": HTML["HOME"]["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"],
        "home_content": "Home page",
        "start_btn": HTML["HOME"]["START_BTN"]
        }

    return render(request, PATHS["HOME"], context=context)

def about(request):
    context = {
        "title": HTML["ABOUT"]["TITLE"],
        "about_content": "some info about the app"
        }
    
    return render(request, PATHS["ABOUT"], context=context)

def faq(request):
    context = {
        "title": HTML["FAQ"]["TITLE"],
        "faq_content": "some frequently asked questions"
        }
    
    return render(request, PATHS["FAQ"], context=context)

def choose_image(request):
    # Update config to include the explanatory text for the home page
    HTML["CHOOSE_IMAGE"]["EXPLAIN_TEXT"]["ID"] = HTML["APP"]["EXPLAIN_TEXT"]["ID"]

    # Update config to set the 'active' class for the stepper bar
    for step in HTML["APP"]["STEPPER_BAR"]["ITEMS"]:
        if step["ID"] == "step1-id":
            step["CLASS"] = "active"
        else:
            step["CLASS"] = ""

    # Set ID for the 'next' button
    HTML["CHOOSE_IMAGE"]["NEXT_BTN"]["ID"] = HTML["APP"]["NEXT_BTN"]["ID"]

    context = {
        "title": HTML["CHOOSE_IMAGE"]["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"],
        "stepper": HTML["APP"]["STEPPER_BAR"],
        "explain_text": HTML["CHOOSE_IMAGE"]["EXPLAIN_TEXT"],
        "next_btn": HTML["CHOOSE_IMAGE"]["NEXT_BTN"],
        "choose_img_btn": HTML["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"],
        "image_pane": HTML["APP"]["IMAGE_PANE"],
        "config": CONFIG,
        }

    return render(request, PATHS["CHOOSE_IMAGE"], context=context)

def set_regions(request):

    if request.method == "POST" and request.is_ajax():
        image_data_b64 = request.POST.get("data", None)
        print(f"***** AJAX POST request received at server: {image_data_b64[0:20]}... *****")
        # processed_data = get_sticky_notes(IMAGE_DATA_B64)
        processed_data = get_sticky_notes(image_data_b64)
        if processed_data is not None:
            print(f"***** Processed data sent to client *****")
            return JsonResponse(processed_data, status=200)
        else:
            print(f"***** Null response sent to client *****")
            return JsonResponse(NULL_RESULT, status=400)
    else:
        # Update config to set the 'active' class for the stepper bar
        for step in HTML["APP"]["STEPPER_BAR"]["ITEMS"]:
            if step["ID"] == "step1-id" or step["ID"] == "step2-id":
                step["CLASS"] = "active"
            else:
                step["CLASS"] = ""

        # Set IDs for the 'next' and 'previous' buttons
        HTML["SET_REGIONS"]["PREVIOUS_BTN"]["ID"] = HTML["APP"]["PREVIOUS_BTN"]["ID"]
        HTML["SET_REGIONS"]["NEXT_BTN"]["ID"] = HTML["APP"]["NEXT_BTN"]["ID"]
        
        context = {
            "title": HTML["SET_REGIONS"]["TITLE"],
            "navbar": HTML["BASE"]["NAVBAR"],
            "stepper": HTML["APP"]["STEPPER_BAR"],
            "explain_text": HTML["SET_REGIONS"]["EXPLAIN_TEXT"],
            "find_rgns_btn": HTML["SET_REGIONS"]["FIND_REGIONS_BTN"],
            "add_rgn_btn": HTML["SET_REGIONS"]["ADD_REGION_BTN"],
            "next_btn": HTML["SET_REGIONS"]["NEXT_BTN"],
            "prev_btn": HTML["SET_REGIONS"]["PREVIOUS_BTN"],
            "image_pane": HTML["APP"]["IMAGE_PANE"],
            "config": CONFIG,
            }
            
        return render(request, PATHS["SET_REGIONS"], context=context)

def analyse_text(request):
    context = {
        "title": HTML["ANALYSE_TEXT"]["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"],
        "stepper": HTML["APP"]["STEPPER_BAR"],
        "explain_text": HTML["APP"]["EXPLAIN_TEXT"],
        "next_btn": HTML["APP"]["NEXT_BTN"],
        "prev_btn": HTML["APP"]["PREVIOUS_BTN"],
        "image_pane": HTML["APP"]["IMAGE_PANE"],
        "config": CONFIG,
        }

    return render(request, PATHS["ANALYSE_TEXT"], context=context)
    

