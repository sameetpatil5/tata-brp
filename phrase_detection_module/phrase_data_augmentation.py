import csv, json
import random
from nltk.corpus import wordnet

PHRASE_DATASET = "./datasets/phrase_datasets/phrase_dataset.csv"
AUGMENTED_PHRASE_DATASET = "./datasets/phrase_datasets/augmented_phrase_dataset.csv"
MEDICAL_SYNONYMS = "./datasets/phrase_datasets/medical_synonym.json"
AUGMENTATION_VARIANCE = 3

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

def augment_phrase(phrase: str, synonyms_dict: dict, num_augmentations: int = AUGMENTATION_VARIANCE) -> list:
    """
    Generate augmented variations of a phrase by replacing words with synonyms.

    Args:
        phrase (str): The original phrase to augment.
        synonyms_dict (dict): A dictionary where keys are words and values are lists of synonyms.
        num_augmentations (int): The number of augmented phrases to generate. Default is 3.

    Returns:
        list: A list of augmented phrases.
    """
    words = phrase.split()
    augmented_phrases = set()

    for _ in range(num_augmentations):
        new_words = words[:]
        for i, word in enumerate(words):
            if word.lower() in synonyms_dict:
                synonym = random.choice(synonyms_dict[word.lower()])
                new_words[i] = synonym
            else:
                nltk_synonyms = get_synonyms(word.lower())
                if nltk_synonyms:
                    new_words[i] = random.choice(nltk_synonyms)
        augmented_phrases.add(' '.join(new_words))

    return list(augmented_phrases)

def augment_dataset(input_csv: str, output_csv: str, synonyms_dict: dict) -> None:
    """
    Augment the dataset by generating variations of each phrase and saving the augmented data.

    Args:
        input_csv (str): Path to the input CSV file containing phrases and categories.
        output_csv (str): Path to the output CSV file to save augmented data.
        synonyms_dict (dict): A dictionary where keys are words and values are lists of synonyms.

    Returns:
        None: Writes the augmented data to the specified output CSV file.
    """
    augmented_data = []

    with open(input_csv, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        augmented_data.append(header)

        for row in reader:
            phrase, category = row
            augmented_phrases = augment_phrase(phrase, synonyms_dict)
            for augmented_phrase in augmented_phrases:
                augmented_data.append([augmented_phrase, category])
            augmented_data.append(row)

    with open(output_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(augmented_data)

with open(MEDICAL_SYNONYMS, 'r') as medical_synonyms_file:
    """
    Load the medical synonyms dictionary from a JSON file and augment the dataset.

    The dictionary is used to replace words in phrases with their medical synonyms.
    """
    medical_synonyms = json.load(medical_synonyms_file)
    augment_dataset(PHRASE_DATASET, AUGMENTED_PHRASE_DATASET, medical_synonyms)