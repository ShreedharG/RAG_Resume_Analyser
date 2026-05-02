import chromadb
from chromadb.config import Settings
import os

class ChromaStore:
    def __init__(self, persist_directory: str = "backend/data/embeddings"):
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        
    def get_or_create_collection(self, name: str, embedding_function):
        # We need to wrap the embedding function to match Chroma's expected interface if needed
        # But LangChain's Chroma wrapper is usually easier.
        pass

# We will use LangChain's Chroma wrapper in the main pipeline for simplicity
from langchain_community.vectorstores import Chroma

def get_vector_store(chunks, embedding_function, persist_directory="backend/data/embeddings", collection_name="resume_collection"):
    """Creates and returns a Chroma vector store."""
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
        
    vector_db = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_function,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    vector_db.persist()
    return vector_db

def load_vector_store(embedding_function, persist_directory="backend/data/embeddings", collection_name="resume_collection"):
    """Loads an existing Chroma vector store."""
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function,
        collection_name=collection_name
    )
