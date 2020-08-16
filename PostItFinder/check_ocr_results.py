# ================================================================================================
# Name:        check_ocr_results.py
# Description: script provided in Azure Read API Quickstart, to illustrate usage of the API.
#              Used here to check that the results provided by the API are still correct, as 
#              small changes to the Azure image processing algorithms may cascade to the results
#              (for example, the bounding boxes produced by this code on 15/08/20 are different to 
#              those shown in the example JSON on the page).
# Reference:   https://docs.microsoft.com/en-gb/azure/cognitive-services/computer-vision/quickstarts/python-hand-text
# ================================================================================================

import json
import os
import sys
import requests
import time

missing_env = False

if 'SNIP_OCR_SUBS_KEY' in os.environ:
    subscription_key = os.environ['SNIP_OCR_SUBS_KEY']
else:
    print("From Azure Cogntivie Service, retrieve your endpoint and subscription key.")
    print("\nSet the OCR_SUBSCRIPTION_KEY environment variable, such as \"1234567890abcdef1234567890abcdef\".\n")
    missing_env = True

if missing_env:
    print("**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

text_recognition_url = "https://snip-ocr.cognitiveservices.azure.com/vision/v3.0/read/analyze"

# Set image_url to the URL of an image that you want to recognize.
image_url = "https://raw.githubusercontent.com/MicrosoftDocs/azure-docs/master/articles/cognitive-services/Computer-vision/Images/readsample.jpg"

headers = {'Ocp-Apim-Subscription-Key': subscription_key}
data = {'url': image_url}
response = requests.post(text_recognition_url, headers=headers, json=data)
response.raise_for_status()

# Extracting text requires two API calls: One call to submit the
# image for processing, the other to retrieve the text found in the image.

# Holds the URI used to retrieve the recognized text.
operation_url = response.headers["Operation-Location"]

# The recognized text isn't immediately available, so poll to wait for completion.
analysis = {}
poll = True
while (poll):
    response_final = requests.get(
        response.headers["Operation-Location"], headers=headers)
    analysis = response_final.json()
    
    # print(json.dumps(analysis, indent=4))

    time.sleep(1)
    if ("analyzeResult" in analysis):
        poll = False
    if ("status" in analysis and analysis['status'] == 'failed'):
        poll = False

print(analysis)