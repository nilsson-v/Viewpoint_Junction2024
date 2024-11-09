from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from langchain_community.chat_models import ChatOCIGenAI
from config_private import GROQ_API_KEY, COMPARTMENT_OCID
from prompts import CREATE_POLIS_DISCUSSION_PROMPT, TRANSLATE_AND_EXPAND_ARTICLE_PROMPT
import os
import json
import re

os.environ["GROQ_API_KEY"] = GROQ_API_KEY

llm = ChatOCIGenAI(
    model_id="meta.llama-3.1-70b-instruct",
    service_endpoint="https://inference.generativeai.eu-frankfurt-1.oci.oraclecloud.com",
    compartment_id=COMPARTMENT_OCID,
    model_kwargs={"temperature": 0.2, "max_tokens": 4000},
)

cred = credentials.Certificate("./firebase_backend/junction-2024-firebase-adminsdk-nkyl9-f1b4744457.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-l6-v2")


def process_articles(data):

    articles = {}

    translate_and_expand_prompt_template = ChatPromptTemplate.from_messages(
                [("system", TRANSLATE_AND_EXPAND_ARTICLE_PROMPT), ("user", "{text}")]
            )
    translate_and_expand_chain = translate_and_expand_prompt_template | llm

    create_polis_discussion_prompt_template = ChatPromptTemplate.from_messages(
                [("system", CREATE_POLIS_DISCUSSION_PROMPT), ("user", "{text}")]
            )

    create_polis_discussion_chain = create_polis_discussion_prompt_template | llm

    for i, article in enumerate(data.values()):
        try:
            te_response = translate_and_expand_chain.invoke({"text": article}).content

            print("\n\n\n")
            print(te_response)
            print("\n\n\n")

            cpd_response = create_polis_discussion_chain.invoke({"text": te_response}).content

            print(cpd_response)
            print("\n\n\n")

            title = re.search(r"<title>(.*?)</title>", te_response).group(1)
            article_content = re.search(r"<content>(.*?)</content>", te_response, re.DOTALL).group(1)

            topic = re.search(r"<topic>(.*?)</topic>", cpd_response).group(1)
            subtopic = re.search(r"<subtopic>(.*?)</subtopic>", cpd_response).group(1)
            statements_raw = re.search(r"<statements>(.*?)</statements>", cpd_response).group(1)

            # Split statements by '|'
            statements = [statement.strip() for statement in statements_raw.split("|")]

            articles["article" + str(i)] = {
                "title": title,
                "date": "2024-11-09T10:00:00Z",
                "content": article_content,
                "subtopic": subtopic,
                "statements": statements,
                "topic": topic,
                "source": "YLE (modified by GenAI)",
            }
        except:
            print("article"+ str(i) + " failed processing")
            continue
    
    return articles


def upload_articles(data):
    for key, value in zip(data.keys(), data.values()):
        value["embedding"] = Vector(embed_model.embed_query(value.get("content", "")))
        db.collection("news_articles").document(key).set(value)


def clear_collection(collection_ref):
    docs = collection_ref.stream()
    for doc in docs:
        doc.reference.delete()


if __name__ == "__main__":
    process_news = False

    upload_news = True

    clear_news = True

    if clear_news:
        clear_collection(db.collection("news_articles"))

    if process_news:
        file_path = "./news_data.json" # from yle api
        with open(file_path, 'r') as file:
            data_dict = json.load(file)
        data = process_articles(data_dict)

        file_path = './processed_news1.json'

        # Open the file in write mode ('w')
        with open(file_path, 'w') as file:
            # Use json.dump() to write the data to the file
            json.dump(data, file, indent=4)

    if upload_news:
        file_path = "./processed_news.json"
        with open(file_path, 'r') as file:
            data_dict = json.load(file)
        upload_articles(data_dict)
    