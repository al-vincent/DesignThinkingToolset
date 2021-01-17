import os, requests, json

prediction_key = os.environ.get("SNIP_OBJ_DET_PRED_KEY")
project_id = os.environ.get("SNIP_OBJ_DET_PROJ_ID")
published_name = os.environ.get("SNIP_OBJ_DET_PUB_NAME")
api_url = f"https://uksouth.api.cognitive.microsoft.com/customvision/v3.0/Prediction/{project_id}/detect/iterations/{published_name}/url"
img_url = "https://snipblobstorage.blob.core.windows.net/snip-test-container-01/test_postits.jpg"

headers = {
    # Request headers
    'Content-Type': 'application/json',
    'Prediction-key': prediction_key,
}

try:
    response = requests.post(api_url, headers=headers, data = json.dumps({"url": img_url}))
    response.raise_for_status()
except Exception as err:
    print(f"ERROR: {err}")

print(response.json())