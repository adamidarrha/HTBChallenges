import os
from dotenv import load_dotenv
import json
import httpx

#have 40 files

# Try to load existing data
try:
    with open('filenames.json', 'r') as f:
        id_to_filename = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    id_to_filename = {}

print(f"this is {len(id_to_filename)}")

load_dotenv()

# Get API token from environment variable
token = os.getenv("TOKEN")

print(token)

# Replace with the actual base URL of the API
base_url = "https://labs.hackthebox.com/api/v4/challenge/download/"

headers = {
    "Authorization": f"Bearer {token}"
}

# Loop through IDs from 0 to 300
for i in range(400, 500):
    # Construct the URL with the current ID
    url = f"{base_url}{i}"

    client = httpx.Client(http2=True)
    response = client.get(url, headers=headers)

    if(response.status_code != 200):
        print(f"Failed to download file with ID {i}")
        continue

    print(response)

    # Check if the 'Content-Disposition' header is present
    if 'Content-Disposition' in response.headers:
        # Extract the filename from the header
        content_disposition = response.headers['Content-Disposition']
        filename = content_disposition.split('filename=')[-1].strip('"')

        # Store the filename in the dictionary
        id_to_filename[i] = filename
        print(f"Downloaded file with ID {i} and filename {filename}")

# Write the results to a JSON file
with open('filenames.json', 'w') as file:
    json.dump(id_to_filename, file)

print("Finished. The filenames have been saved to filenames.json.")
