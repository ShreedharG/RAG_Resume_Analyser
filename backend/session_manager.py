import json
import os
from datetime import datetime

SESSIONS_FILE = "backend/data/chats/chat_history.json"

def ensure_sessions_file():
    os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, "w") as f:
            json.dump({}, f)

def load_sessions():
    ensure_sessions_file()
    with open(SESSIONS_FILE, "r") as f:
        return json.load(f)

def save_sessions(sessions):
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f, indent=4)

def create_session(session_id: str, title: str):
    sessions = load_sessions()
    sessions[session_id] = {
        "id": session_id,
        "title": title,
        "created_at": datetime.now().isoformat(),
        "messages": []
    }
    save_sessions(sessions)
    return sessions[session_id]

def add_message(session_id: str, role: str, content: str):
    sessions = load_sessions()
    if session_id in sessions:
        sessions[session_id]["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        save_sessions(sessions)
        return True
    return False

def get_session(session_id: str):
    sessions = load_sessions()
    return sessions.get(session_id)

def list_sessions():
    sessions = load_sessions()
    # Return metadata only for list
    return [
        {"id": s["id"], "title": s["title"], "created_at": s["created_at"]}
        for s in sessions.values()
    ]
