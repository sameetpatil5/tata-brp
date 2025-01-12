import requests
import pandas as pd

# Define the API endpoint
url = "http://127.0.0.1:5000/predict"
url = "http://127.0.0.1:5000/convert_units"

# Define the input data
data = {
    "phrases": ["cell count", "Lymphocyte count", "leucocytic count", "count", "Absolute neutrophil count "]
}
data = pd.read_csv('unit_conversion_module/unit_conv(from phrase detected).csv', index_col=0).to_json()

# Send the POST request
response = requests.post(url, json=data)

# Print the response
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
