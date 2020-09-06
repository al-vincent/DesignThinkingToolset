from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse, FileResponse

from PostItFinder.azure_services import ObjectDetector, TextAnalyser, MatchWordsToRegions
from PostItFinder.create_and_store_pptx import SnipPptxCreator, SaveFileToAzureBlobStorage

import os
from json import load, loads
import base64
import logging
from datetime import datetime, timedelta
import uuid
from io import BytesIO


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
def set_session_image_data(request):
    # clear any regions session data, to prevent crossover between regions
    request.session[settings.REGION_KEY] = None

    image_data = request.POST.get("data", None)
    image_name = request.POST.get("name", None)

    logger.info(f"AJAX POST data received at server: filename={image_name}, filedata={image_data[0:40]}...")
    
    if image_data is None: 
        logger.critical(f"Data sent from client does not contain the 'data' key - CANNOT CONTINUE!")

    if image_name is None:
        logger.error(f"Data sent from client does not contain the 'name' key")
        
    request.session[settings.IMAGE_KEY] = {"data": image_data, "name": image_name}

def set_session_region_data(request):
    # Regions data is stringified in the JS; convert it to a JSON structure
    regions = loads(request.POST.get("data", None))

    logger.info(f"AJAX POST data received at server: regions={regions}")
    
    if regions is None: 
        logger.info(f"Data sent from client does not contain the 'data' key - no regions selected?")
        
    request.session[settings.REGION_KEY] = regions
   
def get_regions(input_str):
    if input_str is not None:
        try:
            start_img_str = input_str.index(",") + 1
            image_data_b64 = input_str[start_img_str:]
            aod = ObjectDetector(image_data=image_data_b64, 
                                prediction_key=settings.OBJ_DET_PREDICTION_KEY,
                                obj_det_url=settings.OBJ_DET_API_URL,
                                confidence_threshold=CONST["AZURE"]["OBJ_DET"]["CONFIDENCE_THRESHOLD"])
            return aod.analyse_and_process()
        except ValueError as err:
            logger.error(f"input_str, {input_str}, does not contain a comma. Sys error: {err}")
            return None
    else:
        logger.warning(f"input_str is None; is this expected?")
        return None

def get_text(input_str, regions):
    # if the user has selected some regions, set use_words to True. 
    # Otherwise it's False,and lines of text will be extracted.
    use_words = True if regions else False
    if input_str is not None:
        try:
            start_img_str = input_str.index(",") + 1
            image_data_b64 = input_str[start_img_str:]
            
            ta = TextAnalyser(image_data=image_data_b64,
                            subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                            api_url=settings.OCR_API_URL, 
                            use_words=use_words)
            text = ta.analyse_and_process()
            if use_words:
                logger.info("Text will be assigned to regions")
                return assign_text_to_regions(regions, text);
            else:
                logger.info("No regions discovered; lines will be returned")
                return text
        except ValueError as err:
            logger.error(f"input_str, {input_str}, does not contain a comma. Sys error: {err}")
            return None
    else:
        logger.warning(f"input_str is None; is this expected?")
        return None

def assign_text_to_regions(regions, words):
    mwtr = MatchWordsToRegions(region_data=regions, word_data=words)
    return mwtr.match()

def get_blob_url(filename, filepath, container_name, create_new_container):
    sftabs = SaveFileToAzureBlobStorage(settings.BLOB_STORAGE_CONN_STR,
                                        filename=filename,
                                        filepath=filepath,
                                        container_name=container_name, 
                                        create_new_container=create_new_container)
    return sftabs.get_blob_url()

def generate_container_name_and_pres_filename():
    """ 
    Create a unique name for the container and presentation file, in the formats:
        - container; YYYYMMDDHHMMSS-uuid
        - presentation file; YYYYMMDDHHMMSS-SnipResults
    
    Appending the uuid to the container name prevents clashes with other container 
    names, and the datetime should allow easy lookup if anything goes wrong.

    Including a ref to the image in either name is not a good option, given how 
    many issues could be encountered with filenames (e.g. length of filename, 
    switching / removing illegal characters etc).

    The container name and filename must conform to the Azure rules:
    https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names
    https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#blob-names
    [NOTE: container format is much more stringent than filename format]
    """    
    # generate the container name and presentation filename
    now = datetime.now()
    container_name = f"{now.strftime('%Y%m%d%H%M%S')}-{uuid.uuid4()}"
    pres_filename = f"{now.strftime('%Y%m%d%H%M%S')}-SnipResults.pptx"
    
    return (container_name, pres_filename)                                  

def get_bytes_from_b64_encoded_string(b64_string):
    start_img_str = b64_string.index(",") + 1
    image_data_b64 = b64_string[start_img_str:]
    base64_img_bytes = image_data_b64.encode('utf-8')
    return BytesIO(base64.decodebytes(base64_img_bytes))

def analyse_text_button_click(request):
    # get the image and the current regions (if any)
    image_data = request.session.get(settings.IMAGE_KEY, None)
    regions = request.session.get(settings.REGION_KEY, None)

    # analyse the text
    region_text = get_text(image_data.get("data", None), regions)

    # text has been found and assigned to regions
    if region_text is not None:
        logger.info(f"Azure processing successful")

        # generate Blob Storage container name and presentation filename
        container_name, presentation_name = generate_container_name_and_pres_filename()

        # get the image bytes
        img_bytes = get_bytes_from_b64_encoded_string(image_data.get("data"))

        # create the presentation and save it to the new directory
        spc = SnipPptxCreator(image_filename=image_data.get("name"),
                            image_bytes=img_bytes,
                            text_boxes=region_text)
        pres_bytes = spc.build_pres()
        logger.info(f"The presentation {presentation_name} was created successfully")

        # create blob storage container and upload presentation and image, returning 
        # the URL of the presentation
        sftabs = SaveFileToAzureBlobStorage(connect_str=settings.BLOB_STORAGE_CONN_STR,
                                            container_name=container_name)
        url = sftabs.upload_bytes_to_blob_storage(file_name=presentation_name,
                                                file_bytes=pres_bytes)

        if url is not None:
            logger.info("Processing successful and files transferred. Sending results to client")
            return JsonResponse({"data": region_text, "url": url}, status=200)
        else: 
            logger.warning(f"File transfer unsuccessful, null response sent to client")
            return JsonResponse(None, safe=False, status=400) 
    # something has gone wrong...
    else:
        logger.warning(f"Azure region_text unsuccessful, null response sent to client")
        return JsonResponse(None, safe=False, status=400)    

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
        "start_btn": HTML["HOME"]["START_BTN"],
        "config": CONFIG,
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
    # clear any regions session data, to prevent crossover between regions
    request.session[settings.REGION_KEY] = None

    if request.is_ajax() and request.method == "POST":
        set_session_image_data(request)
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
        if processed_data is not None:
            logger.info(f"Azure processing successful, results sent to client")
            return JsonResponse(processed_data, safe=False, status=200)
        else:
            logger.warning(f"Azure processing unsuccessful, null response sent to client")
            return JsonResponse(processed_data, safe=False, status=400)
    elif request.is_ajax() and request.method == "POST":
        logger.info(f"AJAX POST request received at server")        
        set_session_region_data(request)
        return JsonResponse({"status": "success"}, status=200)
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
            "image_data": image_data,
            "region_data": request.session.get(settings.REGION_KEY, None),
            }
            
        return render(request, PATHS["SET_REGIONS"], context=context)

def analyse_text(request):
    # get session data
    image_data = request.session.get(settings.IMAGE_KEY, None)
    regions = request.session.get(settings.REGION_KEY, None)

    # user has clicked "Analyse Text"
    if request.is_ajax() and request.method == "GET":        
        return analyse_text_button_click(request)
    else:
        # Update config to set the 'active' class for the stepper bar
        stepper_bar = get_stepper_bar_active_states(3)

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
            "image_data": image_data, 
            "region_data": request.session.get(settings.REGION_KEY, None),
            }

        return render(request, PATHS["ANALYSE_TEXT"], context=context)
    

