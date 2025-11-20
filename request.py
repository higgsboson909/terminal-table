import requests
import json
import os

def download_json_file(url, output_filename="downloaded_data.json"):
    """
    Downloads a file from a given URL and saves the content as a JSON file.
    
    Args:
        url (str): The URL of the JSON file to download.
        output_filename (str): The name for the local file to save the data to.
    """
    try:
        # 1. Send an HTTP GET request
        print(f"Attempting to download from: {url}")
        response = requests.get(url, stream=True)
        
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()
        
        # 2. Check content type (optional but good practice)
        content_type = response.headers.get('Content-Type', '')
        if 'application/json' not in content_type and 'text/json' not in content_type:
            print(f"Warning: Content-Type is '{content_type}', not standard JSON.")
        
        # 3. Process and save the JSON content
        
        # Decode the JSON data from the response text
        json_data = response.json()
        
        # Write the JSON data to a local file
        with open(output_filename, 'w', encoding='utf-8') as f:
            # Use json.dump for clean, readable output
            json.dump(json_data, f, indent=4)
        
        print(f"\n✅ Success! JSON data saved to '{output_filename}'")
        print(f"File size: {os.path.getsize(output_filename)} bytes")

    except requests.exceptions.RequestException as e:
        print(f"\n❌ An error occurred during the request: {e}")
    except json.JSONDecodeError:
        print("\n❌ Failed to decode response as JSON. The file might be corrupted or not valid JSON.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")

# --- Configuration ---
# Replace this URL with the actual path to your JSON file
JSON_URL = "https://griffin-k.github.io/Time-Table-Actions/read-data.json" 
# Example URL returns: {"userId": 1, "id": 1, "title": "delectus aut autem", "completed": false}

if __name__ == "__main__":
    download_json_file(JSON_URL, "data.json")
