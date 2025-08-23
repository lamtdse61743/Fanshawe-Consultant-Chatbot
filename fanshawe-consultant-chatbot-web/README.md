# Fanshawe Consultant Chatbot Web Application

A web-based intelligent chatbot system designed for Fanshawe College that provides instant answers to student and faculty questions using advanced vector database technology and AI-powered responses.

## 🚀 Features

- **Interactive Web Interface**: Clean, responsive chat interface for seamless user experience
- **Vector Database Integration**: Efficient information retrieval from structured knowledge base
- **AI-Powered Responses**: Gemini API integration for handling queries beyond the database scope
- **Real-time Communication**: Instant responses with typing indicators and message history
- **Scalable Architecture**: Modular design supporting easy maintenance and feature expansion

## 🏗️ Project Structure

```
fanshawe-consultant-chatbot-web/
├── src/
│   ├── main.py                 # Vector database initialization and query handling
│   ├── app.py                  # Flask web application entry point
│   ├── templates/
│   │   └── chat.html          # Chat interface HTML template
│   ├── static/
│   │   └── style.css          # Responsive CSS styling
│   ├── db/
│   │   └── vector_db.py       # Vector database management class
│   ├── rag/
│   │   └── retriever.py       # RAG (Retrieval-Augmented Generation) logic
│   └── utils/
│       └── json_loader.py     # JSON data processing utilities
├── requirements.txt            # Python dependencies
└── README.md                  # Project documentation
```

## ⚡ Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/lamtdse61743/Fanshawe-Consultant-Chatbot.git
   cd fanshawe-consultant-chatbot-web
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Set up your Gemini API key (if required)
   export GEMINI_API_KEY="your_api_key_here"
   ```

4. **Run the application**
   ```bash
   python src/app.py
   ```

5. **Access the chatbot**
   
   Open your browser and navigate to `http://localhost:5000`

## 💡 How It Works

The chatbot operates using a two-tier response system:

1. **Primary Layer**: Searches the vector database for relevant information matching user queries
2. **Fallback Layer**: When database results are insufficient, the Gemini API generates contextually appropriate responses

This hybrid approach ensures comprehensive coverage while maintaining response accuracy and relevance.

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **AI/ML**: Vector Database, RAG Architecture, Google Gemini API
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Processing**: JSON, Vector Embeddings

## 📖 Usage Examples

**Student Query**: "What are the admission requirements for Computer Programming?"

**Faculty Query**: "How do I submit grades through the portal?"

**General Query**: "What services does the library offer?"

The system intelligently categorizes and responds to various query types with accurate, helpful information.

## 🤝 Contributing

We welcome contributions to improve the chatbot system! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines for Python code
- Add comments for complex logic
- Test new features thoroughly before submitting
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions, issues, or suggestions:

- **Create an issue** on GitHub
- **Email**: lamtdse61743@gmail.com
- **LinkedIn**: [Connect with me](https://linkedin.com/in/lamdinh)

## 🔄 Version History

- **v1.0.0** - Initial release with core chatbot functionality
- **v1.1.0** - Added web interface and improved response accuracy
- **v1.2.0** - Integrated Gemini API for enhanced AI responses

---

⭐ **Star this repository** if you find it helpful!