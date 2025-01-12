# unit_conversion_api.py
import flask
from flask import request, jsonify
from unit_conversion import unit_conversion
import pandas as pd

app = flask.Flask(__name__)

@app.route('/convert_units', methods=['POST'])
def convert_units():
    try:
        # Load the request data
        data = request.get_json()
        units_df = pd.read_json(data)

        final_data_packet = unit_conversion(units_df)

        return jsonify(final_data_packet)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
