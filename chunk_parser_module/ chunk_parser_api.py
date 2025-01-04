from flask import Flask, request, jsonify
from chunk_parser import parse_chunk_to_dataframe

app = Flask(__name__)
@app.route("/parse_chunk", methods=["POST"])
def parse_chunk():
    data = request.json
    chunk = data.get("chunk")

    if chunk:
        df = parse_chunk_to_dataframe(chunk)
    else:
        return jsonify({"error": "No valid input provided."}), 400

    if df is not None:
        return jsonify({"dataframe": df.to_dict(orient="records")})
    else:
        return jsonify({"error": "Failed to parse the input."}), 400

if __name__ == "__main__":
    app.run(debug=True)
