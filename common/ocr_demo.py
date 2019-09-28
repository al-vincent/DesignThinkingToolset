import requests
import time
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
import functools
from sys import exit


def analyse_image(image_path, subscription_key, analysis_url):
    """
    Use the Azure Computer Vision service to find all the data in an image on 
    a local disk. 
    
    Parameters:
        - image_path (str), the path to the image file that we want to analyse
        - subscription_key (str), the unique key for our Azuer Computer Vision 
        service
        - analysis_url (str), the URL that the Computer Vision service is 
        hosted on.
    
    Returns a dict (cenverted from JSON) with the results of the image analysis
    """
    # Read the image into a byte array
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
    except FileNotFoundError:
        print(f"*** ERROR: the file {image_path} was not found. ***")
        exit(2)
        
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Categories,Description,Color'}
    response = requests.post(analysis_url, 
                             headers=headers, 
                             params=params, 
                             data=image_data)
    response.raise_for_status()
    
    # Extracting text requires two API calls: One call to submit the
    # image for processing, the other to retrieve the text found in the image.
        
    # The recognized text isn't immediately available, so poll to wait for completion.
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(response.headers["Operation-Location"], 
                                      headers=headers)
        analysis = response_final.json()
            
        time.sleep(1)
        # In this case, we've got our results
        if ("recognitionResults" in analysis):
            poll = False
        # in this case, the analysis has completed but failed to work
        if ("status" in analysis and analysis['status'] == 'Failed'):
            print("*** WARNING: No results were obtained from the analysis. ***")
            poll = False
     
    return analysis

def image_transpose_exif(img):
    """
    Apply Image.transpose to ensure 0th row of pixels is at the visual
    top of the image, and 0th column is the visual left-hand side.

    As per CIPA DC-008-2012, the orientation field contains an integer,
    1 through 8. Other values are reserved.
    
    Credit: Roman Odaisky, 
    https://stackoverflow.com/questions/4228530/pil-thumbnail-is-rotating-my-image
    
    Parameters:
        - img (object), a binary stream containing the image data.
        
    Returns either the transformed image, or the original image if the 
    orientation cannot be determined.
    """

    exif_orientation_tag = 0x0112
    exif_transpose_sequences = [                   # Val  0th row  0th col
        [],                                        #  0    (reserved)
        [],                                        #  1   top      left
        [Image.FLIP_LEFT_RIGHT],                   #  2   top      right
        [Image.ROTATE_180],                        #  3   bottom   right
        [Image.FLIP_TOP_BOTTOM],                   #  4   bottom   left
        [Image.FLIP_LEFT_RIGHT, Image.ROTATE_90],  #  5   left     top
        [Image.ROTATE_270],                        #  6   right    top
        [Image.FLIP_TOP_BOTTOM, Image.ROTATE_90],  #  7   right    bottom
        [Image.ROTATE_90],                         #  8   left     bottom
    ]

    try:
        seq = exif_transpose_sequences[img._getexif()[exif_orientation_tag]]
    except Exception:
        return img
    else:
        return functools.reduce(type(img).transpose, seq, img)

def show_results(analysis, image_path):
    """
    Display the results of the image processing / OCR. The image is displayed 
    with a bounding box drawn around each text area discovered by the analysis, 
    with the extracted text overlaid on the image.
    
    Parameters:
        - analysis (dict), the output from the Computer Vision algorithm
        - image_path (str), the filepath for the image
    
    Returns None.
    """
    polygons = []
    # check if we
    if "recognitionResults" in analysis:
        # Extract the recognized text, with bounding boxes.
        polygons = [(line["boundingBox"], line["text"]) for line in analysis["recognitionResults"][0]["lines"]]
        print(f"Polygons: {polygons}")
        # Display the image and overlay it with the extracted text.
        plt.figure(figsize=(30, 30))
        # TODO: we've already got the image once, better to pass it in?
        try:
            image = Image.open(image_path)
        except IOError:
            print(f"*** ERROR: the file {image_path} was not found. ***")
            exit(2)
        # check the image orientation, and alter if necessary
        new_image = image_transpose_exif(image)
        ax = plt.imshow(new_image)
        # plot each of the display boxes
        for polygon in polygons:
            vertices = [(polygon[0][i], polygon[0][i+1]) for i in range(0, len(polygon[0]), 2)]
            text = polygon[1]
            patch = Polygon(vertices, closed=True, fill=False, linewidth=2, color='r')
            ax.axes.add_patch(patch)
            plt.text(vertices[0][0], vertices[0][1], text, fontsize=15, va="top")
        image.close()
    else:
        print(f"*** WARNING: no text was found in {image_path}. Results: {analysis} ***")
        exit(3)

def main():
    # TODO: to be 'better', SUSCRIPTION_KEY, REGION and IMAGE_PATH should be 
    # supplied via argparse or similar.
    
    # Set the subscription key for the Computer Vision service
    SUBSCRIPTION_KEY = "c61dcfc33cfc4c9db6178bc1f81ffc6d"
    assert SUBSCRIPTION_KEY
    
    # set the API region to use (must match the region in the subscription)
    REGION = "uksouth"
    
    # Set the Computer Vision base URL and analysis URL
    VISION_BASE_URL = f"https://{REGION}.api.cognitive.microsoft.com/vision/v2.0/"
    ANALYSIS_URL = VISION_BASE_URL + "read/core/asyncBatchAnalyze"
    
    # Set image_path to the local path of an image that you want to analyze.
    IMAGE_PATH = "C:/Users/Al/OneDrive/Pictures/PostIts/persona.jpg"
#    IMAGE_PATH = "C:/Users/Al/OneDrive/Code/DesignThinkingToolset/media/test/test_img.jpg"
    
    # analyse the image
    results = analyse_image(image_path=IMAGE_PATH, 
                            subscription_key=SUBSCRIPTION_KEY,
                            analysis_url=ANALYSIS_URL)
    # display the results
    show_results(analysis=results, image_path=IMAGE_PATH)
  
if __name__ == "__main__":
    main()