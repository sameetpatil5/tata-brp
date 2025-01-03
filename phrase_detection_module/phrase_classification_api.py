from flask import Flask, request, jsonify
from phrase_classification import classify_phrase

app = Flask(__name__)

@app.route('/classify', methods=['POST'])
def classify():
    try:
        # Get the list of phrases from the request JSON
        data = request.get_json()
        if not data or 'phrases' not in data:
            return jsonify({"error": "Invalid request. Please provide a 'phrases' list."}), 400

        phrases = data['phrases']
        if not isinstance(phrases, list):
            return jsonify({"error": "'phrases' should be a list of strings."}), 400

        # Classify the phrases
        classifications = classify_phrase(phrases)

        # Return the classifications as JSON
        return jsonify({"classifications": classifications})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
