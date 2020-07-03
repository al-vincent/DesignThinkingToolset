from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse

from PostItFinder.azure_services import ObjectDetector

import os
from json import load
import base64

# NOTE: can I replace these with the built-in static finders?
with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
    CONFIG = load(f)
    PATHS = CONFIG["PATHS"]
    HTML = CONFIG["HTML"]
    CONST = CONFIG["CONSTANTS"]

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
        data_b64 = request.POST.get("data", None) 
        if data_b64 is not None:
            # convert 'b64data' from a base64-encoded string to bytes
            data_bytes = base64.decodebytes(data_b64.encode('utf-8'))
            # send the bytes to the Azure object detection service for processing
            OBJ_DET = CONST["AZURE"]["OBJ_DET"]
            # obj_det = ObjectDetector(base_url=OBJ_DET["BASE_URL"],
            #                         data=data_bytes,
            #                         prediction_key=os.environ.get(OBJ_DET["PREDICTION_KEY"]),
            #                         subscription_key=os.environ.get(OBJ_DET["SUBSCRIPTION_KEY"]),
            #                         project_id=os.environ.get(OBJ_DET["PROJECT_ID"]),
            #                         published_name=os.environ.get(OBJ_DET["PUBLISHED_NAME"]))

            # send the object detection results back to the client for display
            # image_json = obj_det.analyse_image()
            # import time
            # time.sleep(3)
            # image_json = {
            #     "status": "SUCCESS",
            #     "param1": 1,
            #     "param2": True,
            #     "param3": [
            #         {"a": 4},
            #         {"b": 5},
            #         {"c": 6},
            #         {"d": 7}
            #     ]
            # }
            if image_json is not None:
                print(f"***** SENT JSON RESPONSE *****")
                return JsonResponse(image_json)
            else: 
                return JsonResponse({"status": "FAILED - no data was received from Azure"})
        else:
            return JsonResponse({"status": "FAILED - no data was sent from client"})
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
