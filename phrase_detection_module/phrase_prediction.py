import joblib
from phrase_detection_module_constants import *

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

    # Load Model
    classifier, vectorizer = joblib.load(PHRASE_DETECTION_MODEL)

    # If a single phrase is passed, convert it to a list
    if isinstance(phrases, str):
        phrases = [phrases]
    
    # Transform phrases into vectors
    phrase_vec = vectorizer.transform(phrases)
    
    # Get predictions for all phrases
    predictions = classifier.predict(phrase_vec)
    
    # Return predictions as a list
    return predictions