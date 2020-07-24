from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse

from PostItFinder.azure_services import ObjectDetector

import os
from json import load
import base64
import logging


# ================================================================================================
# GLOBALS
# ================================================================================================
with open(os.path.join(settings.STATIC, 'PostItFinder', 'js', 'config.json'), "r") as f:
    CONFIG = load(f)
    PATHS = CONFIG["PATHS"]
    HTML = CONFIG["HTML"]
    CONST = CONFIG["CONSTANTS"]
    
# Get a logger instance
logger = logging.getLogger(__name__)

# ================================================================================================
# HELPER FUNCTIONS
# ================================================================================================
def set_session_data(request):
    image_data = request.POST.get("data", None)
    image_name = request.POST.get("name", None)

    logger.info(f"AJAX POST data received at server: filename={image_name}, filedata={image_data[0:20]}")
    
    if image_data is None: 
        logger.critical(f"Data sent from client does not contain the 'data' key - CANNOT CONTINUE!")

    if image_name is None:
        logger.error(f"Data sent from client does not contain the 'name' key")
        
    request.session[settings.IMAGE_KEY] = {"data": image_data, "name": image_name}
    
def get_regions(input_str):
    if input_str is not None:
        try:
            start_img_str = input_str.index(",") + 1
            image_data_b64 = input_str[start_img_str:]
            aod = ObjectDetector(image_data=image_data_b64,                            
                            confidence_threshold=CONST["AZURE"]["OBJ_DET"]["CONFIDENCE_THRESHOLD"])
            return aod.analyse_and_process()
        except ValueError as err:
            logger.error(f"input_str, {input_str}, does not contain a comma. Sys error: {err}")
    else:
        logger.warning(f"input_str is None; is this expected?")
    return None

def get_stepper_bar_active_states(step_level):
    stepper = HTML["APP"]["STEPPER_BAR"]
    count = 1
    for step in stepper["ITEMS"]:
        if count <= step_level:
            step["CLASS"] = "active"
        else:
            step["CLASS"] = ""
        count += 1
    
    return stepper

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
    if request.method == "POST" and request.is_ajax():
        set_session_data(request)
        return JsonResponse({"status": "success"}, status=200)
    else:
        # get session data if available
        image_data = request.session.get(settings.IMAGE_KEY, None)
        
        # Update config to include the explanatory text for the home page
        HTML["CHOOSE_IMAGE"]["EXPLAIN_TEXT"]["ID"] = HTML["APP"]["EXPLAIN_TEXT"]["ID"]

        # Update config to set the 'active' class for the stepper bar
        stepper_bar = get_stepper_bar_active_states(1)

        # Set ID for the 'next' button
        HTML["CHOOSE_IMAGE"]["NEXT_BTN"]["ID"] = HTML["APP"]["NEXT_BTN"]["ID"]

        context = {
            "title": HTML["CHOOSE_IMAGE"]["TITLE"],
            "navbar": HTML["BASE"]["NAVBAR"],
            "stepper": stepper_bar,
            "explain_text": HTML["CHOOSE_IMAGE"]["EXPLAIN_TEXT"],
            "next_btn": HTML["CHOOSE_IMAGE"]["NEXT_BTN"],
            "choose_img_btn": HTML["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"],
            "image_pane": HTML["APP"]["IMAGE_PANE"],
            "config": CONFIG,
            "image_data": image_data,
            }

        return render(request, PATHS["CHOOSE_IMAGE"], context=context)

def set_regions(request):
    # get session data
    image_data = request.session.get(settings.IMAGE_KEY, None)

    if request.is_ajax() and request.method == "GET":
        logger.info(f"AJAX GET request received at server")        
        processed_data = get_regions(image_data.get("data", None))
        if processed_data["data"] is not None:
            logger.info(f"Azure processing successful, results sent to client")
            return JsonResponse(processed_data, status=200)
        else:
            logger.warning(f"Azure processing unsuccessful, null response sent to client")
            return JsonResponse(processed_data, status=400)
    else:
        # Update config to set the 'active' class for the stepper bar
        stepper_bar = get_stepper_bar_active_states(2)

        # Set IDs for the 'next' and 'previous' buttons
        HTML["SET_REGIONS"]["PREVIOUS_BTN"]["ID"] = HTML["APP"]["PREVIOUS_BTN"]["ID"]
        HTML["SET_REGIONS"]["NEXT_BTN"]["ID"] = HTML["APP"]["NEXT_BTN"]["ID"]
        
        context = {
            "title": HTML["SET_REGIONS"]["TITLE"],
            "navbar": HTML["BASE"]["NAVBAR"],
            "stepper": stepper_bar,
            "explain_text": HTML["SET_REGIONS"]["EXPLAIN_TEXT"],
            "find_rgns_btn": HTML["SET_REGIONS"]["FIND_REGIONS_BTN"],
            "add_rgn_btn": HTML["SET_REGIONS"]["ADD_REGION_BTN"],
            "next_btn": HTML["SET_REGIONS"]["NEXT_BTN"],
            "prev_btn": HTML["SET_REGIONS"]["PREVIOUS_BTN"],
            "image_pane": HTML["APP"]["IMAGE_PANE"],
            "config": CONFIG,
            "image_data": image_data
            }
            
        return render(request, PATHS["SET_REGIONS"], context=context)

def analyse_text(request):

    # Update config to set the 'active' class for the stepper bar
    stepper_bar = get_stepper_bar_active_states(3)

    context = {
        "title": HTML["ANALYSE_TEXT"]["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"],
        "stepper": stepper_bar,
        "explain_text": HTML["APP"]["EXPLAIN_TEXT"],
        "next_btn": HTML["APP"]["NEXT_BTN"],
        "prev_btn": HTML["APP"]["PREVIOUS_BTN"],
        "image_pane": HTML["APP"]["IMAGE_PANE"],
        "config": CONFIG,
        }

    return render(request, PATHS["ANALYSE_TEXT"], context=context)
    

