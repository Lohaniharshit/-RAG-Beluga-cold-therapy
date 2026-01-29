import os
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="config/.env")

CHROMA_DB_DIR = "chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def main():
    if not GROQ_API_KEY or GROQ_API_KEY == "your_api_key_here":
        print("Error: GROQ_API_KEY not found in config/.env")
        print("Please add your key to config/.env")
        return

    print("Initializing components...")
    
    # 1. Load Embeddings
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    
    # 2. Load Vector Store
    if not os.path.exists(CHROMA_DB_DIR):
         print(f"Error: {CHROMA_DB_DIR} not found. Run ingest.py first.")
         return

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
    
    # 4. Create Retrieval Chain
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
    
    print("\n--- Quick RAG Solution (Type 'exit' to quit) ---\n")
    
    while True:
        query = input("Query: ")
        if query.lower() in ["exit", "quit", "q"]:
            break
            
        if not query.strip():
            continue
            
        try:
            print("Thinking...")
            result = qa_chain.invoke({"query": query})
            answer = result["result"]
            sources = result["source_documents"]
            
            print(f"\nAnswer: {answer}\n")
            print("Sources:")
            for i, doc in enumerate(sources, 1):
                print(f"{i}. {doc.metadata.get('title', 'Unknown')} (Source: {os.path.basename(doc.metadata.get('source', ''))})")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
