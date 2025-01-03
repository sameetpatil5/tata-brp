from fuzzywuzzy import process
import json

# Function to classify a phrase
def classify_phrase(input_phrases: list[str]) -> str:
    with open("my_datasets/phrase_datasets/phrase.json", "r") as phrase_file, open("my_datasets/phrase_datasets/common_phrases.txt", "r") as common_phrases_file, open("my_datasets/phrase_datasets/valid_short_terms.txt", "r") as valid_short_terms_file:

        # Define the classification dictionary
        classification_dict = json.load(phrase_file)

        # Common terms that should be considered as "Unknown"
        common_terms = set(common_phrases_file.read().split(","))

        # Valid short terms that should be classified correctly
        valid_short_terms = set(valid_short_terms_file.read().split(","))

        # Flatten the dictionary for reverse mapping
        phrase_to_key = {phrase.lower(): key for key, phrases in classification_dict.items() for phrase in phrases}

        # Dictionary to store the classification
        input_classification_dict = {}

        for phrase in input_phrases:
            phrase = phrase.lower().strip()  # Normalize input
            
            # Check if the phrase is just a common term
            if phrase in common_terms:
                input_classification_dict[phrase] = "Unknown"
                continue

            # Check if the phrase is too short or contains common terms
            if len(phrase.split()) < 2:
                # Check if it's a valid short term
                if phrase in valid_short_terms:
                    input_classification_dict[phrase] = phrase_to_key.get(phrase, "Unknown")
                else:
                    input_classification_dict[phrase] = "Unknown"
                continue

            # Find the closest match
            closest_match, score = process.extractOne(phrase, phrase_to_key.keys())
            # Set a threshold for accuracy
            if score > 80:
                input_classification_dict[phrase] = phrase_to_key[closest_match]
            else:
                input_classification_dict[phrase] = "Unknown"

        return input_classification_dict