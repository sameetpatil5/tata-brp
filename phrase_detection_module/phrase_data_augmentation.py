import csv, json
import random
from nltk.corpus import wordnet
from phrase_detection_module_constants import *

def get_synonyms(word: str) -> list:
    """
    Get synonyms for a given word using WordNet.

    Args:
        word (str): The word for which synonyms are to be fetched.

    Returns:
        list: A list of synonyms for the given word. If no synonyms are found, returns an empty list.
    """
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

def augment_phrase(phrase: str, medical_synonyms: dict, use_medical_synonyms: bool, num_augmentations: int = AUGMENTATION_VARIANCE) -> list:
    """
    Generate augmented variations of a phrase by replacing words with synonyms.

    Args:
        phrase (str): The original phrase to augment.
        medical_synonyms (dict): A dictionary of medical synonyms.
        use_medical_synonyms (bool): Whether to use medical synonyms for augmentation.
        num_augmentations (int): The number of augmented phrases to generate.

    Returns:
        list: A list of augmented phrases.
    """
    words = phrase.split()
    augmented_phrases = set()

    for _ in range(num_augmentations):
        new_words = words[:]
        for i, word in enumerate(words):
            # Use medical synonyms if enabled and available
            if use_medical_synonyms and word.lower() in medical_synonyms:
                new_words[i] = random.choice(medical_synonyms[word.lower()])
            else:
                nltk_synonyms = get_synonyms(word.lower())
                if nltk_synonyms:
                    new_words[i] = random.choice(nltk_synonyms)
        augmented_phrases.add(' '.join(new_words))

    return list(augmented_phrases)

def augment_dataset(input_csv: str, output_csv: str, medical_synonyms_path: str, use_medical_synonyms: bool) -> None:
    """
    Augment the dataset by generating variations of each phrase and saving the augmented data.

    Args:
        input_csv (str): Path to the input CSV file containing phrases and categories.
        output_csv (str): Path to the output CSV file to save augmented data.
        medical_synonyms_path (str): Path to the medical synonyms JSON file.
        use_medical_synonyms (bool): Whether to use medical synonyms for augmentation.

    Returns:
        None: Writes the augmented data to the specified output CSV file.
    """
    augmented_data = []
    unique_phrases = set()

    # Load medical synonyms if required
    medical_synonyms = {}
    if use_medical_synonyms:
        with open(medical_synonyms_path, 'r') as file:
            medical_synonyms = json.load(file)


    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        augmented_data.append(header)

        for row in reader:
            phrase, category = row
            augmented_phrases = augment_phrase(phrase, medical_synonyms, use_medical_synonyms)

            # Always add the original phrase
            if phrase not in unique_phrases:
                augmented_data.append([phrase, category])
                unique_phrases.add(phrase)

            # Add only unique phrases (based on phrase content)
            for augmented_phrase in augmented_phrases:
                if augmented_phrase not in unique_phrases:
                    augmented_data.append([augmented_phrase, category])
                    unique_phrases.add(augmented_phrase)

    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerows(augmented_data)

# Augment dataset
augment_dataset(
    PHRASE_DATASET, 
    AUGMENTED_PHRASE_DATASET, 
    MEDICAL_SYNONYMS, 
    use_medical_synonyms=True 
)