from bs4 import BeautifulSoup
import pandas as pd

def parse_chunk_to_dataframe(chunk: str) -> pd.DataFrame:
    """
    Parses an HTML or Markdown-like chunk into a pandas DataFrame.
    Handles cases where headers are missing by adding placeholder headers.

    Parameters:
        chunk (str): The HTML or Markdown-like input string.

    Returns:
        pd.DataFrame: The resulting DataFrame.
    """
    # Try parsing as HTML table first
    soup = BeautifulSoup(chunk, "html.parser")
    table = soup.find("table")

    if table:
        # Extract table headers if present
        headers = [header.text.strip() for header in table.find_all("th")]

        # Extract table rows
        rows = []
        for row in table.find_all("tr"):
            cells = [cell.text.strip() for cell in row.find_all(["td", "th"])]
            rows.append(cells)

        # Ensure headers are present, add placeholders if missing
        if not headers:
            headers = [f"Column {i+1}" for i in range(len(rows[0]))]

        # Create the DataFrame
        df = pd.DataFrame(rows[1:], columns=headers)
        return df

    # If no table, try parsing Markdown-like pipe-delimited text
    elif "|" in chunk:
        lines = chunk.splitlines()
        rows = [line.strip(" ").strip("|").split("|") for line in lines if "|" in line.strip()]

        print(rows)

        # Ensure all rows have the same number of columns
        max_columns = max(len(row) for row in rows)
        rows = [row + ["" for _ in range(max_columns - len(row))] for row in rows]

        # Extract headers if the first row looks like a header row
        headers = rows[0] if all(cell.isalpha() or cell.isspace() for cell in rows[0]) else []

        # Add placeholder headers if none exist
        if not headers:
            headers = [f"Column {i+1}" for i in range(len(rows[0]))]

        # Skip the header row if it was detected as headers
        data = rows[1:] if headers == rows[0] else rows

        # Create the DataFrame
        df = pd.DataFrame(data, columns=headers)
        return df

    else:
        raise ValueError("The input chunk is not in a recognizable format.")

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

# # Parse HTML chunk
# df_html = parse_chunk_to_dataframe(html_chunk)
# print("HTML Chunk DataFrame:")
# print(df_html)

# Parse Markdown-like chunk
df_markdown = parse_chunk_to_dataframe(markdown_chunk)
print("\nMarkdown Chunk DataFrame:")
print(df_markdown)
