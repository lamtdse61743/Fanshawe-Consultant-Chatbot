# LLM RAG Vector Database

This project implements a vector database designed for a large language model (LLM) system with retrieval-augmented generation (RAG). The system utilizes a JSON file located in the `QA_data` folder to populate the vector database, enabling efficient storage and retrieval of vector embeddings.

## Project Structure

```
llm-rag-vector-db
├── src
│   ├── main.py          # Entry point of the application
│   ├── db
│   │   └── vector_db.py # Manages storage and retrieval of vector embeddings
│   ├── rag
│   │   └── retriever.py  # Responsible for querying the vector database
│   ├── utils
│   │   └── json_loader.py # Utility functions for loading JSON data
│   └── types
│       └── index.py      # Defines types and interfaces for type safety
├── QA_data
│   └── data.json         # JSON data for populating the vector database
├── requirements.txt       # Lists project dependencies
└── README.md              # Documentation for the project
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd llm-rag-vector-db
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that the JSON data file is located in the `QA_data` folder.

## Usage

To run the application, execute the following command:
```
python src/main.py
```

## Overview of the System Architecture

The system is designed to load data from a JSON file, convert it into vector embeddings, and store these embeddings in a vector database. The retriever component allows for efficient querying of the database, enabling the LLM to retrieve relevant information during generation tasks.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.