import chromadb
import os

class ChromaStore:
    def __init__(self, persist_directory: str = "backend/data/embeddings"):
        # 🔥 Always resolve absolute path
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.persist_directory = os.path.join(BASE_DIR, persist_directory)

        if not os.path.exists(self.persist_directory):
            os.makedirs(self.persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(path=self.persist_directory)

    def get_or_create_collection(self, name: str, embedding_function):
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=embedding_function
        )


# -------------------------------
# MAIN VECTOR STORE FUNCTION
# -------------------------------
def get_vector_store(
    chunks,
    embedding_function,
    persist_directory="backend/data/embeddings",
    collection_name="resume_jd_collection"
):
    """
    Creates or updates Chroma collection using native chromadb.
    """

    store = ChromaStore(persist_directory)
    collection = store.get_or_create_collection(collection_name, embedding_function)

    # Extract text + metadata
    texts = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "type": c.get("type", "unknown")} for c in chunks]

    # Unique IDs (important to avoid duplicates)
    ids = [
        f"{c['source']}_chunk_{i}"
        for i, c in enumerate(chunks)
    ]

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids
    )

    return collection


# -------------------------------
# LOAD EXISTING COLLECTION
# -------------------------------
def load_vector_store(
    embedding_function,
    persist_directory="backend/data/embeddings",
    collection_name="resume_jd_collection"
):
    store = ChromaStore(persist_directory)
    return store.get_or_create_collection(collection_name, embedding_function)