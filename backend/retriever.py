import re
from collections import Counter


class HybridRetriever:
    def __init__(self, collection, embedding_fn):
        self.collection = collection
        self.embedding_fn = embedding_fn

    # -------------------------------
    # Simple keyword scoring
    # -------------------------------
    def _keyword_score(self, query, text):
        STOPWORDS = {"what", "is", "the", "are", "does", "do", "a", "an", "of", "and", "to", "in"}

        query_words = [
            w for w in re.findall(r"\w+", query.lower())
            if w not in STOPWORDS
        ]

        text_words = re.findall(r"\w+", text.lower())
        text_freq = Counter(text_words)

        score = 0
        for word in query_words:
            score += text_freq.get(word, 0)

        return score

    # -------------------------------
    # Semantic retrieval + reranking
    # -------------------------------
    def get_relevant_documents(self, query, k_resume=3, k_jd=3, min_score=0.0):
        results = self.collection.query(
            query_texts=[query],
            n_results=12  # fetch a bit more, then filter
        )

        docs = results["documents"][0]
        metas = results["metadatas"][0]
        distances = results["distances"][0]

        combined = []

        for doc, meta, dist in zip(docs, metas, distances):
            # filter junk
            if len(doc.split()) < 20:
                continue

            semantic_score = 1 / (1 + dist)
            keyword_score = self._keyword_score(query, doc)
            keyword_score_norm = min(keyword_score / 5, 1)

            final_score = 0.7 * semantic_score + 0.3 * keyword_score_norm

            if final_score < min_score:
                continue

            combined.append({
                "text": doc,
                "type": meta["type"],
                "source": meta["source"],
                "score": final_score
            })

        combined.sort(key=lambda x: x["score"], reverse=True)

        resume_chunks = [c for c in combined if c["type"] == "resume"][:k_resume]
        jd_chunks     = [c for c in combined if c["type"] == "jd"][:k_jd]

        return {
            "resume_chunks": resume_chunks,
            "jd_chunks": jd_chunks
        }