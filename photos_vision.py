import io
import os
import json
import requests

from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes, OperationStatusCodes

credentials = json.load(open('credentials.json'))
API_KEY = credentials['API_KEY']
ENDPOINT = credentials['ENDPOINT']

cv_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

def describe_image_in_stream(image):


    response = cv_client.describe_image_in_stream(open(image, 'rb'))

    for tag in response.tags:
        print(tag)


    # Prepare the data to be written to the JSON file
    data = {
        'image_path': image,
        'tags': [tag for tag in response.tags],
        'captions': [{'text': caption.text, 'confidence': caption.confidence} for caption in response.captions]
    }

    # Read the existing data
    try:
        with open('output.json', 'r', encoding='utf-8') as f:
            try:
                data_list = json.load(f)
            except json.JSONDecodeError:
                data_list = []
    except FileNotFoundError:
        data_list = []

    # Add the new data
    data_list.append(data)

    # Write the data back to the file
    with open('output.json', 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=4)


# function that calls describe_image_in_stream for every image in a photos folder
def analyze_images_in_folder(folder_name):
    # List all files in the directory
    files = os.listdir(folder_name)

    # Filter out non-image files
    image_files = [f for f in files if f.endswith(('.png', '.jpg', '.jpeg'))]

    for image_file in image_files:
        # Create the full image path
        image_path = os.path.join(folder_name, image_file)
        describe_image_in_stream(image_path)

