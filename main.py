import requests

# Define the API endpoint
url = "http://127.0.0.1:5000/predict"

# Define the input data
data = {
    "phrases": ["cell count", "Lymphocyte count", "leucocytic count", "count", "Absolute neutrophil count "]
}

# Send the POST request
response = requests.post(url, json=data)

# Print the response
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
