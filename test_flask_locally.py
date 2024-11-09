from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Route for the homepage
@app.route('/')
def home():
    return "Welcome to the Flask API"

# Route to fetch data from the file
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        # Open the text file and load its JSON content
        with open('test_news.txt', 'r') as file:
            data = json.load(file)  # Parse the JSON from the file
        return jsonify(data)  # Return the data as JSON
    except Exception as e:
        return jsonify({"error": f"Error reading the file: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
