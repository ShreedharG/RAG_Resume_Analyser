import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import Dashboard from './components/Dashboard/Dashboard';
import ChatInterface from './components/Chat/ChatInterface';
import './styles/global.css';
import { api } from './services/api';

function App() {
    const [view, setView] = useState('upload'); // 'upload' or 'chat'
    const [history, setHistory] = useState([]);
    const [activeSession, setActiveSession] = useState(null);
    const [messages, setMessages] = useState([]);

    // Load history from backend
    useEffect(() => {
        fetchSessions();
    }, []);

    const fetchSessions = async () => {
        try {
            const data = await api.getSessions();
            setHistory(data);
        } catch (error) {
            console.error("Failed to fetch sessions:", error);
        }
    };

    const handleStartAnalysis = async (files) => {
        try {
            const result = await api.initialize(files.resume, files.jd);
            if (result.session) {
                setHistory(prev => [result.session, ...prev]);
                setActiveSession(result.session.id);
                setMessages([]);
                setView('chat');
            }
        } catch (error) {
            console.error("Analysis failed:", error);
        }
    };

    const handleSendMessage = async (text) => {
        // Optimistic UI update
        const userMsg = { role: 'user', content: text };
        setMessages(prev => [...prev, userMsg]);

        try {
            const result = await api.chat(activeSession, text);
            const aiMsg = { role: 'ai', content: result.response };
            setMessages(prev => [...prev, aiMsg]);
        } catch (error) {
            console.error("Chat failed:", error);
        }
    };

    const handleNewChat = () => {
        setView('upload');
        setMessages([]);
        setActiveSession(null);
    };

    const handleSelectSession = async (id) => {
        try {
            const session = await api.getSession(id);
            setActiveSession(id);
            setMessages(session.messages || []);
            setView('chat');
        } catch (error) {
            console.error("Failed to load session:", error);
        }
    };

    return (
        <div className="app-container">
            <Sidebar 
                history={history} 
                activeSession={activeSession}
                onNewChat={handleNewChat}
                onSelectSession={handleSelectSession}
            />
            
            <main className="main-content" style={{ flex: 1, position: 'relative' }}>
                <header className="top-nav" style={{ height: '64px', borderBottom: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', padding: '0 2rem' }}>
                    <div className="status-indicator" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        <span className="dot" style={{ width: '8px', height: '8px', background: '#10b981', borderRadius: '50%', boxShadow: '0 0 8px #10b981' }}></span>
                        RAG Pipeline Ready
                    </div>
                </header>

                {view === 'upload' ? (
                    <Dashboard onStartAnalysis={handleStartAnalysis} />
                ) : (
                    <ChatInterface messages={messages} onSendMessage={handleSendMessage} />
                )}
            </main>
        </div>
    );
}

export default App;
