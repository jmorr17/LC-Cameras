import requests
from datetime import datetime, timedelta
import os

# Replace with your actual API URL
api_url = "https://app-api.frosttech.io/location/getByGroupAPIKey"
api_key = "API_KEY"  # Store this securely in GitHub Secrets

# Define the locations
locations = ["467b2df2-7466-4c03-acea-2bf918994c47", "6cd567b7-1e15-40b9-8c52-b4d5ed8b6892", "9901653b-734b-43c7-9c4e-253506e9b665", "9f39b736-a675-491b-ba5c-6d1ab45c96eb", "5b061389-5e7a-49f1-9048-9c0bec194f5c"]

# Calculate the current time and the time 30 minutes ago
end_time = datetime.utcnow()
start_time = end_time - timedelta(minutes=30)

# Convert times to strings in the format the API expects (e.g., "2025-02-04T15:00:00Z")
start_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
end_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

# Directory to save images
save_path = "snapshots/"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Fetch snapshots for each location
for location in locations:
    # Set up parameters for the GET request
    params = {
        'start': start_str,
        'end': end_str,
        'includeImages': 'true',
        'location': location
    }

    headers = {
        'Authorization': f"Bearer {api_key}"
    }

    # Send the GET request
    response = requests.get(api_url, headers=headers, params=params)

    if response.status_code == 200:
        # Assuming the response contains an image URL (adjust according to actual API response structure)
        image_url = response.json().get('image_url')  # Adjust based on actual API response

        if image_url:
            # Download the image
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                # Save the image with a unique filename based on location and timestamp
                filename = f"{location}_{start_time.strftime('%Y%m%d%H%M%S')}.jpg"
                with open(os.path.join(save_path, filename), 'wb') as f:
                    f.write(image_response.content)
                print(f"Snapshot for {location} saved as {filename}")
            else:
                print(f"Failed to download image for {location}.")
        else:
            print(f"No image URL found for {location}.")
    else:
        print(f"Failed to retrieve data for {location}. HTTP Status Code: {response.status_code}")

