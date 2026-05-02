from .ingestion.parser import extract_text_from_pdf
from .ingestion.chunker import chunk_text
from .embeddings.embedding import get_embedding_function
from .vectorstore.chroma_store import get_vector_store
from .retrieval.retriever import HybridRetriever
from .generation.generator import Generator
import os

class RAGPipeline:
    def __init__(self):
        self.embedding_fn = get_embedding_function()
        self.generator = Generator()
        self.vector_store = None
        self.retriever = None
        self.all_chunks = []

    def initialize_pipeline(self, resume_content: bytes, jd_content: bytes):
        """Processes documents and initializes the vector store."""
        resume_text = extract_text_from_pdf(resume_content)
        jd_text = extract_text_from_pdf(jd_content)
        
        combined_text = f"RESUME CONTENT:\n{resume_text}\n\nJOB DESCRIPTION:\n{jd_text}"
        self.all_chunks = chunk_text(combined_text)
        
        # Initialize Vector Store
        self.vector_store = get_vector_store(self.all_chunks, self.embedding_fn, persist_directory="backend/data/embeddings")
        
        # Initialize Hybrid Retriever
        self.retriever = HybridRetriever(self.vector_store, self.all_chunks)
        
        return {"status": "success", "chunks": len(self.all_chunks)}

    def answer_query(self, query: str):
        if not self.retriever:
            return "Please upload documents first."
        
        context_docs = self.retriever.get_relevant_documents(query)
        context_str = "\n---\n".join(context_docs)
        
        response = self.generator.generate_response(query, context_str)
        return response
