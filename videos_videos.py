# from azure.ai.videoanalyzer import VideoAnalyzerClient
# from azure.core.credentials import AzureKeyCredential

# credentials = json.load(open('credentials_videos.json'))
# API_KEY_VIDEOS = credentials['API_KEY_VIDEOS']
# ENDPOINT_VIDEOS = credentials['ENDPOINT_VIDEOS']

# # Create a VideoAnalyzerClient
# video_analyzer_client = VideoAnalyzerClient(endpoint=ENDPOINT, credential=AzureKeyCredential(API_KEY))

# def analyze_video(video_path):
    

#     # Open the video file
#     with open(video_path, 'rb') as video_file:
#         video_bytes = video_file.read()

#     # Analyze the video
#     response = video_analyzer_client.analyze_video(input=video_bytes)

#     # Prepare the data to be written to the JSON file
#     data = {
#         'video_path': video_path,
#         'insights': response.video_analysis
#     }

#     # Read the existing data
#     try:
#         with open('output.json', 'r', encoding='utf-8') as f:
#             try:
#                 data_list = json.load(f)
#             except json.JSONDecodeError:
#                 data_list = []
#     except FileNotFoundError:
#         data_list = []

#     # Add the new data
#     data_list.append(data)

#     # Write the data back to the file
#     with open('output.json', 'w', encoding='utf-8') as f:
#         json.dump(data_list, f, ensure_ascii=False, indent=4)



# def analyze_videos_in_folder(folder_name):
#     # List all files in the directory
#     files = os.listdir(folder_name)

#     # Filter out non-video files
#     video_files = [f for f in files if f.endswith(('.mp4', '.avi', '.mov'))]

#     for video_file in video_files:
#         # Create the full video path
#         video_path = os.path.join(folder_name, video_file)
#         analyze_video(video_path)



import requests
import json
import time

api_url = "your_api_url"
location = "your_location"
account_id = "51bfa390-ecc7-46e8-a636-c1dc77313df9"
account_access_token = "84d1958c86ef4599b5fb912aba677f15"
api_key = "84d1958c86ef4599b5fb912aba677f15"
video_url = "your_video_url"  # or remove this if uploading a video file

# As an alternative to specifying video URL, you can upload a file
with open('path_to_video_file', 'rb') as video_file:
    video_content = video_file.read()

content = {
    # Add other form data if needed
    'file': ('filename', video_content, 'video/mp4')
}

# Assuming the video is being uploaded via file, remove the videoUrl from this line
response = requests.post(
    f"{api_url}/{location}/Accounts/{account_id}/Videos?accessToken={account_access_token}&name=some_name&description=some_description&privacy=private&partition=some_partition",
    files=content
)

upload_result = response.text
video_id = json.loads(upload_result)['id']
print("Uploaded")
print(f"Video ID: {video_id}")

# Obtain video access token
headers = {
    "Ocp-Apim-Subscription-Key": api_key
}
response = requests.get(
    f"{api_url}/auth/{location}/Accounts/{account_id}/Videos/{video_id}/AccessToken?allowEdit=true",
    headers=headers
)
video_access_token = response.text.replace('"', '')

# Wait for the video index to finish
while True:
    time.sleep(10)
    
    response = requests.get(
        f"{api_url}/{location}/Accounts/{account_id}/Videos/{video_id}/Index?accessToken={video_access_token}&language=English"
    )
    video_index_result = response.text
    
    processing_state = json.loads(video_index_result)['state']
    
    print("\nState:")
    print(processing_state)
    
    if processing_state != "Uploaded" and processing_state != "Processing":
        print("\nFull JSON:")
        print(video_index_result)
        break

# Search for the video
response = requests.get(
    f"{api_url}/{location}/Accounts/{account_id}/Videos/Search?accessToken={account_access_token}&id={video_id}"
)
search_result = response.text
print("\nSearch:")
print(search_result)

# Get insights widget url
response = requests.get(
    f"{api_url}/{location}/Accounts/{account_id}/Videos/{video_id}/InsightsWidget?accessToken={video_access_token}&widgetType=Keywords&allowEdit=true"
)
insights_widget_link = response.headers['Location']
print("Insights Widget url:")
print(insights_widget_link)

# Get player widget url
response = requests.get(
    f"{api_url}/{location}/Accounts/{account_id}/Videos/{video_id}/PlayerWidget?accessToken={video_access_token}"
)
player_widget_link = response.headers['Location']
print("\nPlayer Widget url:")
print(player_widget_link)
