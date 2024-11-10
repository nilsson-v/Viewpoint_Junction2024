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
from collections import Counter

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


@app.route("/get_opinion/<opinion_id>", methods=["GET"])
def get_opinion(opinion_id):
    """
    Retrieves a single opinion by its ID from the 'opinions' collection.
    
    Args:
        opinion_id (str): The ID of the opinion to retrieve.
    
    Returns:
        JSON: A JSON object containing the opinion data or an error message if not found.
    """
    # Retrieve the document based on the provided opinion_id
    doc_ref = db.collection("opinions").document(opinion_id)
    doc = doc_ref.get()
    
    # Check if the document exists and return data if found
    if doc.exists:
        return jsonify({"opinion": doc.to_dict(), "id": doc.id})
    else:
        return jsonify({"error": "Opinion not found"}), 404


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
    """
    Endpoint to ask a question based on provided content.
    
    Accepts a JSON payload with the following fields:
        - "content" (str): The main content or article text to analyze.
        - "question" (str): The user's question about the provided content.
    
    Uses a language model prompt template to generate an answer to the question
    based on the content and returns a JSON response.
    
    Returns:
        JSON response containing:
        - "response" (str): The generated answer to the user's question.
    """
    # Get the JSON data from the request
    data = request.json

    # Extract 'content' and 'question' from the request, default to empty string if missing
    content = data.get("content", "")
    question = data.get("question", "")

    # Define a prompt template for the question-answering model
    qa_prompt_template = ChatPromptTemplate.from_messages(
                [("system", ADD_RELEVANT_INFO_PROMPT), ("user", "<article_content>{article}</article_content> <user_question>{text}</user_question>")]
            )
    
    # Create a chain that combines the prompt template and the language model
    qa_chain = qa_prompt_template | llm

    # Invoke the chain with content and question to get a response
    response = qa_chain.invoke({"article": content, "text": question}).content

    # Return the response in JSON format
    return jsonify({"response": response})


@app.route("/get_topics", methods=["GET"])
def get_topics():
    """
    Endpoint to retrieve and count topics from articles in the database.
    
    Collects all articles from the 'news_articles' collection, counts occurrences of each topic, 
    and returns a sorted list of topics in descending order of frequency.
    
    Returns:
        JSON response containing:
        - "data" (list): A list of dictionaries, each with:
            - "topic" (str): The topic name.
            - "count" (int): The count of articles for this topic.
    """
    # Reference the 'news_articles' collection in the database
    articles_ref = db.collection("news_articles")
    docs = articles_ref.stream()

    # Initialize a Counter to tally the topics
    topic_counts = Counter()

    # Process each document in the collection
    for doc in docs:
        article_data = doc.to_dict()
        
        # Extract the topic if it exists and increment its count
        topic = article_data.get("topic")
        if topic:
            topic_counts[topic] += 1

    # Sort topics by their count in descending order
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)

    # Format the sorted topics list for JSON response
    sorted_topics_json = [{"topic": topic, "count": count} for topic, count in sorted_topics]

    # Return the list of topics as a JSON response
    return jsonify({"data": sorted_topics_json})


@app.route("/get_articles/<topic>", methods=["GET"])
def get_articles_by_topic(topic):
    """
    Endpoint to retrieve articles by a specified topic.
    
    Fetches all articles in the 'news_articles' collection that match the specified topic
    and returns them as a list in JSON format.
    
    Args:
        topic (str): The topic to filter articles by (provided in URL).
    
    Returns:
        JSON response containing:
        - "data" (list): A list of dictionaries, each representing an article, with:
            - "id" (str): Document ID of the article.
            - Other article fields excluding "embedding" for clarity.
    """
    # Reference the 'news_articles' collection in the database
    articles_ref = db.collection("news_articles")
    
    # Create a query to retrieve articles with the specified topic
    query = articles_ref.where("topic", "==", topic)
    docs = query.stream()

    # Initialize a list to hold articles with the specified topic
    articles = []

    # Process each document and add to the articles list
    for doc in docs:
        article_data = doc.to_dict()
        article_data["id"] = doc.id  # Add document ID for reference
        article_data.pop("embedding", None)  # Exclude 'embedding' for response clarity
        articles.append(article_data)

    # Return the list of articles as a JSON response
    return jsonify({"data": articles})


# Run the Flask app on host 0.0.0.0 and port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
