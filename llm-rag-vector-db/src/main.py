import os
import google.generativeai as genai
from db.vector_db import VectorDatabase
from rag.retriever import Retriever
from utils.json_loader import load_json
key = "AIzaSyCsxy-8Wa3_jlNBA8rqPJsbBsO9CHAJl7M"
def call_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')  # Use Gemini Flash 2.5
    response = model.generate_content(prompt)
    return response.text

def main():
    # Load data from JSON file
    data = load_json('llm-rag-vector-db/QA_data/data.json')
    items = data["qa_data"]

    print("Initializing vector database and embedding questions...")

    # Initialize the vector database
    vector_db = VectorDatabase()
    vector_db.load_from_json(items)

    # Set up the retriever
    retriever = Retriever()
    retriever.set_database(vector_db)

    # Get Gemini API key from environment variable
    api_key = key
    if not api_key:
        print("Gemini API key not found. Set GEMINI_API_KEY environment variable.")
        return

    # Interactive question input
        # Add this before the while loop
    conversation_history = []

    # Inside the while loop, after each user query:
    while True:
        query = input("Enter your question (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        results = retriever.retrieve(query)
        print("Top results:")
        context = ""
        relevant_results = [r for r in results if r[1] >= 0.6]
        if relevant_results:
            for idx, score, item in relevant_results:
                print(f"ID: {idx}, Cosine Similarity: {score:.4f}")
                print(f"Question: {item['question']}")
                print(f"Answer: {item['answer']}\n")
                context += f"Q: {item['question']}\nA: {item['answer']}\n"
            prompt = (
                f"You are an expert Fanshawe College consultant.\n"
                f"Conversation history:\n"
                f"{''.join(conversation_history)}\n"
                f"Based on the following relevant information, answer the user's question concisely and directly.\n"
                f"If possible, include a direct link to the official Fanshawe College program page for more details.\n\n"
                f"User question: {query}\n"
                f"Relevant information:\n{context}\n"
                f"Format your answer as:\n"
                f"1. Direct answer to the question\n"
                f"2. Link to the official program page\n"
            )
        else:
            print("No relevant information found above the threshold. Asking Gemini to answer independently.")
            prompt = (
                f"You are an expert Fanshawe College consultant.\n"
                f"Conversation history:\n"
                f"{''.join(conversation_history)}\n"
                f"Answer the user's question as best as you can, even if no relevant information is provided.\n"
                f"If possible, include a direct link to the official Fanshawe College program page for more details.\n\n"
                f"User question: {query}\n"
            )
        gemini_response = call_gemini(prompt, api_key)
        print("Gemini Response:")
        print(gemini_response)
        conversation_history.append(f"User: {query}\nGemini: {gemini_response}\n")

if __name__ == "__main__":
    main()