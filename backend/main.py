from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
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
            raise HTTPException(status_code=400, detail="Files cannot be empty")
        
        # Save raw files
        try:
            with open(os.path.join(RAW_UPLOAD_DIR, resume.filename), "wb") as f:
                f.write(resume_bytes)
            with open(os.path.join(RAW_UPLOAD_DIR, jd.filename), "wb") as f:
                f.write(jd_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save files: {str(e)}")
        
        # Process RAG
        try:
            result = pipeline.initialize_pipeline(resume_bytes, jd_bytes)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Pipeline initialization failed: {str(e)}")
        
        # Create a new session
        session_id = str(uuid.uuid4())
        title = f"{resume.filename.split('.')[0]} ({datetime.now().strftime('%H:%M')})"
        session_data = create_session(session_id, title, resume.filename, jd.filename)
        
        return {"status": "success", "session": session_data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(session_id: str = Form(...), query: str = Form(...)):
    try:
        # Verify session exists
        session = get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if not query or not query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # 1. Save user message
        add_message(session_id, "user", query)
        
        # 2. Generate AI response
        try:
            pipeline_result = pipeline.answer_query(query)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Pipeline query failed: {str(e)}")
            
        # Extract the answer string (which is the AI response)
        # If pipeline_result is already a string (fallback), use it; otherwise get the 'answer' field
        answer = pipeline_result.get("answer", str(pipeline_result)) if isinstance(pipeline_result, dict) else str(pipeline_result)
        
        # 3. Save AI message
        add_message(session_id, "ai", answer)
        
        return {"status": "success", "response": answer}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sessions")
def get_all_sessions():
    return list_sessions()

@app.get("/sessions/{session_id}")
def get_single_session(session_id: str):
    try:
        session = get_session(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"status": "success", "session": session}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/sessions/{session_id}")
def delete_session_endpoint(session_id: str):
    try:
        from session_manager import delete_session
        success = delete_session(session_id)
        if not success:
            raise HTTPException(status_code=404, detail="Session not found")
        return {"status": "success"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health():
    return {"status": "online"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
