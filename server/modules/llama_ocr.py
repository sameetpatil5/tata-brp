from together import Together
import base64
import os
import logging

logger = logging.getLogger(__name__)

def image_to_md(image_path: str, api_key: str = None, model: str = "Llama-3.2-90B-Vision") -> str:
    """
    Convert an image into Markdown format using Together AI's vision model.

    Args:
        image_path (str): Path to the image file (local or remote URL).
        api_key (str, optional): Together AI API key. Defaults to environment variable TOGETHER_API_KEY.
        model (str, optional): Model to use ("Llama-3.2-90B-Vision", "Llama-3.2-11B-Vision", or "free").

    Returns:
        str: Extracted content in Markdown format.
    """

    if api_key is None:
        api_key = os.getenv("TOGETHER_API_KEY")
        logger.info("TOGETHER_API_KEY loaded from environment")

    vision_llm = (
        "meta-llama/Llama-Vision-Free"
        if model == "free"
        else f"meta-llama/{model}-Instruct-Turbo"
    )

    logger.info(f"Vision model {vision_llm} loaded ")

    try:

        client = Together(api_key=api_key)

        # Prepare image for API request
        final_image_url = image_path if is_remote_file(image_path) else encode_image(image_path)
        logger.info("Image URL loaded")
        logger.debug(f"Packed image in a final URL: {final_image_url[:50]}...")

        system_prompt = """Convert the provided image into Markdown format. 
        Ensure that all content from the page is included, such as headers, footers, subtexts, images (with alt text if possible), tables, and any other elements.

        Requirements:
        - Output Only Markdown: Return solely the Markdown content without any additional explanations or comments.
        - No Delimiters: Do not use code fences or delimiters like ```markdown.
        - Complete Content: Do not omit any part of the page, including headers, footers, and subtext.
        """

        response = client.chat.completions.create(
            model=vision_llm,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": system_prompt},
                        {"type": "image_url", "image_url": {"url": final_image_url}},
                    ],
                }
            ],
        )

        markdown = response.choices[0].message.content
        
        logger.info("Response successfully recieved from TogetherAI vision model")
        logger.debug(f"Response content: \n{markdown}")

        return markdown
    except Exception as e:
        logger.error(f"Error while converting image to markdown: {e}")
        return ""


def encode_image(image_path: str) -> str:
    """Encodes an image to base64 format."""
    try:
        logger.info("Encoding local file")
        with open(image_path, "rb") as image_file:
            encoded_image = f"data:image/jpeg;base64,{base64.b64encode(image_file.read()).decode('utf-8')}"
            logger.info("Successfully encoded the image")
            return encoded_image
    except Exception as e:
        logger.error(f"Error while encoding the image: {e}")

def is_remote_file(image_path: str) -> bool:
    """Checks if a file path is a remote URL."""
    try:
        is_remote = image_path.startswith("http://") or image_path.startswith("https://")
        logger.info("File is remote" if is_remote else "File is local")
        return is_remote
    except Exception as e:
        logger.error(f"Error while checking if the file is remote: {e}")

# Example usage:
if __name__ == "__main__":
    image_path = "E:/SAM ENGINEERINGs/TATA BRP/data/test_image.jpg"
    result = image_to_md(image_path)
    print(result)

