from phrase_detection_module.phrase_detection_module_constants import *
from phrase_detection_module.phrase_prediction import predict_category
import pytest
import csv

# Load Test Data
test_data = []
with open(PHRASE_TEST_DATASET, 'r') as file:
    reader = csv.reader(file)
    header = next(reader)
    test_data = [tuple(row) for row in reader]

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
