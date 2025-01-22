import requests

# Define the API endpoint
API_URL = "http://127.0.0.1:8000/ocr/process"

# Path to the markdown file
MARKDOWN_FILE_PATH = "./data/test_ocr.md"

def test_api():
    try:
        # Read the markdown content from the file
        with open(MARKDOWN_FILE_PATH, "r") as file:
            markdown_content = file.read()

        # Prepare the payload
        payload = {"markdown": markdown_content}

        # Send a POST request to the API
        response = requests.post(API_URL, json=payload)

        # Print the response
        if response.status_code == 200:
            print("API Response:")
            print(response.json())
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)

    except FileNotFoundError:
        print(f"Error: File not found at {MARKDOWN_FILE_PATH}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_api()
