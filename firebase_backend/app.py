from flask import Flask, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from langchain_groq import ChatGroq
from groq_keys import GROQ_API_KEY
import os
from flask_cors import CORS
from backend_prompts import CREATE_POLIS_DISCUSSION_PROMPT
import re
import hashlib

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0.2,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

app = Flask(__name__)
CORS(app)  # This will allow all domains by default PROBABLY NEEDED???

cred = credentials.Certificate("./junction-2024-firebase-adminsdk-nkyl9-f1b4744457.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")


@app.route("/get_articles", methods=["GET"])
def get_articles():
    # Reference the 'news_articles' collection
    articles_ref = db.collection("news_articles")
    docs = articles_ref.stream()

    # Prepare a list to store all articles
    articles = []

    # Iterate through each document and add it to the list
    for doc in docs:
        article_data = doc.to_dict()
        article_data["id"] = doc.id  # Include the document ID
        article_data.pop("embedding", None)
        articles.append(article_data)

    # Return the list of articles as a JSON response
    return jsonify({"data": articles})


@app.route("/get_article/<article_id>", methods=["GET"])
def get_article(article_id):
    doc_ref = db.collection("news_articles").document(article_id)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify({"article": doc.to_dict(), "id": doc.id})
    else:
        return jsonify({"error": "Article not found"}), 404
    

@app.route("/get_opinions", methods=["GET"])
def get_opinions():
    # Reference the 'news_articles' collection
    opinions_ref = db.collection("opinions")
    docs = opinions_ref.stream()

    # Prepare a list to store all articles
    opinions = []

    # Iterate through each document and add it to the list
    for doc in docs:
        opinion_data = doc.to_dict()
        opinion_data["id"] = doc.id  # Include the document ID
        opinion_data.pop("embedding", None)
        opinions.append(opinion_data)

    # Return the list of articles as a JSON response
    return jsonify({"data": opinions})


@app.route("/process_user_viewpoint", methods=["POST"])
def process_user_viewpoint():
    data = request.json

    title = data.get("title", "")
    date = data.get("date", "")
    content = data.get("content")
    source = data.get("source")

    create_polis_discussion_prompt_template = ChatPromptTemplate.from_messages(
                [("system", CREATE_POLIS_DISCUSSION_PROMPT), ("user", "{text}")]
            )

    create_polis_discussion_chain = create_polis_discussion_prompt_template | llm

    response = create_polis_discussion_chain.invoke({"text": content}).content

    topic = re.search(r"<topic>(.*?)</topic>", response).group(1)
    subtopic = re.search(r"<subtopic>(.*?)</subtopic>", response).group(1)
    statements_raw = re.search(r"<statements>(.*?)</statements>", response).group(1)

    # Split statements by '|'
    statements = [statement.strip() for statement in statements_raw.split("|")]

    embedding = Vector(embed_model.embed_query(content))

    opinion_doc = {
                "title": title,
                "date": date,
                "content": content,
                "subtopic": subtopic,
                "statements": statements,
                "topic": topic,
                "source": source,
                "embedding": embedding,
            }

    opinion_id = hashlib.sha256(content.encode()).hexdigest()
    
    db.collection("opinions").document(opinion_id).set(opinion_doc)

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
