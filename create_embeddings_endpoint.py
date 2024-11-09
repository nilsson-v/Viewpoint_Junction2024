from flask import Flask, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
import os

app = Flask(__name__)

embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")


@app.route("/generate", methods=["POST"])
def generate_text():
    data = request.json
    user_input = data.get("text", "")
    # Embed the user input
    response = embed_model.embed_query(user_input)
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
