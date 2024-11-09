from flask import Flask, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.vector import Vector

app = Flask(__name__)

cred = credentials.Certificate("./junction-2024-firebase-adminsdk-nkyl9-f1b4744457.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")


@app.route("/embed_text", methods=["POST"])
def embed_text():
    data = request.json
    user_input = data.get("text", "")
    # Embed the user input
    response = embed_model.embed_query(user_input)
    
    return jsonify({"embedded_text": response})


@app.route("/add_article", methods=["POST"])
def add_article():
    data = request.json

    article = data.get("article", "")
    subtopic = data.get("topic", "")
    statements = data.get("statements", "")

    embedded_subtopic = embed_model.embed_query(subtopic)

    news_doc = { 
        "topic" : subtopic,
        "article": article,
        "statements": statements,
        "embedded_subtopic": Vector(embedded_subtopic)
        }

    db.collection("news").document("1").set(news_doc)

    return jsonify({"response": "success"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
