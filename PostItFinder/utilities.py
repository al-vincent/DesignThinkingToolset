from django.conf import settings
from django.http import JsonResponse

from PostItFinder.azure_services import ImageValidation, ObjectDetector, TextAnalyser, MatchWordsToRegions
from PostItFinder.create_and_store_pptx import SnipPptxCreator, SaveFileToAzureBlobStorage

import os
import logging
from json import load, loads
from datetime import datetime, timedelta
from io import BytesIO
from PIL import Image, ImageOps
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

    # get the user id
    user_id = request.session.get(settings.USER_ID, None)
    if user_id == None:
        logger.error(f"User ID is None!!") 

    logger.info(f"User {user_id}: AJAX POST data received at server: filename={image_name}, filedata={image_data[0:40]}...")
    
    if image_data is None: 
        logger.critical(f"User {user_id}: Data sent from client does not contain the 'data' key - CANNOT CONTINUE!")
        return False

    if image_name is None:
        logger.error(f"User {user_id}: Data sent from client does not contain the 'name' key")
        return False
    
    request.session[settings.IMAGE_KEY] = {"data": image_data, "name": image_name}
    logger.info(f"User {user_id}: Image recorded in session data")
    return True

def set_session_region_data(request):
    # get the user id
    user_id = request.session.get(settings.USER_ID, None)
    if user_id == None:
        logger.error(f"User ID is None!!") 

    # Regions data is stringified in the JS; convert it to a JSON structure
    regions = loads(request.POST.get("data", None))

    logger.info(f"User {user_id}: AJAX POST data received at server: regions={regions}")
    
    if regions is None: 
        logger.warning(f"User {user_id}: Data sent from client does not contain the 'data' key - no regions selected?")
        
    request.session[settings.REGION_KEY] = regions
    logger.info(f"User {user_id}: Regions saved in session data")

# ================================================================================================
# GETTING REGIONS AND TEXT
# ================================================================================================
def get_regions(img_url, user_id):

    if img_url is not None:        
        od_url = ObjectDetector(is_image_url=True,
                            image=img_url,
                            prediction_key=settings.OBJ_DET_PREDICTION_KEY,
                            obj_det_url=f"{settings.OBJ_DET_API_URL}",
                            confidence_threshold=CONST["AZURE"]["OBJ_DET"]["CONFIDENCE_THRESHOLD"])
        logger.info(f"User {user_id}: image sent for region processing")
        return od_url.analyse_and_process()
    else:
        logger.error(f"User {user_id}: no image URL in session data")
        return None

def get_text(input_str, regions, user_id):

    # if the user has selected some regions, set use_words to True. 
    # Otherwise it's False,and lines of text will be extracted.
    use_words = True if regions else False
    if input_str is not None:        
        ta = TextAnalyser(is_image_url=True,
                        image=input_str,
                        subscription_key=settings.OCR_SUBSCRIPTION_KEY,
                        api_url=settings.OCR_API_URL, 
                        use_words=use_words)
        text = ta.analyse_and_process()
        if use_words:
            logger.info(f"User {user_id}: Text will be assigned to regions")
            return assign_text_to_regions(regions, text, user_id)
        else:
            logger.info(f"User {user_id}: No regions discovered; lines will be returned")
            return text
    else:
        logger.warning(f"User {user_id}: input_str is None; is this expected?")
        return None

def assign_text_to_regions(regions, words, user_id):
    logger.info(f"User {user_id}: words matched to regions")
    mwtr = MatchWordsToRegions(region_data=regions, word_data=words)
    return mwtr.match()

# ================================================================================================
# UPLOADING FILES TO BLOB STORAGE
# ================================================================================================
def upload_file_to_blob_storage(container_name, file_name, file_bytes, user_id):
    """
    Create a new container and upload a file to it.

    Parameters:
        container_name (str): name of the container that the file will be stored in
        file_name (str): file name to be used in blob storage (can be different to the
        existing local file name)
        file_bytes (bytes): bytes to be saved to storage

    Returns:
        str or None: if upload completes correctly, the URL to the file will be returned.
        If the upload fails for any reason, None is returned.
    """
    sftabs = SaveFileToAzureBlobStorage(connect_str=settings.BLOB_STORAGE_CONN_STR,
                                        container_name=container_name)
    url = sftabs.create_container_and_upload_file(file_name=file_name, file_bytes=file_bytes)

    if url is not None:
        logger.info(f"User {user_id}: File uploaded successfully to blob storage. URL created: {url}")
    else:
        logger.warning(f"User {user_id}: File NOT uploaded successfully to blob storage.")
    
    return url

def generate_container_name(user_id):
    """ 
    Create a unique name for the container, in the format: YYYYMMDD-HHMMSS-uuid
    
    Appending the uuid to the container name prevents clashes with other container 
    names, and the datetime will allow easy lookup if any errors are encountered.

    Including a ref to the image filename in either name is not a good option, 
    given how many issues could be encountered with filenames (e.g. length of 
    filename, switching / removing illegal characters etc).

    The container name must conform to the Azure rules:
    https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#container-names

    Parameters:
        user_id (str): a uuid4() cast to str. 

    Returns:
        str: containing the container name in the format described
    """    
    # generate the container name and presentation filename
    now = datetime.now()
    return f"{now.strftime('%Y%m%d-%H%M%S')}-{user_id}"

def generate_presentation_filename():
    """ 
    Create a unique name for the presentation file, in the format: YYYYMMDD-HHMMSS-SnipResults.pptx
    
    Including the datetime should allow easy lookup if errors are encountered.

    The filename must conform to the Azure rules:
    https://docs.microsoft.com/en-us/rest/api/storageservices/naming-and-referencing-containers--blobs--and-metadata#blob-names

    Returns:
        str: containing the filename of the presentation, in the format described.
    """    
    # generate the container name and presentation filename
    now = datetime.now()
    return f"{now.strftime('%Y%m%d-%H%M%S')}-SnipResults.pptx"

def get_bytes_from_b64_encoded_string(b64_string):
    start_img_str = b64_string.index(",") + 1
    image_data_b64 = b64_string[start_img_str:]
    base64_img_bytes = image_data_b64.encode('utf-8')
    return BytesIO(base64.decodebytes(base64_img_bytes))

# def set_image_orientation(img_bytes):
#     img = Image.open(img_bytes)
#     new_img = ImageOps.exif_transpose(img)
#     img_byte_arr = BytesIO()
#     new_img.save(img_byte_arr, format=img.format)
#     return img_byte_arr.getvalue()

# ================================================================================================
# DRIVER FUNCTIONS FOR INDIVIDUAL PAGE ACTIONS
# ================================================================================================
# ---------------------------
# --- choose-image events ---
# ---------------------------
def click_upload_image_button(request):
    """
    Steps to complete when the Upload Image button is clicked, i.e.:
    - generate a new container name and presentation filename;
    - store these and the image data (filename and base64-encoded string) in 
    session variables;
    - upload the image to Azure Blob Storage;
    - store the URL created in a session variable.

    Parameters:
        - request (django HttpRequest object): created when the HTTP request is made, 
        and contains the data sent via the AJAX POST request.

    Returns:
        - bool: True if everything executes correctly, otherwise False.
    """
    # get the user id
    user_id = request.session.get(settings.USER_ID, None)
    if user_id == None:
        logger.error(f"User ID is None!!") 

    # generate a new container name 
    container_name = generate_container_name(user_id)
    logger.info(f"User {user_id}: Container name generated; {container_name}")
    
    # store the container name, presentation name and image info in session vars
    request.session[settings.CONTAINER_NAME_KEY] = container_name
    result = set_session_image_data(request)

    # upload the image file to blob storage
    if result:
        logger.info(f"User {user_id}: session image data set successfully")
        file_info = request.session[settings.IMAGE_KEY]
        file_bytes = get_bytes_from_b64_encoded_string(file_info["data"])
        url = upload_file_to_blob_storage(container_name=container_name, 
                                        file_name= file_info["name"],
                                        file_bytes=file_bytes,
                                        user_id=user_id)
    else:
        # if the session variable was not set correctly, return False
        logger.warning(f"User {user_id}: session image data NOT set successfully")
        return False

    # store the URL returned in a session var
    if url is not None:
        request.session[settings.URL_KEY] = url
        logger.info(f"User {user_id}: URL session data set")
    else:
        # if the upload fails, return False
        logger.warning(f"User {user_id}: URL session data NOT set")
        return False

    # on successful completion, return True
    return True
    
# ---------------------------
# --- analyse-text events ---
# ---------------------------
def click_analyse_text_button(request):
    # get the image and the current regions (if any)
    image_data = request.session.get(settings.IMAGE_KEY, None)
    image_url = request.session.get(settings.URL_KEY, None)
    regions = request.session.get(settings.REGION_KEY, None)
    user_id = request.session.get(settings.USER_ID, None)

    # analyse the text
    if all([image_url, regions, user_id]):
        region_text = get_text(image_url, regions, user_id)
    else:
        logger.warning(f"User {user_id}: var is None. image_url: {image_url}; regions: {regions}; user_id: {user_id}")

    # text has been found and assigned to regions
    if region_text is not None:
        logger.info(f"User {user_id}: Azure processing successful")

        # get the existing Blob Storage container name and generate a new presentation filename
        container_name = request.session.get(settings.CONTAINER_NAME_KEY, None)
        presentation_name = generate_presentation_filename()

        # get the image bytes
        img_bytes = get_bytes_from_b64_encoded_string(image_data.get("data"))

        # create the presentation and save it to the new directory
        spc = SnipPptxCreator(image_filename=image_data.get("name"),
                            image_bytes=img_bytes,
                            text_boxes=region_text)
        pres_bytes = spc.build_pres()
        logger.info(f"User {user_id}: Presentation {presentation_name} was created successfully")

        # create blob storage container and upload presentation and image, returning 
        # the URL of the presentation
        sftabs = SaveFileToAzureBlobStorage(connect_str=settings.BLOB_STORAGE_CONN_STR,
                                            container_name=container_name)
        url = sftabs.upload_bytes_to_container(file_name=presentation_name,
                                                file_bytes=pres_bytes)

        if url is not None:
            logger.info("User {user_id}: Processing successful and files transferred. Sending results to client")
            return JsonResponse({"data": region_text, "url": url}, status=200)
        else: 
            logger.warning(f"User {user_id}: File transfer unsuccessful, null response sent to client")
            return JsonResponse(None, safe=False, status=400) 
    # something has gone wrong...
    else:
        logger.warning(f"User {user_id}: Azure region_text unsuccessful, null response sent to client")
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
