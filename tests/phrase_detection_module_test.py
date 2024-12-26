import joblib
import pytest
import csv
from phrase_detection_module.phrase_detection_module_constants import *

# Load Model
classifier, vectorizer = joblib.load(PHRASE_DETECTION_MODEL)

# Load Test Data
test_data = []
with open(PHRASE_TEST_DATASET, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    test_data = [tuple(row) for row in reader]

def predict_category(phrases: str | list) -> list:
    """
    Predicts the category for a list of phrases using a pre-trained machine learning model.

    Args:
        phrases (str or list): A single phrase (str) or a list of phrases (list of str) to classify.
    
    Returns:
        list: A list of predictions corresponding to each input phrase. 
              Each prediction is the predicted category for the phrase.
    
    Example:
        >>> predict_category(["Total leukocyte count", "Polymorphonuclear leucocytes"])
        ['WBC count', 'Neutrophil %']
        
    If a single phrase is provided as a string, it will be converted to a list internally:
        >>> predict_category("Hemoglobin level")
        ['Haemoglobin']
    """
    
    # If a single phrase is passed, convert it to a list
    if isinstance(phrases, str):
        phrases = [phrases]
    
    # Transform phrases into vectors
    phrase_vec = vectorizer.transform(phrases)
    
    # Get predictions for all phrases
    predictions = classifier.predict(phrase_vec)
    
    # Return predictions as a list
    return predictions

@pytest.mark.parametrize("phrase, expected_category", test_data)
def test_predict_category(phrase, expected_category):
    """
    Test the predict_category function to ensure it returns the correct category
    for each phrase based on the provided dataset.
    
    Args:
        phrase (str): The input phrase to be classified.
        expected_category (str): The expected category for the phrase.
    """
    # Get the prediction from the model
    prediction = predict_category([phrase])[0]
    
    # Assert that the predicted category matches the expected category
    assert prediction == expected_category, f"Expected '{expected_category}', but got '{prediction}' for phrase '{phrase}'"

# Run the test
# pytest -v tests/phrase_detection_module_test.py
