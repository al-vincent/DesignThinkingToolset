from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse

import PostItFinder.utilities as ut

import os
from json import load
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
# ROUTES
# ================================================================================================
def index(request):
    # clear all session data
    request.session.flush()

    context = {
        "title": HTML["HOME"]["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"],
        "home_content": "Home page",
        "start_btn": HTML["HOME"]["START_BTN"],
        "config": CONFIG,
        }

    return render(request, PATHS["HOME"], context=context)

def about(request):
    context = {
        "title": HTML["ABOUT"]["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"],
        "about_content": "Placeholder for some info about the app"
        }
    
    return render(request, PATHS["ABOUT"], context=context)

def faq(request):
    context = {
        "title": HTML["FAQ"]["TITLE"],
        "navbar": HTML["BASE"]["NAVBAR"]
        }
    
    return render(request, PATHS["FAQ"], context=context)

def choose_image(request):
    # clear any regions session data, to prevent crossover between regions
    request.session[settings.REGION_KEY] = None

    if request.is_ajax() and request.method == "POST":
        result = ut.click_upload_image_button(request)
        if result:
            return JsonResponse({"status": "success"}, status=200)
        else:
            return JsonResponse({"status": "fail"}, status=400)
    else:
        # get session data if available
        image_data = request.session.get(settings.IMAGE_KEY, None)
        
        # Update config to include the explanatory text for the home page
        HTML["CHOOSE_IMAGE"]["EXPLAIN_TEXT"]["ID"] = HTML["APP"]["EXPLAIN_TEXT"]["ID"]

        # Update config to set the 'active' class for the stepper bar
        stepper_bar = ut.get_stepper_bar_active_states(1)

        # Set ID for the 'next' button
        HTML["CHOOSE_IMAGE"]["NEXT_BTN"]["ID"] = HTML["APP"]["NEXT_BTN"]["ID"]

        context = {
            "title": HTML["CHOOSE_IMAGE"]["TITLE"],
            "navbar": HTML["BASE"]["NAVBAR"],
            "stepper": stepper_bar,
            "explain_text": HTML["CHOOSE_IMAGE"]["EXPLAIN_TEXT"],
            "next_btn": HTML["CHOOSE_IMAGE"]["NEXT_BTN"],
            "choose_img_btn": HTML["CHOOSE_IMAGE"]["CHOOSE_IMG_BTN"],
            "upload_img_btn": HTML["CHOOSE_IMAGE"]["UPLOAD_IMG_BTN"],
            "image_pane": HTML["APP"]["IMAGE_PANE"],
            "config": CONFIG,
            "image_data": image_data,
            }

        return render(request, PATHS["CHOOSE_IMAGE"], context=context)

def set_regions(request):
    image_url = request.session.get(settings.URL_KEY, None)

    if request.is_ajax() and request.method == "GET":
        logger.info(f"AJAX GET request received at server")        
        processed_data = ut.get_regions(img_url=image_url)
        if processed_data is not None:
            logger.info(f"Azure processing successful, results sent to client")
            return JsonResponse(processed_data, safe=False, status=200)
        else:
            logger.warning(f"Azure processing unsuccessful, null response sent to client")
            return JsonResponse(processed_data, safe=False, status=400)
    elif request.is_ajax() and request.method == "POST":
        logger.info(f"AJAX POST request received at server")        
        ut.set_session_region_data(request)
        return JsonResponse({"status": "success"}, status=200)
    else:
        # Update config to set the 'active' class for the stepper bar
        stepper_bar = ut.get_stepper_bar_active_states(2)

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
            "image_data": image_url,
            "region_data": request.session.get(settings.REGION_KEY, None),
            }
            
        return render(request, PATHS["SET_REGIONS"], context=context)

def analyse_text(request):
    # get session data
    # image_data = request.session.get(settings.IMAGE_KEY, None)
    image_url = request.session.get(settings.URL_KEY, None)
    regions = request.session.get(settings.REGION_KEY, None)

    # user has clicked "Analyse Text"
    if request.is_ajax() and request.method == "GET":        
        return ut.click_analyse_text_button(request)
    else:
        # Update config to set the 'active' class for the stepper bar
        stepper_bar = ut.get_stepper_bar_active_states(3)

        HTML["ANALYSE_TEXT"]["PREVIOUS_BTN"]["ID"] = HTML["APP"]["PREVIOUS_BTN"]["ID"]

        context = {
            "title": HTML["ANALYSE_TEXT"]["TITLE"],
            "navbar": HTML["BASE"]["NAVBAR"],
            "stepper": stepper_bar,
            "explain_text": HTML["ANALYSE_TEXT"]["EXPLAIN_TEXT"],
            "prev_btn": HTML["ANALYSE_TEXT"]["PREVIOUS_BTN"],
            "analyse_txt_btn": HTML["ANALYSE_TEXT"]["ANALYSE_TEXT_BTN"],
            "download_results_btn": HTML["ANALYSE_TEXT"]["DOWNLOAD_RESULTS_BTN"],
            "image_pane": HTML["APP"]["IMAGE_PANE"],
            "config": CONFIG,
            # "image_data": image_data, 
            "image_data": image_url, 
            "region_data": regions,
            }

        return render(request, PATHS["ANALYSE_TEXT"], context=context)
    

