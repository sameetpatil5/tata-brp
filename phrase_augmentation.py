# import nltk
from nltk.corpus import wordnet
import random

# Function to find synonyms using WordNet
def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name().replace('_', ' '))
    return list(synonyms)

# Function to augment a phrase by replacing words with synonyms
def augment_phrase(phrase, num_augmentations=3):
    words = phrase.split()
    augmented_phrases = set()
    
    for _ in range(num_augmentations):
        new_words = words[:]
        for i, word in enumerate(words):
            synonyms = get_synonyms(word.lower())
            if synonyms:
                new_words[i] = random.choice(synonyms)
        augmented_phrases.add(' '.join(new_words))
    
    return list(augmented_phrases)

# Example data
phrase = "Total leukocyte count"

# Generate augmented phrases
augmented_phrases = augment_phrase(phrase, num_augmentations=5)
print(f"Original: {phrase}")
print("Augmented Phrases:")
for p in augmented_phrases:
    print(f"- {p}")
