from flask import Flask, render_template, request, jsonify
import os
import glob
import google.generativeai as genai
from db.vector_db import VectorDatabase

app = Flask(__name__)

# Dynamically find the QA_data JSON file
base_dir = os.path.dirname(os.path.abspath(__file__))
qa_data_dir = os.path.join(base_dir, "QA_data")
json_files = glob.glob(os.path.join(qa_data_dir, "*.json"))
if not json_files:
    raise FileNotFoundError("No JSON file found in QA_data directory.")
qa_json_path = json_files[0]  # Use the first JSON file found

# Initialize the vector database (build or load)
vector_db = VectorDatabase()
vector_db.build_or_load(qa_json_path)

# Get Gemini API key from environment variable or config
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
    vector_db.build_or_load(qa_json_path, process_log=process_log)

    if not user_query:
        return jsonify({'error': 'No query provided.'}), 400

    results = vector_db.get_top_k(user_query, top_k=5)
    process_log.append(f"Retrieved {len(results)} candidates for: \"{user_query}\"")

    relevant = []
    reference = []
    low_conf = []
    for idx, score, item in results:
        if score >= 0.6:
            relevant.append((idx, score, item))
        elif score >= 0.5:
            reference.append((idx, score, item))
        else:
            low_conf.append((idx, score, item))

    context = ""
    warning_msg = ""
    if relevant:
        for idx, score, item in relevant:
            process_log.append(f"Relevant (cosine {score:.4f}): result {idx}")
            context += f"Q: {item['question']}\nA: {item['answer']}\n"
        if reference:
            context += "\n---\nThe following information is provided for reference only:\n"
            for idx, score, item in reference:
                process_log.append(f"Reference (cosine {score:.4f}): result {idx}")
                context += f"Q: {item['question']}\nA: {item['answer']}\n"
        process_log.append("Context assembled from relevant and reference results.")
    elif reference:
        for idx, score, item in reference:
            process_log.append(f"Reference (cosine {score:.4f}): result {idx}")
            context += f"Q: {item['question']}\nA: {item['answer']}\n"
        warning_msg = "Sorry, I don't have a direct answer, but here is some information that might help:\n\n"
        process_log.append("No highly relevant context found, using reference information only.")
    elif low_conf:
        for idx, score, item in low_conf:
            process_log.append(f"Low confidence (cosine {score:.4f}): result {idx}")
            context += f"Q: {item['question']}\nA: {item['answer']}\n"
        warning_msg = "Sorry, I couldn't find a trustworthy answer, but here is the closest information I found (may not be accurate):\n\n"
        process_log.append("No relevant or reference context found, using low-confidence information only.")

        prompt = (
            f"You are an expert Fanshawe College consultant.\n"
            f"Conversation history:\n"
            f"{''.join(conversation_history)}\n"
            f"Based on the following information, answer the user's question concisely and directly.\n"
            f"If the provided information is not helpful, answer using your own knowledge as an expert Fanshawe College consultant.\n"
            f"User question: {user_query}\n"
            f"Relevant information:\n{context}\n"
            f"Format your answer as:\n"
            f"1. Direct answer to the question\n"
            f"2. If a direct link to the official program page is present in the relevant information, include it. Otherwise, do not mention links or searching the website.\n"
        )
        process_log.append("Sending prompt to Gemini...")
        gemini_response = call_gemini(prompt, api_key)
        process_log.append("Received response from Gemini.")
        gemini_response = warning_msg + gemini_response.replace('*', '')
        conversation_history.append(f"User: {user_query}\nGemini: {gemini_response}\n")
        return jsonify({'response': gemini_response, 'history': conversation_history, 'process_log': process_log})
    else:
        sorry_msg = "Sorry, I couldn't find any information related to your question."
        process_log.append("No context found at all. Not sending to Gemini.")
        conversation_history.append(f"User: {user_query}\nGemini: {sorry_msg}\n")
        return jsonify({'response': sorry_msg, 'history': conversation_history, 'process_log': process_log})

    prompt = (
        f"You are an expert Fanshawe College consultant.\n"
        f"Conversation history:\n"
        f"{''.join(conversation_history)}\n"
        f"Based on the following information, answer the user's question concisely and directly.\n"
        f"User question: {user_query}\n"
        f"Relevant information:\n{context}\n"
        f"Format your answer as:\n"
        f"1. Direct answer to the question\n"
        f"2. If a direct link to the official program page is present in the relevant information, include it. Otherwise, do not mention links or searching the website.\n"
    )
    process_log.append("Sending prompt to Gemini...")
    gemini_response = call_gemini(prompt, api_key)
    process_log.append("Received response from Gemini.")
    gemini_response = warning_msg + gemini_response.replace('*', '')
    conversation_history.append(f"User: {user_query}\nGemini: {gemini_response}\n")
    return jsonify({'response': gemini_response, 'history': conversation_history, 'process_log': process_log})
if __name__ == "__main__":
    app.run(debug=True)