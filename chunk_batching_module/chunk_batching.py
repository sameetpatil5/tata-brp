# from markdown_it import MarkdownIt
# from mdit_py_plugins.front_matter import front_matter_plugin
# from mdit_py_plugins.footnote import footnote_plugin
# from bs4 import BeautifulSoup
# import pandas as pd

# md = (
#     MarkdownIt('commonmark' ,{'breaks':True,'html':True})
#     .use(front_matter_plugin)
#     .use(footnote_plugin)
#     .enable('table')
# )

# with open('my_datasets/test_chunk.md', 'r') as file:
#     text = file.read()

# tokens = md.parse(text)
# html_text = md.render(text)

# # print(tokens)
# print(html_text)

# # Your HTML content
# html_content = html_text

# # Parse the HTML
# soup = BeautifulSoup(html_content, 'html.parser')

# # Extract tables
# tables = soup.find_all('table')
# dataframes = []

# for table in tables:
#     # Extract table headers
#     print(table)
#     headers = [th.get_text(strip=True) for th in table.find_all('th')]
    
#     # Extract table rows
#     rows = []
#     for row in table.find_all('tr')[1:]:  # Skip the header row
#         cols = [td.get_text(strip=True) for td in row.find_all('td')]
#         rows.append(cols)
    
#     # Convert to DataFrame
#     if rows:
#         df = pd.DataFrame(rows, columns=headers)
#         dataframes.append(df)

# # Combine header DataFrame and table DataFrames
# final_dataframes = dataframes

# # Display the results
# for idx, df in enumerate(final_dataframes):
#     print(f"DataFrame {idx}:\n{df}\n")
import re

def identify_chunks(md_content):
    """
    Identify and separate tables and paragraphs from markdown content.

    Args:
        md_content (str): The markdown content.

    Returns:
        list: A list of dictionaries with `type` (table or paragraph) and `content`.
    """
    chunks = []
    table_pattern = re.compile(r"\|.*?\|\n(?:\|.*?\|\n)*")

    position = 0
    for match in table_pattern.finditer(md_content):
        # # Capture paragraph before the table
        # if position < match.start():
        #     paragraph = md_content[position:match.start()].strip()
        #     if paragraph:
        #         chunks.append({"type": "paragraph", "content": paragraph})
        
        # Capture the table
        table = match.group().strip()
        chunks.append({"type": "table", "content": table})
        position = match.end()

    # # Capture any remaining paragraph
    # if position < len(md_content):
    #     paragraph = md_content[position:].strip()
    #     if paragraph:
    #         chunks.append({"type": "paragraph", "content": paragraph})

    return chunks

if __name__ == "__main__":
    with open("my_datasets/test_chunk.md", "r") as file:
        md_content = file.read()
    
    chunks = identify_chunks(md_content)
    for chunk in chunks:
        print(chunk)
