from django.conf import settings
from django.http import JsonResponse

from PostItFinder.azure_services import ObjectDetector, TextAnalyser, MatchWordsToRegions
from PostItFinder.create_and_store_pptx import SnipPptxCreator, SaveFileToAzureBlobStorage

import os
import logging
from json import load, loads
from datetime import datetime, timedelta
from io import BytesIO
import uuid
import base64

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
# SETTING SESSION VARIABLES
# ================================================================================================
def set_session_image_data(request):
    # get the image information that was sent in the AJAX request 
    image_data = request.POST.get("data", None)
    image_name = request.POST.get("name", None)

    logger.info(f"AJAX POST data received at server: filename={image_name}, filedata={image_data[0:40]}...")
    
    if image_data is None: 
        logger.critical(f"Data sent from client does not contain the 'data' key - CANNOT CONTINUE!")
        return False

    if image_name is None:
        logger.error(f"Data sent from client does not contain the 'name' key")
        return False
    
    request.session[settings.IMAGE_KEY] = {"data": image_data, "name": image_name}
    logger.info(f"Image recorded in session data successfully")
    return True

def set_session_region_data(request):
    # Regions data is stringified in the JS; convert it to a JSON structure
    regions = loads(request.POST.get("data", None))

    logger.info(f"AJAX POST data received at server: regions={regions}")
    
    if regions is None: 
        logger.warning(f"Data sent from client does not contain the 'data' key - no regions selected?")
        
    request.session[settings.REGION_KEY] = regions

# ================================================================================================
# GETTING REGIONS AND TEXT
# ================================================================================================
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
                return assign_text_to_regions(regions, text)
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

# ================================================================================================
# UPLOADING FILES TO BLOB STORAGE
# ================================================================================================
def upload_file_to_blob_storage(container_name, file_name, file_bytes):
    """
    

    Args:
        container_name (str): name of the container that the 
        file_name ([type]): [description]
        file_bytes ([type]): [description]

    Returns:
        [type]: [description]
    """
    sftabs = SaveFileToAzureBlobStorage(connect_str=settings.BLOB_STORAGE_CONN_STR,
                                        container_name=container_name)
    url = sftabs.create_container_and_upload_file(file_name=file_name, file_bytes=file_bytes)

    if url is not None:
        logger.info(f"File uploaded successfully to blob storage. URL created: {url}")
    else:
        logger.warning(f"File NOT uploaded successfully to blob storage.")
    
    return url

def generate_container_name_and_pres_filename():
    """ 
    Create a unique name for the container and presentation file, in the formats:
        - container; YYYYMMDD-HHMMSS-uuid
        - presentation file; YYYYMMDD-HHMMSS-SnipResults.pptx
    
    Appending the uuid to the container name prevents clashes with other container 
    names, and the datetime will allow easy lookup if any errors are encountered.

    Including a ref to the image filename in either name is not a good option, 
    given how many issues could be encountered with filenames (e.g. length of 
    filename, switching / removing illegal characters etc).

    The container name and filename must conform to the Azure rules:
    https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names
    https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#blob-names
    [NOTE: container format is much more stringent than filename format]

    Returns:
        tuple: of the format (container name, presentation filename)
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

# ================================================================================================
# DRIVER FUNCTIONS FOR INDIVIDUAL PAGE ACTIONS
# ================================================================================================
def click_upload_image_button(request):
    """
    Steps to complete when the Upload Image button is clicked, i.e.:
    - generate a new container name and presentation filename;
    - store these and the image data (filename and base64-encoded string) in 
    session variables;
    - upload the image to Azure Blob Storage;
    - store the URL created in a session variable.

    Args:
        request (django HttpRequest object): created when the HTTP request is made, 
        and contains the data sent via the AJAX POST request.

    Returns:
        bool: True if everything executes correctly, otherwise False.
    """
    # generate a new container name and presentation filename
    container_name, pres_name = generate_container_name_and_pres_filename()
    
    # store the container name, presentation name and image info in session vars
    request.session[settings.CONTAINER_NAME_KEY] = container_name
    request.session[settings.PRESENTATION_NAME_KEY] = pres_name
    result = set_session_image_data(request)

    # upload the image file to blob storage
    if result:
        file_info = request.session[settings.IMAGE_KEY]
        file_bytes = get_bytes_from_b64_encoded_string(file_info["data"])
        url = upload_file_to_blob_storage(container_name=container_name, 
                                        file_name= file_info["name"],
                                        file_bytes=file_bytes)
    else:
        # if the session variable was not set correctly, return False
        return False

    # store the URL returned in a session var
    if url is not None:
        request.session[settings.URL_KEY] = url
    else:
        # if the upload fails, return False
        return False

    # on successful completion, return True
    return True

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

# ================================================================================================
# GENERAL HELPER FUNCTIONS
# ================================================================================================
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
