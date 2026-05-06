const API_BASE = "http://localhost:8000";

const handleResponse = async (response) => {
    const data = await response.json();
    if (!response.ok) {
        throw new Error(data.message || `HTTP ${response.status}`);
    }
    return data;
};

export const api = {
    async initialize(resume, jd) {
        const formData = new FormData();
        formData.append("resume", resume);
        formData.append("jd", jd);
        
        const response = await fetch(`${API_BASE}/initialize`, {
            method: "POST",
            body: formData,
        });
        return handleResponse(response);
    },

    async chat(sessionId, query) {
        const formData = new FormData();
        formData.append("session_id", sessionId);
        formData.append("query", query);
        
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            body: formData,
        });
        return handleResponse(response);
    },

    async getSessions() {
        const response = await fetch(`${API_BASE}/sessions`);
        return handleResponse(response);
    },

    async getSession(id) {
        const response = await fetch(`${API_BASE}/sessions/${id}`);
        return handleResponse(response);
    },

    async deleteSession(id) {
        const response = await fetch(`${API_BASE}/sessions/${id}`, {
            method: "DELETE",
        });
        return handleResponse(response);
    },

    async healthCheck() {
        try {
            const response = await fetch(`${API_BASE}/health`);
            return handleResponse(response);
        } catch (error) {
            throw new Error("Backend not reachable");
        }
    }
};
