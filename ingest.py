import os
import json
import glob
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
# from langchain_community.vectorstores import Chroma # Deprecated, using langchain_chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="config/.env")

# Configuration
DATASET_DIR = "dataset"
CHROMA_DB_DIR = "chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def load_documents_from_json(dataset_dir):
    documents = []
    json_files = glob.glob(os.path.join(dataset_dir, "*.json"))
    
    print(f"Found {len(json_files)} JSON files in {dataset_dir}")

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Check if data is a list of items (dataset format)
                if isinstance(data, list):
                    items = data
                elif isinstance(data, dict):
                    # Try to find a list value, or treat strict dict as one item
                    items = [data]
                else:
                    print(f"Skipping {file_path}: Unknown format")
                    continue
                
                for item in items:
                    title = item.get("title", "No Title")
                    content = item.get("content", "")
                    
                    # specific handling if content is a list of strings
                    if isinstance(content, list):
                        text_content = "\n".join(content)
                    else:
                        text_content = str(content)
                    
                    full_text = f"Title: {title}\nContent: {text_content}"
                    
                    metadata = {
                        "source": file_path,
                        "title": title
                    }
                    
                    doc = Document(page_content=full_text, metadata=metadata)
                    documents.append(doc)
                    
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    return documents

def main():
    print("Loading documents...")
    docs = load_documents_from_json(DATASET_DIR)
    print(f"Loaded {len(docs)} documents.")

    if not docs:
        print("No documents found. Exiting.")
        return

    print(f"Initializing HuggingFace Embeddings ({EMBEDDING_MODEL_NAME})...")
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    print(f"Creating Chroma vector store in {CHROMA_DB_DIR}...")
    # This automatically persists to disk in newer langchain-chroma versions if directory is provided
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=CHROMA_DB_DIR
    )
    
    print("Ingestion complete. Vector store created.")

if __name__ == "__main__":
    main()
