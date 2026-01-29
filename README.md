# RAG Beluga Cold Therapy - Medical Device Support Chatbot

This project implements a Retrieval-Augmented Generation (RAG) chatbot designed to provide medical device support, specifically for "Beluga Health" products with a focus on cold therapy. The application features a web-based chat interface where users can ask questions, and the RAG system retrieves relevant information from a knowledge base to generate informed answers, citing its sources.

## Features

*   **Interactive Chat Interface:** A user-friendly web interface for natural language interaction.
*   **Context-Aware Responses:** Utilizes a RAG system to provide answers grounded in a specialized knowledge base.
*   **Source Citation:** Mentions the source documents used to formulate answers, enhancing trustworthiness.
*   **Scalable Knowledge Base:** Easily extendable by adding more JSON documents to the `dataset` directory.
*   **Flexible LLM Integration:** Powered by Groq's fast inference capabilities.

## Key Technologies

*   **Backend Framework:** Flask (Python)
*   **Embedding Model:** HuggingFace `all-MiniLM-L6-v2`
*   **Vector Store:** Chroma
*   **Large Language Model (LLM):** Groq `llama-3.3-70b-versatile`
*   **Environment Management:** Python virtual environment
*   **Task Runner:** `just` (for simplified command execution)
*   **Frontend:** HTML, CSS, JavaScript (single-page application)

## Architecture

The application is structured into the following main components:

1.  **Data Ingestion (`ingest.py`):**
    *   Processes JSON documents located in the `dataset` directory.
    *   Uses `all-MiniLM-L6-v2` to create vector embeddings of the document content.
    *   Stores these embeddings in a persistent Chroma vector database (`chroma_db`), forming the project's knowledge base.

2.  **Web Application (`app.py`):**
    *   A Flask web server that handles HTTP requests.
    *   Serves the `index.html` frontend, providing the user interface for the chatbot.
    *   Exposes a `/api/chat` API endpoint to receive user queries and return RAG-powered responses.
    *   Initializes the RAG system by loading the HuggingFace embeddings, connecting to the Chroma vector store, and configuring the Groq LLM.
    *   Manages sensitive configurations and API keys by loading them from `config/.env`.

3.  **CLI RAG Interface (`rag_app.py`):**
    *   A standalone command-line script for direct interaction and testing of the RAG system. It provides an interactive prompt to submit queries and see immediate results from the RAG model.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.x:** (Recommended Python 3.9+)
*   **Git:** For cloning the repository.
*   **Groq API Key:** Obtain one from [Groq](https://groq.com/). This key is essential for the LLM integration.

### Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-repo/RAG-Beluga-cold-therapy.git
    cd RAG-Beluga-cold-therapy
    ```

2.  **Create a virtual environment and install dependencies:**

    It's highly recommended to use a Python virtual environment to manage dependencies. While a `requirements.txt` is not explicitly provided, the core dependencies are: `Flask`, `langchain-huggingface`, `langchain-chroma`, `langchain-groq`, and `python-dotenv`.

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install Flask langchain-huggingface langchain-chroma langchain-groq python-dotenv
    ```

3.  **Configure Environment Variables:**

    Create a file named `.env` inside the `config/` directory and add your Groq API key:

    ```
    # config/.env
    GROQ_API_KEY="your_actual_groq_api_key_here"
    ```
    *Replace `"your_actual_groq_api_key_here"` with the API key you obtained from Groq.*

4.  **Ingest Data:**

    Before running the application, you need to populate the vector database with your knowledge base documents. This step processes the JSON files in the `dataset/` directory.

    ```bash
    python ingest.py
    ```
    This will create a `chroma_db` directory containing your vectorized knowledge base.

### Running the Application

Once the setup is complete and data has been ingested, you can start the Flask web application:

```bash
just run
```
The application will typically be accessible in your web browser at `http://127.0.0.1:5000`.

### Running the CLI RAG Interface (for testing and quick interaction)

For direct command-line interaction with the RAG system (useful for development and testing):

```bash
python rag_app.py
```
You can then type your queries directly into the terminal. Type `exit`, `quit`, or `q` to stop the interactive session.

## Development Guidelines

*   **Python Best Practices:** Adhere to standard Python coding conventions (e.g., PEP 8).
*   **Virtual Environments:** Always work within the `.venv` to maintain clean dependency management.
*   **Configuration Management:** Use `config/.env` for all sensitive credentials and environment-specific settings.
*   **Data Structure:** Ensure knowledge base documents are provided as JSON files in the `dataset/` directory, following a consistent structure (e.g., each object having `title` and `content` fields).
*   **Task Automation:** Utilize the `justfile` for running predefined tasks such as starting the application.

## Contribution

(Add guidelines for contributions if applicable)

## License

(Add license information)
