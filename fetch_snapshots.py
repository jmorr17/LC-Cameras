import requests
from datetime import datetime, timedelta
import os

# Get the API key from the environment variable set in GitHub Actions
api_key = os.getenv("API_KEY")  # Fetch API key from GitHub Secrets

# Define the list of locations with a name for each
locations = [
    {"LocationID": "467b2df2-7466-4c03-acea-2bf918994c47", "name": "Leadville Junction"},
    {"LocationID": "6cd567b7-1e15-40b9-8c52-b4d5ed8b6892", "name": "Fire Station 2"},
    {"LocationID": "9901653b-734b-43c7-9c4e-253506e9b665", "name": "Halfmoon"},
    {"LocationID": "9f39b736-a675-491b-ba5c-6d1ab45c96eb", "name": "Twin Lakes Shop"},
    {"LocationID": "5b061389-5e7a-49f1-9048-9c0bec194f5c", "name": "Huck Finn Park"}
]


locations_url = "https://app-api.frosttech.io/location/getByGroupAPIKey"

# Set headers for authentication
headers = {
    'GroupAPIKey': api_key
}

# Calculate the current time and the time 30 minutes ago (UTC format)
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=30)

# Convert times to ISO 8601 strings in UTC format (e.g., "2025-02-04T15:00:00Z")
start_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
end_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')

# Directory to save images
save_path = "snapshots/"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# 2. Fetch data for each location
for location_id in locations:
    # Set up parameters for the GET request to fetch sensor data
    data_url = f"https://app-api.frosttech.io/locationDataTransmission/getByGroupAPIKey"
    params = {
        'locationID': location_id,
        'start': start_str,
        'end': end_str,
        'includeImages': 'true',  # Include images as per API docs
        'includeForecast': 'false'  # If you don't need forecast data
    }

    # Send the GET request
    data_response = requests.get(data_url, headers=headers, params=params)
    
    if data_response.status_code == 200:
        # The API response contains a list (not a dictionary)
        data = data_response.json()
    
        print(f"API Response for {location_id}: {data}")  # Print the full API response for inspection
    
        # Iterate through the list and look for the 'image_url' key
    for item in data:
        image_url = item.get('ImageUrl')  # Adjusting for the correct key name
    
        if image_url:
            # Download the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Save the image with a unique filename based on location and timestamp
                filename = f"{location_id}_{start_time.strftime('%Y%m%d%H%M%S')}.jpg"
                with open(os.path.join(save_path, filename), 'wb') as f:
                    f.write(image_response.content)
                print(f"Snapshot for {location_id} saved as {filename}")
            else:
                print(f"Failed to download image for {location_id}.")
        else:
            print(f"No image URL found for {location_id}.")
    else:
        print(f"Failed to retrieve data for {location_id}. HTTP Status Code: {data_response.status_code}")

