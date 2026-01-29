import os
from flask import Flask, render_template, request, jsonify
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

from src.logger import setup_logger

# Load environment variables
load_dotenv(dotenv_path="config/.env")

app = Flask(__name__)
logger = setup_logger(__name__)

# Configuration
CHROMA_DB_DIR = "chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Global variable to store the chain
qa_chain = None

def initialize_rag():
    global qa_chain
    
    if not GROQ_API_KEY or GROQ_API_KEY == "your_api_key_here":
        logger.error("GROQ_API_KEY not found in config/.env")
        return False

    logger.info("Initializing RAG components...")
    
    # 1. Load Embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # 2. Load Vector Store
    if not os.path.exists(CHROMA_DB_DIR):
         logger.error(f"{CHROMA_DB_DIR} not found. Run ingest.py first.")
         return False

    vectorstore = Chroma(
        persist_directory=CHROMA_DB_DIR,
        embedding_function=embeddings
    )
    
    # 3. Initialize LLM
    llm = ChatGroq(
        temperature=0,
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile"
    )
    
    # 4. Create Retrieval Chain with Custom Prompt
    template = """You are a helpful AI assistant specialized in medical device support for Beluga Health.
    Use the following pieces of context to answer the question at the end.
    If the answer is not in the context, say that you don't know, do not try to make up an answer.
    Keep the answer concise and professional.

    Context:
    {context}

    Question: {question}

    Helpful Answer:"""
    
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
    )
    
    logger.info("RAG initialized successfully.")
    return True

# Initialize on startup
if not initialize_rag():
    logger.error("Failed to initialize RAG. App may not work correctly.")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    if not qa_chain:
        return jsonify({"error": "RAG system not initialized"}), 500
    
    data = request.json
    query = data.get('query')
    
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        result = qa_chain.invoke({"query": query})
        answer = result["result"]
        source_docs = result["source_documents"]
        
        sources = []
        for doc in source_docs:
            sources.append({
                "title": doc.metadata.get('title', 'Unknown'),
                "source": os.path.basename(doc.metadata.get('source', '')),
                "content": doc.page_content[:200] + "..." # Preview
            })
            
        return jsonify({
            "answer": answer,
            "sources": sources
        })
        
    except Exception as e:
        logger.error(f"Error during query: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
