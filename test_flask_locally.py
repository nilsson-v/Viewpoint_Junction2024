from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = {
    "1": {
        "title": "Qatar asks Hamas leaders to leave after US pressure",
        "date": "2024-11-09T10:00:00Z",
        "content": "Warren Buffett has bought a new home in Chinatown...",
        "subtopic": "US economy",
        "statements": [],
        "topic": "Politics",
        "source": "Reuters"
    },
    "2": {
        "title": "AI Breakthroughs in Healthcare: What's Next?",
        "date": "2024-11-08T15:30:00Z",
        "content": "Artificial intelligence has made significant strides in healthcare...",
        "subtopic": "Technology",
        "statements": [],
        "topic": "Healthcare",
        "source": "TechCrunch"
    }
}

# Route for the homepage
@app.route('/')
def home():
    return "Welcome to the Flask API"

# Route to fetch data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
