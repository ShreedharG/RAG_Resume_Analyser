# ──────────────────────────────────────────────
# Backend Dockerfile — FastAPI + Uvicorn
# ──────────────────────────────────────────────
FROM python:3.11-slim

# System deps needed by pdfplumber / chromadb
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/backend

# Install Python dependencies first (layer cache optimisation)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Pre-download the sentence-transformers model so cold-start is fast
# This runs at BUILD time, not at container start
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Copy backend source
COPY backend/ /app/backend/

# Create persistent data directories
# (these will be overridden by the Docker volume at runtime)
RUN mkdir -p /app/backend/data/raw_upload \
             /app/backend/data/embeddings \
             /app/backend/data/chats

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
