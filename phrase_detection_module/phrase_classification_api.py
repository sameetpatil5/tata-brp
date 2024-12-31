from phrase_classification import classify_phrase

# Test cases
test_phrases = [
    "Total leukocyte count",
    "Segmented neutrophils",
    "Hb",
    "Absolute neutrophil count",
    "Lymphocyte percentage",
    "Random term",
    "count",
    "level of WBC",
    "white blood cell count"
]

# Classify the test phrases
classify_phrase(test_phrases)