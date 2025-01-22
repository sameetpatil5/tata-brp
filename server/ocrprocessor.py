from .modules.unit_conversion import unit_conversion
from .modules.phrase_detection import detect_phrases
from .modules.data_extractor import extract_phrases, extract_data
from .modules.chunking import batch_chunks, parse_chunks, bundle_chunks
from .modules.format_data import format_markdown

class OCRProcessor:
    def __init__(self, ocr_markdown=None):
        """
        Initializes the OCRProcessor with the OCR markdown input.

        Args:
            ocr_markdown (str): Raw OCR output in markdown format.
        """
        self.ocr_markdown = ocr_markdown
        self.data_packet = None

    def set_markdown(self, ocr_markdown):
        """
        Sets the OCR markdown input for the OCRProcessor.

        Args:
            ocr_markdown (str): Raw OCR output in markdown format.
        """
        self.ocr_markdown = ocr_markdown

    def format_markdown(self, ocr_markdown):
        """
        Formats the OCR markdown input for the OCRProcessor.

        Args:
            ocr_markdown (str): Raw OCR output in markdown format.
        """
        self.ocr_markdown = format_markdown(ocr_markdown)

    def process_chunks(self):
        """
        Identifies and processes chunks of text from the OCR markdown.

        Returns:
            pd.DataFrame: A bundled DataFrame containing all processed chunks.
        """
        raw_chunks = batch_chunks(self.ocr_markdown)  # Identify text chunks from OCR data.
        processed_chunks = []

        for chunk in raw_chunks:
            processed_chunks.append(parse_chunks(chunk))  # Parse each chunk into structured data.

        # Bundle all processed chunks into a single DataFrame.
        return bundle_chunks(processed_chunks)

    def detect_phrases(self, processed_chunks):
        """
        Detects and classifies meaningful phrases from processed chunks.

        Args:
            processed_chunks (pd.DataFrame): DataFrame containing processed text chunks.

        Returns:
            pd.DataFrame: DataFrame with extracted and classified phrases.
        """
        phrases = extract_phrases(processed_chunks)  # Extract phrases from the chunks.
        classified_phrases = detect_phrases(phrases)  # Classify the phrases into categories.

        # Filter out phrases classified as "Unknown".
        valid_phrases = {phrase: classification for phrase, classification in classified_phrases.items() if classification != "Unknown"}

        # Extract relevant data based on the valid phrases.
        return extract_data(processed_chunks, valid_phrases)

    def convert_units(self, phrase_data):
        """
        Converts the units of the extracted data to standard units.

        Args:
            phrase_data (pd.DataFrame): DataFrame with columns 'Test', 'Result', and 'Unit'.

        Returns:
            pd.DataFrame: DataFrame with converted units in the 'Result' column.
        """
        return unit_conversion(phrase_data)

    def process_ocr(self):
        """
        Executes the entire OCR processing pipeline: chunk processing, phrase detection,
        and unit conversion. Updates the data_packet attribute with the results.

        Returns:
            pd.DataFrame: Final processed data with standardized units.
        """

        if not self.ocr_markdown:
            raise ValueError("OCR markdown is not set. Please provide the OCR data.")

        # Format the OCR markdown.
        self.format_markdown(self.ocr_markdown)

        # Process the OCR markdown into structured chunks.
        processed_chunks = self.process_chunks()

        # Detect and classify phrases from the processed chunks.
        phrase_data = self.detect_phrases(processed_chunks)

        # Convert units in the extracted phrase data.
        self.data_packet = self.convert_units(phrase_data)

        return self.data_packet
