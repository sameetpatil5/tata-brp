import markdown
from markdown_it import MarkdownIt
import markdown_it
# with open("unit_conversion_module/test.md", "r") as f:
#     content = f.read()

# text_md = markdown.markdown(content)
# print(text_md)

md = (
    MarkdownIt('commonmark' ,{'breaks':True,'html':True})
    # .use(markdown_it.front_matter_plugin)
    # .use(markdown_it.footnote_plugin)
    .enable('table')
)
text = ("""
### Complete Blood Count  

| Haemoglobin         | 11.3        | gm/dl          | 14 - 18             |
| R.B.C. Count        | 3.82        | mil./cu.mm     | 4.5 - 6.5           |
| Total WBC Count     | 5800        | /cmm           | 4000 - 10000        |
| Platelets           | 246000      | /cmm           | 150000 - 450000     |
""")
tokens = md.parse(text)
html_text = md.render(text)

# html_text = """
# <h3>Complete Blood Count</h3>
# <table>
# <thead>
# <tr>
# <th><strong>Tests</strong></th>
# <th><strong>Results</strong></th>
# <th><strong>Unit</strong></th>
# <th><strong>Reference Range</strong></th>
# </tr>
# </thead>
# <tbody>
# <tr>
# <td>Haemoglobin</td>
# <td>11.3</td>
# <td>gm/dl</td>
# <td>14 - 18</td>
# </tr>
# <tr>
# <td>R.B.C. Count</td>
# <td>3.82</td>
# <td>mil./cu.mm</td>
# <td>4.5 - 6.5</td>
# </tr>
# <tr>
# <td>Total WBC Count</td>
# <td>5800</td>
# <td>/cmm</td>
# <td>4000 - 10000</td>
# </tr>
# <tr>
# <td>Platelets</td>
# <td>246000</td>
# <td>/cmm</td>
# <td>150000 - 450000</td>
# </tr>
# </tbody>
# </table>
# """

# from bs4 import BeautifulSoup
# import pandas as pd

# # Parse the HTML
# soup = BeautifulSoup(html_text, "html.parser")

# # Extract table headers
# headers = [header.text.strip() for header in soup.find_all("th")]

# # Extract table rows
# rows = []
# for row in soup.find_all("tr")[1:]:  # Skip the header row
#     cells = [cell.text.strip() for cell in row.find_all("td")]
#     rows.append(cells)

# # Create a pandas DataFrame
# df = pd.DataFrame(rows, columns=headers)
# print(df)

print(html_text)


# HTML input with OCR-chunked data
html_text_ocr = """
<h3>Complete Blood Count</h3>
<p>| Haemoglobin         | 11.3        | gm/dl          | 14 - 18             |<br />
| R.B.C. Count        | 3.82        | mil./cu.mm     | 4.5 - 6.5           |<br />
| Total WBC Count     | 5800        | /cmm           | 4000 - 10000        |<br />
| Platelets           | 246000      | /cmm           | 150000 - 450000     |</p>
"""

# Parse the HTML
soup_ocr = BeautifulSoup(html_text_ocr, "html.parser")

# Extract the data rows from the OCR chunk
ocr_data = soup_ocr.find("p").text.splitlines()

# Clean and split the rows into columns
rows_ocr = [line.strip("|").strip().split("|") for line in ocr_data if line.strip()]

# Fill headers with empty placeholders if not provided
headers_ocr = [f"Column {i+1}" for i in range(len(rows_ocr[0]))]

# Create a pandas DataFrame
df_ocr = pd.DataFrame(rows_ocr, columns=headers_ocr)
df_ocr
