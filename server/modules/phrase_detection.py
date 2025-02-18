from fuzzywuzzy import process
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - Line %(lineno)d: %(message)s"
)
logger = logging.getLogger(__name__)

def detect_phrases(input_phrases: list[str]) -> dict:
    """
    Classify a list of phrases based on a predefined classification dataset.

    Args:
        input_phrases (list[str]): List of phrases to classify.

    Returns:
        dict: A dictionary mapping input phrases to their classifications or "Unknown" if no match is found.
    """
    logger.info("Loading classification data from JSON and text files...")

    try:
        with open("data/phrase_data/phrase.json", "r") as phrase_file, \
             open("data/phrase_data/common_phrases.txt", "r") as common_phrases_file, \
             open("data/phrase_data/valid_short_terms.txt", "r") as valid_short_terms_file:

            classification_dict = json.load(phrase_file)
            common_terms = set(common_phrases_file.read().lower().split(","))
            valid_short_terms = set(valid_short_terms_file.read().lower().split(","))
    except Exception as e:
        logger.error("Error loading classification data: %s", str(e))
        return {}

    logger.info("Successfully loaded classification data.")

    # Create a reverse mapping for classification.
    phrase_to_key = {
        phrase.lower(): key
        for key, phrases in classification_dict.items()
        for phrase in phrases
    }

    classification_results = {}

    logger.info("Processing %d input phrases...", len(input_phrases))

    for phrase in input_phrases:
        normalized_phrase = phrase.lower().strip()

        if not normalized_phrase:  # Skip empty phrases.
            logger.debug("Skipping empty phrase.")
            classification_results[phrase] = "Unknown"
            continue

        logger.debug("Processing phrase: '%s'", phrase)

        if normalized_phrase in common_terms:  # Check for common terms.
            logger.info("Phrase '%s' is a common term. Classified as 'Unknown'.", phrase)
            classification_results[phrase] = "Unknown"
            continue

        if normalized_phrase in valid_short_terms:  # Check for valid short terms.
            classification_results[phrase] = phrase_to_key.get(normalized_phrase, "Unknown")
            logger.info("Phrase '%s' matched as a valid short term. Classified as '%s'.",
                        phrase, classification_results[phrase])
            continue

        if normalized_phrase in phrase_to_key:  # Exact match in dataset.
            classification_results[phrase] = phrase_to_key[normalized_phrase]
            logger.info("Exact match found for '%s'. Classified as '%s'.",
                        phrase, classification_results[phrase])
            continue

        # Use fuzzy matching for approximate matches.
        closest_match, score = process.extractOne(normalized_phrase, phrase_to_key.keys())

        if score > 90:  # Threshold for fuzzy matching.
            classification_results[phrase] = phrase_to_key[closest_match]
            logger.info("Fuzzy match: '%s' -> '%s' (score: %d). Classified as '%s'.",
                        phrase, closest_match, score, classification_results[phrase])
        else:
            classification_results[phrase] = "Unknown"
            logger.info("No good match found for '%s' (best fuzzy score: %d). Classified as 'Unknown'.",
                        phrase, score)

    logger.info("Phrase classification completed.")
    return classification_results