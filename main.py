import requests

# Define the API endpoint
# url = "http://127.0.0.1:5000/classify"  # Correct endpoint
url = "http://127.0.0.1:5000/parse_chunk"  

# Define the input data
# data = {
#     "phrases": ["cell count", "Lymphocyte count", "leucocytic count", "count", "Absolute neutrophil count "]
# }

# Example usage
html_chunk = """
<h3>Complete Blood Count</h3>
<table>
<thead>
<tr>
<th><strong>Tests</strong></th>
<th><strong>Results</strong></th>
<th><strong>Unit</strong></th>
<th><strong>Reference Range</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Haemoglobin</td>
<td>11.3</td>
<td>gm/dl</td>
<td>14 - 18</td>
</tr>
<tr>
<td>R.B.C. Count</td>
<td>3.82</td>
<td>mil./cu.mm</td>
<td>4.5 - 6.5</td>
</tr>
<tr>
<td>Total WBC Count</td>
<td>5800</td>
<td>/cmm</td>
<td>4000 - 10000</td>
</tr>
<tr>
<td>Platelets</td>
<td>246000</td>
<td>/cmm</td>
<td>150000 - 450000</td>
</tr>
</tbody>
</table>
"""

markdown_chunk = """
<h3>Complete Blood Count</h3>
<p>| Haemoglobin         | 11.3        | gm/dl          | 14 - 18             |<br />
| R.B.C. Count        | 3.82        | mil./cu.mm     | 4.5 - 6.5           |<br />
| Total WBC Count     | 5800        | /cmm           | 4000 - 10000        |<br />
| Platelets           | 246000      | /cmm           | 150000 - 450000     |</p>
"""

data = {"chunk": html_chunk}

# Send the POST request
response = requests.post(url, json=data)

# Print the response
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
