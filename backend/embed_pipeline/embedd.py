from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()
client = OpenAI()

class OpenAIEmbeddingWrapper:
    """
    A wrapper class to make OpenAI embeddings compatible with 
    LangChain's expected interface (embed_documents and embed_query).
    """
    def __init__(self, model="text-embedding-3-small"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
        
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def embed_documents(self, texts):
        if isinstance(texts, str):
            texts = [texts]
            
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [item.embedding for item in response.data]

    def embed_query(self, text):
        """Embeds a single query string."""
        response = self.client.embeddings.create(
            model=self.model,
            input=[text]
        )
        return response.data[0].embedding

def get_embedding_function():
    """Returns an instance of the embedding wrapper."""
    return OpenAIEmbeddingWrapper()

if __name__ == "__main__":
    # Test the embedding function
    embedder = get_embedding_function()
    
    # Single text test
    test_text = "Your text string goes here"
    embedding = embedder.embed_query(test_text)
    
    print(f"Successfully generated embedding for: '{test_text}'")
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 dimensions: {embedding[:5]}")
