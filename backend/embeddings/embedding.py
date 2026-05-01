from langchain_community.embeddings import SentenceTransformerEmbeddings

def get_embedding_function(model_name: str = "all-MiniLM-L6-v2"):
    """Returns a LangChain compatible embedding function."""
    return SentenceTransformerEmbeddings(model_name=model_name)
