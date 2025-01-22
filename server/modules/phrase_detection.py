from fuzzywuzzy import process
import json

def detect_phrases(input_phrases: list[str]) -> dict:
    """
    Classify a list of phrases based on a predefined classification dataset.

    Args:
        input_phrases (list[str]): List of phrases to classify.

    Returns:
        dict: A dictionary mapping input phrases to their classifications or "Unknown" if no match is found.
    """
    with open("data/phrase_data/phrase.json", "r") as phrase_file, \
         open("data/phrase_data/common_phrases.txt", "r") as common_phrases_file, \
         open("data/phrase_data/valid_short_terms.txt", "r") as valid_short_terms_file:

        # Load classification data and auxiliary term sets.
        classification_dict = json.load(phrase_file)
        common_terms = set(common_phrases_file.read().lower().split(","))
        valid_short_terms = set(valid_short_terms_file.read().lower().split(","))

        # Create a reverse mapping for classification.
        phrase_to_key = {
            phrase.lower(): key
            for key, phrases in classification_dict.items()
            for phrase in phrases
        }

        # Initialize the classification result dictionary.
        classification_results = {}

        for phrase in input_phrases:
            normalized_phrase = phrase.lower().strip()  # Normalize input.

            if not normalized_phrase:  # Skip empty phrases.
                classification_results[phrase] = "Unknown"
                continue

            if normalized_phrase in common_terms:  # Check for common terms.
                classification_results[phrase] = "Unknown"
                continue

            if normalized_phrase in valid_short_terms:  # Check for valid short terms.
                classification_results[phrase] = phrase_to_key.get(normalized_phrase, "Unknown")
                continue

            if normalized_phrase in phrase_to_key:  # Exact match in dataset.
                classification_results[phrase] = phrase_to_key[normalized_phrase]
                continue

            # Use fuzzy matching for approximate matches.
            closest_match, score = process.extractOne(normalized_phrase, phrase_to_key.keys())
            if score > 90:  # Threshold for fuzzy matching.
                classification_results[phrase] = phrase_to_key[closest_match]
            else:
                classification_results[phrase] = "Unknown"

        return classification_results