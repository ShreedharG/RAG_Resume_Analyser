const API_BASE = "http://localhost:8000";

export const api = {
    async initialize(resume, jd) {
        const formData = new FormData();
        formData.append("resume", resume);
        formData.append("jd", jd);
        
        const response = await fetch(`${API_BASE}/initialize`, {
            method: "POST",
            body: formData,
        });
        return response.json();
    },

    async chat(sessionId, query) {
        const formData = new FormData();
        formData.append("session_id", sessionId);
        formData.append("query", query);
        
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            body: formData,
        });
        return response.json();
    },

    async getSessions() {
        const response = await fetch(`${API_BASE}/sessions`);
        return response.json();
    },

    async getSession(id) {
        const response = await fetch(`${API_BASE}/sessions/${id}`);
        return response.json();
    }
};
