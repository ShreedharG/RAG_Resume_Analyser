from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from rag_pipeline import RAGPipeline
import uvicorn
import os

from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

app = FastAPI(title="Resume Intel RAG API")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from session_manager import list_sessions, get_session, add_message, create_session
from datetime import datetime
import uuid

# Global pipeline instance
pipeline = RAGPipeline()

RAW_UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "data", "raw_upload")
os.makedirs(RAW_UPLOAD_DIR, exist_ok=True)

@app.post("/initialize")
async def initialize(resume: UploadFile = File(...), jd: UploadFile = File(...)):
    try:
        resume_bytes = await resume.read()
        jd_bytes = await jd.read()
        
        if not resume_bytes or not jd_bytes:
            return {"status": "error", "message": "Files cannot be empty"}, 400
        
        # Save raw files
        with open(os.path.join(RAW_UPLOAD_DIR, resume.filename), "wb") as f:
            f.write(resume_bytes)
        with open(os.path.join(RAW_UPLOAD_DIR, jd.filename), "wb") as f:
            f.write(jd_bytes)
        
        # Process RAG
        result = pipeline.initialize_pipeline(resume_bytes, jd_bytes)
        
        # Create a new session
        session_id = str(uuid.uuid4())
        title = f"Analysis: {resume.filename.split('.')[0]} ({datetime.now().strftime('%H:%M')})"
        session_data = create_session(session_id, title)
        
        return {"status": "success", "session": session_data}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.post("/chat")
async def chat(session_id: str = Form(...), query: str = Form(...)):
    try:
        # Verify session exists
        session = get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}, 404
        
        if not query or not query.strip():
            return {"status": "error", "message": "Query cannot be empty"}, 400
        
        # 1. Save user message
        add_message(session_id, "user", query)
        
        # 2. Generate AI response
        response = pipeline.answer_query(query)
        
        # 3. Save AI message
        add_message(session_id, "ai", response)
        
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.get("/sessions")
def get_all_sessions():
    return list_sessions()

@app.get("/sessions/{session_id}")
def get_single_session(session_id: str):
    try:
        session = get_session(session_id)
        if not session:
            return {"status": "error", "message": "Session not found"}, 404
        return {"status": "success", "session": session}
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

@app.get("/health")
def health():
    return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
