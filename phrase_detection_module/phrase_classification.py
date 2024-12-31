from fuzzywuzzy import process
from my_datasets.phrase_datasets.phrase import *

# Function to classify a phrase
def classify_phrase(input_phrases: list[str]) -> str:
    # Flatten the dictionary for reverse mapping
    phrase_to_key = {phrase.lower(): key for key, phrases in classification_dict.items() for phrase in phrases}

    # Dictionary to store the classification
    input_classification_dict = {}

    for phrase in input_phrases:
        phrase = phrase.lower().strip()  # Normalize input
        
        # Check if the phrase is too short or contains common terms
        if len(phrase.split()) < 2:
            # Check if it's a valid short term
            if phrase in valid_short_terms:
                input_classification_dict[phrase] = phrase_to_key.get(phrase, "Unknown")
            input_classification_dict[phrase] = "Unknown"
        
        # Check if the phrase is just a common term
        if any(common_term for common_term in common_terms if common_term == phrase):
            input_classification_dict[phrase] = "Unknown"
        
        # Find the closest match
        closest_match, score = process.extractOne(phrase, phrase_to_key.keys())
        # Set a threshold for accuracy
        if score > 80:
            input_classification_dict[phrase] = phrase_to_key[closest_match]
        else:
            input_classification_dict[phrase] = "Unknown"

classify_phrase(["Total leukocyte count"])