from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai
from db.vector_db import VectorDatabase
from rag.retriever import Retriever
from utils.json_loader import load_json

app = Flask(__name__)

# Load data from JSON file
data = load_json('llm-rag-vector-db/QA_data/data.json')
items = data["qa_data"]

# Initialize the vector database
vector_db = VectorDatabase()
vector_db.load_from_json(items)

# Set up the retriever
retriever = Retriever()
retriever.set_database(vector_db)

# Get Gemini API key from environment variable

api_key = "AIzaSyCsxy-8Wa3_jlNBA8rqPJsbBsO9CHAJl7M"
if not api_key:
    raise ValueError("Gemini API key not found. Set GEMINI_API_KEY environment variable.")

def call_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')
    conversation_history = request.json.get('history', [])
    process_log = []

    results = retriever.retrieve(user_query)
    process_log.append(f"Retrieved {len(results)} candidates for: \"{user_query}\"")
    context = ""
    relevant_results = [r for r in results if r[1] >= 0.8]  # Use your chosen threshold

    if relevant_results:
        for idx, score, item in relevant_results:
            process_log.append(f"Cosine similarity for result {idx}: {score:.4f}")
            context += f"Q: {item['question']}\nA: {item['answer']}\n"
        process_log.append("Context assembled from relevant results.")
        prompt = (
            f"You are an expert Fanshawe College consultant.\n"
            f"Conversation history:\n"
            f"{''.join(conversation_history)}\n"
            f"Based on the following relevant information, answer the user's question concisely and directly.\n"
            f"User question: {user_query}\n"
            f"Relevant information:\n{context}\n"
            f"Format your answer as:\n"
            f"1. Direct answer to the question\n"
            f"2. Link to the official program page\n"
        )
        process_log.append("Sending prompt to Gemini...")
        gemini_response = call_gemini(prompt, api_key)
        process_log.append("Received response from Gemini.")
        conversation_history.append(f"User: {user_query}\nGemini: {gemini_response}\n")
        return jsonify({'response': gemini_response, 'history': conversation_history, 'process_log': process_log})
    else:
        sorry_msg = "Sorry, I couldn't find information about that program. Please check the official Fanshawe College website."
        process_log.append("No relevant context found (cosine similarity below threshold). Not sending to Gemini.")
        conversation_history.append(f"User: {user_query}\nGemini: {sorry_msg}\n")
        return jsonify({'response': sorry_msg, 'history': conversation_history, 'process_log': process_log})
if __name__ == "__main__":
    app.run(debug=True)