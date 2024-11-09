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
from backend_prompts import CREATE_POLIS_DISCUSSION_PROMPT, ADD_RELEVANT_INFO_PROMPT
import re
import hashlib

# Set API key for GROQ model
os.environ["GROQ_API_KEY"] = GROQ_API_KEY

# Initialize the language model with specific parameters
llm = ChatGroq(
    model="gemma2-9b-it",
    temperature=0.2,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# Initialize Flask app and enable CORS
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Initialize Firebase connection with credentials
cred = credentials.Certificate("./junction-2024-firebase-adminsdk-nkyl9-f1b4744457.json")
firebase_admin.initialize_app(cred)

# Firestore database client
db = firestore.client()

# HuggingFace embedding model used for text vectorization
embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")


@app.route("/get_articles", methods=["GET"])
def get_articles():
    """
    Fetches all articles from the 'news_articles' Firestore collection and returns them as JSON.
    
    Returns:
        JSON: A JSON object containing a list of articles with their metadata.
    """
    # Reference the 'news_articles' collection
    articles_ref = db.collection("news_articles")
    docs = articles_ref.stream()

    # Prepare a list to store all articles
    articles = []

    # Iterate through each document and add it to the list
    for doc in docs:
        article_data = doc.to_dict()
        article_data["id"] = doc.id  # Include the document ID
        article_data.pop("embedding", None)  # Remove embedding data for response clarity
        articles.append(article_data)

    # Return the list of articles as a JSON response
    return jsonify({"data": articles})


@app.route("/get_article/<article_id>", methods=["GET"])
def get_article(article_id):
    """
    Retrieves a single article by its ID from the 'news_articles' collection.
    
    Args:
        article_id (str): The ID of the article to retrieve.
    
    Returns:
        JSON: A JSON object containing the article data or an error message if not found.
    """
    # Retrieve the document based on the provided article_id
    doc_ref = db.collection("news_articles").document(article_id)
    doc = doc_ref.get()
    if doc.exists:
        return jsonify({"article": doc.to_dict(), "id": doc.id})
    else:
        return jsonify({"error": "Article not found"}), 404
    

@app.route("/get_opinions", methods=["GET"])
def get_opinions():
    """
    Fetches all opinions from the 'opinions' Firestore collection and returns them as JSON.
    
    Returns:
        JSON: A JSON object containing a list of opinions with their metadata.
    """
    # Reference the 'opinions' collection
    opinions_ref = db.collection("opinions")
    docs = opinions_ref.stream()

    # Prepare a list to store all opinions
    opinions = []

    # Iterate through each document and add it to the list
    for doc in docs:
        opinion_data = doc.to_dict()
        opinion_data["id"] = doc.id  # Include the document ID
        opinion_data.pop("embedding", None)  # Remove embedding data for response clarity
        opinions.append(opinion_data)

    # Return the list of opinions as a JSON response
    return jsonify({"data": opinions})


@app.route("/process_user_viewpoint", methods=["POST"])
def process_user_viewpoint():
    """
    Processes user-submitted content by generating a topic, subtopic, and statements
    using the language model. Embeds the content and saves it to the 'opinions' Firestore collection.
    
    Expected JSON input:
        - title (str): Title of the opinion content.
        - date (str): Date of the opinion content.
        - content (str): Main content of the opinion.
        - source (str): Source of the opinion content.
    
    Returns:
        JSON: A JSON object indicating success.
    """
    # Extract data from the request
    data = request.json
    title = data.get("title", "")
    date = data.get("date", "")
    content = data.get("content")
    source = data.get("source")

    # Generate prompts for the language model
    create_polis_discussion_prompt_template = ChatPromptTemplate.from_messages(
                [("system", CREATE_POLIS_DISCUSSION_PROMPT), ("user", "{text}")]
            )
    create_polis_discussion_chain = create_polis_discussion_prompt_template | llm

    # Invoke the model with the content to generate a response
    response = create_polis_discussion_chain.invoke({"text": content}).content

    # Parse the response for topic, subtopic, and statements
    topic = re.search(r"<topic>(.*?)</topic>", response).group(1)
    subtopic = re.search(r"<subtopic>(.*?)</subtopic>", response).group(1)
    statements_raw = re.search(r"<statements>(.*?)</statements>", response).group(1)

    # Split statements by '|' and trim whitespace
    statements = [statement.strip() for statement in statements_raw.split("|")]

    # Generate embedding for the content
    embedding = Vector(embed_model.embed_query(content))

    # Prepare the opinion document
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

    # Generate a unique ID based on the content hash
    opinion_id = hashlib.sha256(content.encode()).hexdigest()
    
    # Store the opinion document in Firestore
    db.collection("opinions").document(opinion_id).set(opinion_doc)

    return jsonify({"response": "success"})


@app.route("/search_articles", methods=["POST"])
def search_articles():
    """
    Searches for articles similar to the provided text using vector similarity in the
    'news_articles' collection.
    
    Expected JSON input:
        - text (str): The text query to search for similar articles.
    
    Returns:
        JSON: A JSON object containing a list of similar articles based on vector similarity.
    """
    # Extract query text from the request
    data = request.json
    text = data.get("text", "")

    # Generate query vector using embedding model
    query_vector = embed_model.embed_query(text)

    # Reference the 'news_articles' collection
    collection = db.collection("news_articles")

    # Execute a nearest neighbor search based on cosine similarity
    vector_query = collection.find_nearest(
        vector_field="embedding",
        query_vector=Vector(query_vector),
        distance_measure=DistanceMeasure.COSINE,
        limit=5,
    )

    # Stream the search results
    docs = vector_query.stream()

    # Prepare a list to store the retrieved articles
    articles = []

    # Iterate through each document and add it to the list
    for doc in docs:
        article_data = doc.to_dict()
        article_data["id"] = doc.id  # Include the document ID
        article_data.pop("embedding", None)  # Remove embedding data for response clarity
        articles.append(article_data)

    # Return the list of articles as a JSON response
    return jsonify({"data": articles})

@app.route("/ask_question", methods=["POST"])
def ask_question():
    data = request.json

    content = data.get("content", "")
    question = data.get("question", "")

    qa_prompt_template = ChatPromptTemplate.from_messages(
                [("system", ADD_RELEVANT_INFO_PROMPT), ("user", "<article_content>{article}</article_content> <user_question>{text}</user_question>")]
            )
    qa_chain = qa_prompt_template | llm

    response = qa_chain.invoke({"article": content, "text": question}).content

    return jsonify({"response": response})


# Run the Flask app on host 0.0.0.0 and port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
