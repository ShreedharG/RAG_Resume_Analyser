from sentence_transformers import SentenceTransformer

class LocalEmbeddingWrapper:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def __call__(self, input):
        """Chroma calls this for document embedding"""
        if isinstance(input, str):
            input = [input]
        return self.model.encode(input).tolist()

    def embed_documents(self, texts):
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts).tolist()

    def embed_query(self, input):
        """Must return LIST of embeddings, not a single vector"""
        if isinstance(input, str):
            input = [input]
        return self.model.encode(input).tolist()

    def name(self):
        return "local_sentence_transformer"


def get_embedding_function():
    return LocalEmbeddingWrapper()