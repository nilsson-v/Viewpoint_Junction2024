from flask import Flask, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from langchain_groq import ChatGroq
from config_private import GROQ_API_KEY
import os

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0.2,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

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


@app.route("/similarity_search_article", methods=["POST"])
def similarity_search_article():
    data = request.json
    subtopic = data.get("topic", "")
    embedded_subtopic = embed_model.embed_query(subtopic)

    collection = db.collection("news")

    # Requires a single-field vector index
    vector_query = collection.find_nearest(
        vector_field="embedded_subtopic",
        query_vector=Vector(embedded_subtopic),
        distance_measure=DistanceMeasure.COSINE,
        limit=5,
        distance_result_field="vector_distance"
    )

    docs = vector_query.stream()

    response_data = [f"{doc.id}), Distance: {doc.get('vector_distance')}" for doc in docs]

    return jsonify({"response": response_data})


@app.route("/generate_text", methods=["POST"])
def generateText():
    data = request.json
    user_input = data.get("text", )

    prompt_template = ChatPromptTemplate.from_messages(
                [("system", "You are now an assistant whose task is simple QA. Please briefly answer user questions. Lets begin..."), ("user", "{text}")]
            )

    chain = prompt_template | llm

    response = chain.invoke({"text": user_input})

    return jsonify({"response": response.content})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
