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


def get_vector_store(chunks, embedding_function, persist_directory="backend/data/embeddings", collection_name="resume_jd_collection"):
    """Creates or updates a Chroma vector store with metadata."""
    if not os.path.exists(persist_directory):
        os.makedirs(persist_directory)
        
    # Extract text and metadata from chunks (which are dicts)
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"]} for c in chunks]
        
    if os.path.exists(os.path.join(persist_directory, "chroma.sqlite3")):
        # Load existing and add new texts
        vector_db = load_vector_store(embedding_function, persist_directory, collection_name)
        vector_db.add_texts(texts=texts, metadatas=metadatas)
    else:
        # Create new vector store
        vector_db = Chroma.from_texts(
            texts=texts,
            embedding=embedding_function,
            metadatas=metadatas,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
    
    vector_db.persist()
    return vector_db

def load_vector_store(embedding_function, persist_directory="backend/data/embeddings", collection_name="resume_jd_collection"):
    """Loads an existing Chroma vector store."""
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function,
        collection_name=collection_name
    )
