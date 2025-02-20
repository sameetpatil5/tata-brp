from .modules.unit_conversion import unit_conversion
from .modules.phrase_detection import detect_phrases
from .modules.data_extractor import extract_phrases, extract_data
from .modules.chunking import batch_chunks, parse_chunks, bundle_chunks
from .modules.format_data import format_markdown
from .modules.llama_ocr import image_to_md
from .modules.preprocess_image import preprocess_image, save_image, load_image
from .modules.image_validation import validate_image

import pandas as pd
from pathlib import Path
import datetime as dt
import logging
from PIL import Image

logger = logging.getLogger(__name__)

class Processor:
    def __init__(self, file: str = None, markdown: str = None):
        """
        Initializes the Processor class for OCR processing.

        Args:
            file (str, optional): Path to the input image file.
            markdown (str, optional): Raw OCR output in markdown format.
        """
        self.file = file
        self.markdown = markdown
        self.image = None
        self.data = None

    def preprocess_image(self, image_path: str) -> str:
        """
        Preprocesses the image for better OCR performance.

        Args:
            image_path (str): Path of the image to be processed.
        
        Returns:
            str: File path of the preprocessed image.
        """
        logger.info(f"Preprocessing image...")
        logger.debug(f"Preprocessing image: {image_path}")
        preprocessed_image = preprocess_image(image=image_path)

        if validate_image(Image.fromarray(preprocessed_image)):
            self.image = preprocessed_image
            logger.info("Preprocessed image is valid. Using preprocessed image")
        else:
            self.image = load_image(image_path=image_path)
            logger.info("Preprocessed image is invalid. Using original image")

        BASE_DIR = Path(__file__).resolve().parent
        SAVE_DIR = BASE_DIR / "data/preprocessed"
        SAVE_DIR.mkdir(parents=True, exist_ok=True)

        timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y_%m_%d_%H_%M_%S")
        file_path = SAVE_DIR / f"{timestamp}.jpg"
        save_image(self.image, str(file_path))

        logger.info(f"Saved preprocessed image")
        logger.debug(f"Saved preprocessed image to: {file_path}")
        return str(file_path)

    def convert_image_to_markdown(self, image_path: str) -> None:
        """
        Converts an image to markdown using a vision model.

        Args:
            image_path (str): Path to the image file.
        """
        logger.info(f"Converting image to markdown...")
        logger.debug(f"Converting image to markdown: {image_path}")
        self.markdown = image_to_md(image_path=image_path)

    def perform_ocr(self, file_path: str = None) -> None:
        """
        Performs OCR on an image, applying preprocessing before conversion.

        Args:
            file_path (str, optional): Path of the image to be processed.
        """
        if self.file and file_path:
            raise ValueError("Either 'file' or 'file_path' should be provided, not both.")
        
        logger.info(f"Performing OCR on image...")
        logger.debug(f"Performing OCR on image: {file_path or self.file}")
        preprocessed_file_path = self.preprocess_image(file_path or self.file)
        self.convert_image_to_markdown(preprocessed_file_path)

    def set_markdown(self, markdown: str) -> None:
        """
        Sets the markdown content for processing.

        Args:
            markdown (str): Raw OCR markdown output.
        """
        logger.info("Setting OCR markdown content...")
        self.markdown = markdown

    def format_markdown(self, markdown: str) -> None:
        """
        Formats the OCR markdown content.

        Args:
            markdown (str): Raw OCR markdown output.
        """
        logger.info("Formatting markdown content...")
        self.markdown = format_markdown(markdown)

    def process_chunks(self) -> pd.DataFrame:
        """
        Processes chunks of text from the OCR markdown.

        Returns:
            pd.DataFrame: DataFrame containing processed text chunks.
        """
        logger.info("Processing text chunks from OCR markdown...")
        raw_chunks = batch_chunks(self.markdown)
        processed_chunks = [parse_chunks(chunk) for chunk in raw_chunks]
        bundled_chunks = bundle_chunks(processed_chunks)
        return bundled_chunks

    def detect_phrases(self, processed_chunks: pd.DataFrame) -> pd.DataFrame:
        """
        Detects meaningful phrases from processed chunks.

        Args:
            processed_chunks (pd.DataFrame): DataFrame containing text chunks.

        Returns:
            pd.DataFrame: DataFrame with extracted and classified phrases.
        """
        logger.info("Detecting phrases from processed chunks...")
        phrases = extract_phrases(processed_chunks)
        classified_phrases = detect_phrases(phrases)
        valid_phrases = {p: c for p, c in classified_phrases.items() if c != "Unknown"}
        extracted_data = extract_data(processed_chunks, valid_phrases)
        return extracted_data

    def convert_units(self, phrase_data: pd.DataFrame) -> pd.DataFrame:
        """
        Converts units in the extracted data.

        Args:
            phrase_data (pd.DataFrame): DataFrame with extracted data.

        Returns:
            pd.DataFrame: DataFrame with standardized units.
        """
        logger.info("Converting units in extracted data...")
        self.data = unit_conversion(phrase_data)
        return self.data

    def process(self) -> dict:
        """
        Runs the full OCR processing pipeline: formatting, chunking, phrase detection, and unit conversion.

        Returns:
            dict: Processed data with standardized units.
        """
        if not self.markdown:
            raise ValueError("OCR markdown is not set. Please provide the OCR data.")
        
        logger.info("Starting full OCR processing pipeline...")
        self.format_markdown(self.markdown)
        processed_chunks = self.process_chunks()
        phrase_data = self.detect_phrases(processed_chunks)
        self.data = self.convert_units(phrase_data)
        logger.info("OCR processing completed successfully")
        return self.data
