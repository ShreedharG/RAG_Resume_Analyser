from ingestion.parser import extract_text_from_pdf, normalize_text
from ingestion.chunker import chunk_documents
from embed_pipeline.embedd import get_embedding_function
from vectorstore.chroma_store import get_vector_store

class RAGPipeline:
    def __init__(self):
        self.embedding_fn = get_embedding_function()
        self.vector_store = None
        self.all_chunks = []
        self.resume_chunks = []
        self.jd_chunks = []

    def initialize_pipeline(self, resume_content: bytes, jd_content: bytes):
        """Processes documents and initializes the vector store."""

        # 1. Extract text
        resume_text = extract_text_from_pdf(resume_content)
        jd_text = extract_text_from_pdf(jd_content)

        resume_text = normalize_text(resume_text)
        jd_text = normalize_text(jd_text)

        # 2. Chunk documents
        self.all_chunks = chunk_documents(
            resume_text,
            jd_text,
            chunk_size=200,
            overlap=50
        )

        # 3. Store in Chroma
        self.vector_store = get_vector_store(
            self.all_chunks,
            self.embedding_fn,
            persist_directory="backend/data/embeddings"
        )

        # 4. Separate chunks (FIXED)
        self.resume_chunks = [c for c in self.all_chunks if c["type"] == "resume"]
        self.jd_chunks = [c for c in self.all_chunks if c["type"] == "jd"]

        return {
            "status": "success",
            "total_chunks": len(self.all_chunks),
            "resume_chunks": len(self.resume_chunks),
            "jd_chunks": len(self.jd_chunks)
        }

    def answer_query(self, query: str, k: int = 5):
        """Basic semantic retrieval (no hybrid yet)"""

        if not self.vector_store:
            return "Please upload documents first."

        results = self.vector_store.query(
            query_texts=[query],
            n_results=k
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        scores = results["distances"][0]

        formatted = []

        for doc, meta, score in zip(docs, metas, scores):
            formatted.append({
                "text": doc,
                "source": meta["source"],
                "type": meta["type"],  
                "score": score
            })

        return formatted

if __name__ == "__main__":
    import os

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PROJECT_ROOT = os.path.dirname(BASE_DIR)

    resume_path = os.path.join(PROJECT_ROOT, "test", "Shreedhar_Goyal_SDE-1.pdf")
    jd_path = os.path.join(PROJECT_ROOT, "test", "JD_Data Solutions Associate Intern.pdf")

    print("Resume Path:", resume_path)
    print("JD Path:", jd_path)

    with open(resume_path, "rb") as f:
        resume_bytes = f.read()

    with open(jd_path, "rb") as f:
        jd_bytes = f.read()

    # Initialize pipeline
    pipeline = RAGPipeline()
    init_res = pipeline.initialize_pipeline(resume_bytes, jd_bytes)

    print("\nPipeline Init:", init_res)

    # Query test
    results = pipeline.answer_query("What backend skills match the job?")

    print("\n--- Query Results ---")
    for i, r in enumerate(results):
        print(f"\nResult {i+1}")
        print(f"Score: {r['score']}")
        print(f"Type: {r['type']}")
        print(f"Source: {r['source']}")
        print(f"Text: {r['text'][:200]}...")