# Fanshawe Consultant Chatbot Web Application

This project is a web application that serves as a chatbot for Fanshawe College, allowing users to ask questions and receive answers based on a vector database of information. The chatbot utilizes the Gemini API for generating responses when relevant information is not found in the database.

## Project Structure

```
fanshawe-consultant-chatbot-web
├── src
│   ├── main.py          # Original script for initializing the vector database and handling user queries
│   ├── app.py           # Main entry point for the web application
│   ├── templates
│   │   └── chat.html    # HTML structure for the chat interface
│   ├── static
│   │   └── style.css     # CSS styles for the chat interface
│   ├── db
│   │   └── vector_db.py  # Class for managing the vector database
│   ├── rag
│   │   └── retriever.py   # Class for retrieving relevant results from the vector database
│   └── utils
│       └── json_loader.py # Utility functions for loading JSON data
├── requirements.txt      # List of dependencies for the project
└── README.md             # Documentation for the project
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fanshawe-consultant-chatbot-web
   ```

2. **Install dependencies:**
   Ensure you have Python installed, then run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the application:**
   Start the web application by executing:
   ```
   python src/app.py
   ```

4. **Access the chat interface:**
   Open your web browser and navigate to `http://localhost:5000` to interact with the chatbot.

## Usage Guidelines

- Enter your questions in the chat interface and receive answers based on the information stored in the vector database.
- If the chatbot cannot find relevant information, it will generate a response using the Gemini API.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.