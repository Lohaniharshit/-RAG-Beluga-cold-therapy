# Project Overview: -RAG-Beluga-cold-therapy

This project is a Flask-based Retrieval-Augmented Generation (RAG) application designed to provide medical device support, specifically for "Beluga Health" products. The application integrates a web-based chat interface where users can ask questions, and the RAG system will provide answers based on a pre-built knowledge base, citing sources. The project's name suggests a focus on "cold therapy" related medical devices.

**Key Technologies:**
*   **Backend Framework:** Flask (Python)
*   **Embedding Model:** HuggingFace `all-MiniLM-L6-v2`
*   **Vector Store:** Chroma
*   **Large Language Model (LLM):** Groq `llama-3.3-70b-versatile`
*   **Environment Management:** Python virtual environment
*   **Task Runner:** `just` (via `justfile`)
*   **Frontend:** HTML, CSS, JavaScript (single-page application)

**Architecture:**
The application consists of two main components:
1.  **Data Ingestion (`ingest.py`):** This script processes JSON documents from the `dataset` directory, embeds their content using `all-MiniLM-L6-v2`, and stores them in a Chroma vector database (`chroma_db`). This forms the knowledge base for the RAG system.
2.  **Web Application (`app.py`):** This is a Flask web server that:
    *   Serves an `index.html` frontend for user interaction.
    *   Exposes a `/api/chat` endpoint.
    *   Initializes and uses the RAG system (HuggingFace embeddings, Chroma vector store, Groq LLM) to answer user queries.
    *   Loads API keys and configurations from `config/.env`.

A separate script, `rag_app.py`, provides a command-line interface for direct interaction and testing of the RAG system.

## Building and Running

### Prerequisites

*   Python 3.x
*   A Groq API key (to be placed in `config/.env`)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/RAG-Beluga-cold-therapy.git
    cd RAG-Beluga-cold-therapy
    ```
2.  **Create a virtual environment and install dependencies:**
    *(Note: While `requirements.txt` is not present, you will need to install the dependencies manually. Based on the code, these include `Flask`, `langchain-huggingface`, `langchain-chroma`, `langchain-groq`, `python-dotenv`.)*
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install Flask langchain-huggingface langchain-chroma langchain-groq python-dotenv
    ```
3.  **Configure Environment Variables:**
    Create a `config/.env` file with your Groq API key:
    ```
    GROQ_API_KEY="your_api_key_here"
    ```
    *Replace `"your_api_key_here"` with your actual Groq API Key.*

4.  **Ingest Data:**
    Populate the Chroma vector database by running the ingestion script:
    ```bash
    python ingest.py
    ```
    This will process JSON files in the `dataset` directory and create the `chroma_db`.

### Running the Application

To start the Flask web application:

```bash
just run
```
The application will typically run on `http://127.0.0.1:5000`.

### Running the CLI RAG Interface (for testing)

To interact with the RAG system via the command line:

```bash
python rag_app.py
```
Type your queries at the prompt.

## Development Conventions

*   **Python Best Practices:** Follows standard Python coding practices.
*   **Virtual Environments:** Uses `.venv` for dependency isolation.
*   **Configuration:** Sensitive information and API keys are managed via `config/.env`.
*   **Data Format:** Knowledge base documents are expected to be in JSON format within the `dataset` directory.
*   **Task Automation:** `justfile` is used for defining and running common project tasks.
*   **Linting/Formatting:** (To be inferred or added if present - *no explicit tools found in analysis*)
*   **Testing:** (To be inferred or added if present - *no explicit testing framework found in analysis*)
