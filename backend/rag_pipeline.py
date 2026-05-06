from parser import extract_text_from_pdf, normalize_text
from chunker import chunk_documents
from embedd import get_embedding_function
from chroma_store import get_vector_store
from retriever import HybridRetriever
from generator import generate

class RAGPipeline:
    def __init__(self):
        self.embedding_fn = get_embedding_function()
        self.vector_store = None
        self.retriever = None
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

        # 4. Initialize retriever
        self.retriever = HybridRetriever(
            self.vector_store,
            self.embedding_fn
        )

        # 5. Split chunks
        self.resume_chunks = [c for c in self.all_chunks if c["type"] == "resume"]
        self.jd_chunks = [c for c in self.all_chunks if c["type"] == "jd"]

        return {
            "status": "success",
            "total_chunks": len(self.all_chunks),
            "resume_chunks": len(self.resume_chunks),
            "jd_chunks": len(self.jd_chunks)
        }
    
    def build_context(self, results, k=5):
        context = ""

        resume_chunks = results["resume_chunks"][:k]
        jd_chunks = results["jd_chunks"][:k]

        for r in resume_chunks:
            context += f"[RESUME]\n{r['text']}\n\n"

        for r in jd_chunks:
            context += f"[JOB DESCRIPTION]\n{r['text']}\n\n"

        return context.strip()
    
    def answer_query(self, query: str):
        if not self.retriever:
            return "Please upload documents first."

        results = self.retriever.get_relevant_documents(query)

        context = self.build_context(results)

        prompt = f"""
You are an AI Resume Analyzer.

Your task is to compare the candidate resume with the job description using ONLY the provided context.

Return STRICT VALID JSON ONLY.
Do NOT return markdown.
Do NOT return explanations outside JSON.
Do NOT wrap response inside ```json.

JSON format rules:
- "reason" MUST always exist
- "matching_skills" is OPTIONAL
- "missing_skills" is OPTIONAL
- Include a field ONLY if data exists
- Never hallucinate skills
- Only use skills explicitly present in context

Valid response examples:

{{"reason":"Candidate information is insufficient."}}

{{"matching_skills":[""],"reason":""}}

{{"missing_skills":[""],"reason":""}}

{{"matching_skills":[""],"missing_skills":[""],"reason":""}}

Output requirements:
- JSON must be syntactically valid
- Arrays must contain strings only
- Keep response concise
- No trailing commas
- No extra keys

Context:
{context}

Question:
{query}
"""
        answer = generate(prompt)

        return {
            "answer": answer,
            "debug": results
        }