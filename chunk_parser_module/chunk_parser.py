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
        lines = soup.find("p").text.splitlines()
        rows = [line.strip("|").strip().split("|") for line in lines if "|" in line.strip()]

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
