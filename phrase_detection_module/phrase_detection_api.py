from flask import Flask, request, jsonify
import joblib
from phrase_detection_module_constants import *
from phrase_prediction import predict_category

# Initialize Flask App
app = Flask(__name__)

# Load Model
classifier, vectorizer = joblib.load(PHRASE_DETECTION_MODEL)

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint to predict categories for input phrases.
    """
    try:
        # Parse JSON input
        data = request.json
        if not data or 'phrases' not in data:
            return jsonify({"error": "Invalid input, 'phrases' key is required"}), 400
        
        phrases = data['phrases']
        
        # Ensure input is a string or list
        if not isinstance(phrases, (str, list)):
            return jsonify({"error": "'phrases' must be a string or a list of strings"}), 400
        
        # Get predictions
        predictions = predict_category(phrases).tolist()
        
        # Return predictions as JSON
        return jsonify({"phrases": phrases, "predictions": predictions})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
