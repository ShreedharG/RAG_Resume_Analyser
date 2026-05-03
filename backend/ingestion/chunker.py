"""
Splits text into overlapping word-based chunks.

Args:
    text (str): Input text
    chunk_size (int): Number of words per chunk
    overlap (int): Number of overlapping words between chunks

Returns:
    List[str]: List of text chunks
"""

def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50):
    words = text.split()
    chunks = []

    step = chunk_size - overlap

    for i in range(0, len(words), step):
        chunk_words = words[i:i + chunk_size]
        if not chunk_words:
            continue

        chunk = " ".join(chunk_words)
        chunks.append(chunk)

    return chunks

def chunk_documents(resume_text: str, jd_text: str, chunk_size=200, overlap=50):
    all_chunks = []

    # Resume chunks
    resume_chunks = chunk_text(resume_text, chunk_size, overlap)
    for chunk in resume_chunks:
        all_chunks.append({"text": chunk,"source": "resume"})

    # JD chunks
    jd_chunks = chunk_text(jd_text, chunk_size, overlap)
    for chunk in jd_chunks:
        all_chunks.append({"text": chunk,"source": "jd"})

    return all_chunks