from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    def __init__(self, vector_store, chunks):
        self.vector_store = vector_store
        self.chunks = chunks
        # Tokenize chunks for BM25
        tokenized_chunks = [chunk.lower().split() for chunk in chunks]
        self.bm25 = BM25Okapi(tokenized_chunks)

    def get_relevant_documents(self, query: str, k: int = 4):
        # 1. Vector Search
        vector_results = self.vector_store.similarity_search(query, k=k)
        vector_contents = [doc.page_content for doc in vector_results]
        
        # 2. BM25 Search
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        top_n_bm25_indices = np.argsort(bm25_scores)[-k:][::-1]
        bm25_contents = [self.chunks[i] for i in top_n_bm25_indices]
        
        # 3. Combine (Simple deduplication for now)
        combined = list(set(vector_contents + bm25_contents))
        return combined[:k]
