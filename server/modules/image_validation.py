import google.generativeai as genai
from dotenv import load_dotenv
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configure the Generative AI model
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

def validate_image(image: Image) -> bool:
    try:
        logger.info("Validating image...")
        # Define the AI model to use
        MODEL_NAME = "gemini-2.0-flash-exp"
        model = genai.GenerativeModel(MODEL_NAME)
        logger.info(f"Model {MODEL_NAME} loaded")

        # Define the AI prompt
        prompt = "You are given a preprocessed image of a blood report. Analyze whether the preprocessing has maintained its medical readability. If the preprocessing has made the image an unusable mess from which no medical information can be inferred, respond only with 'invalid'. If the image remains perfectly readable and useful for medical purposes, respond only with 'valid'. Do not provide any explanation or additional text."

        response = model.generate_content([prompt, image])
        is_valid = response.text
        logger.info("Image validation complete")

        if is_valid == 'valid':
            logger.info("Image is marked valid")
            logger.debug(f"AI reponse: {is_valid}")
            return True
        else:
            logger.error("Image is marked invalid")
            logger.debug(f"AI reponse: {is_valid}")
            return False
    except Exception as e:
        logger.error(f"Error while validating Image: {e}")
        return False
    
if __name__ == "__main__":
    image = Image.open("E:/SAM ENGINEERINGs/TATA BRP/tests/processed_image.jpg")

    if validate_image(image=image):
        print("Image is valid!")
    else:
        print("Image is invalid!")
    