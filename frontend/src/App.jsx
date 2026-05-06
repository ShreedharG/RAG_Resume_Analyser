import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar/Sidebar';
import Dashboard from './components/Dashboard/Dashboard';
import ChatInterface from './components/Chat/ChatInterface';
import LandingPage from './components/Landing/LandingPage';
import './styles/global.css';
import { api } from './services/api';

function App() {
    const [view, setView] = useState('landing'); // 'landing', 'upload', 'chat'
    const [history, setHistory] = useState([]);
    const [activeSession, setActiveSession] = useState(null);
    const [messages, setMessages] = useState([]);
    const [backendStatus, setBackendStatus] = useState('checking'); // 'checking', 'online', 'offline'
    const [isThinking, setIsThinking] = useState(false);

    // Load history from backend
    useEffect(() => {
        fetchSessions();
        checkBackendHealth();
        
        // Check backend health every 30 seconds
        const healthInterval = setInterval(checkBackendHealth, 30000);
        return () => clearInterval(healthInterval);
    }, []);

    const checkBackendHealth = async () => {
        try {
            await api.healthCheck();
            setBackendStatus('online');
        } catch (error) {
            setBackendStatus('offline');
            console.error("Backend health check failed:", error);
        }
    };

    const fetchSessions = async () => {
        try {
            const data = await api.getSessions();
            data.reverse();
            setHistory(data);
        } catch (error) {
            console.error("Failed to fetch sessions:", error);
        }
    };

    const handleStartAnalysis = async (files) => {
        try {
            const result = await api.initialize(files.resume, files.jd);
            if (result.status === "success" && result.session) {
                setHistory(prev => [result.session, ...prev]);
                setActiveSession(result.session.id);
                setMessages([]);
                setView('chat');
            }
        } catch (error) {
            console.error("Analysis failed:", error);
            alert(`Failed to initialize analysis: ${error.message}`);
        }
    };

    const handleSendMessage = async (text) => {
        // Optimistic UI update
        const userMsg = { role: 'user', content: text };
        setMessages(prev => [...prev, userMsg]);
        setIsThinking(true);

        try {
            const result = await api.chat(activeSession, text);
            if (result.status === "success") {
                const aiMsg = { role: 'ai', content: result.response };
                setMessages(prev => [...prev, aiMsg]);
            }
        } catch (error) {
            console.error("Chat failed:", error);
            // Remove the optimistic user message and show error
            setMessages(prev => prev.slice(0, -1));
            alert(`Failed to send message: ${error.message}`);
        } finally {
            setIsThinking(false);
        }
    };

    const handleNewChat = () => {
        setView('upload');
        setMessages([]);
        setActiveSession(null);
    };

    const handleSelectSession = async (id) => {
        try {
            const result = await api.getSession(id);
            if (result.status === "success" && result.session) {
                setActiveSession(id);
                setMessages(result.session.messages || []);
                setView('chat');
            }
        } catch (error) {
            console.error("Failed to load session:", error);
            alert(`Failed to load session: ${error.message}`);
        }
    };

    const handleDeleteSession = async (id) => {
        try {
            await api.deleteSession(id);
            setHistory(prev => prev.filter(s => s.id !== id));
            if (activeSession === id) {
                setView('upload');
                setMessages([]);
                setActiveSession(null);
            }
        } catch (error) {
            console.error("Failed to delete session:", error);
            alert(`Failed to delete session: ${error.message}`);
        }
    };

    return (
        <div className="app-container">
            {view === 'landing' && <LandingPage onEnterApp={() => setView('upload')} />}
            
            <Sidebar 
                history={history} 
                activeSession={activeSession}
                onNewChat={handleNewChat}
                onSelectSession={handleSelectSession}
                onDeleteSession={handleDeleteSession}
            />
            
            <main className="main-content" style={{ flex: 1, position: 'relative' }}>
                <header className="top-nav" style={{ height: '64px', borderBottom: '1px solid var(--glass-border)', display: 'flex', alignItems: 'center', padding: '0 2rem' }}>
                    <div className="status-indicator" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        <span 
                            className="dot" 
                            style={{ 
                                width: '8px', 
                                height: '8px', 
                                borderRadius: '50%', 
                                boxShadow: backendStatus === 'online' ? '0 0 8px #10b981' : '0 0 8px #ef4444',
                                background: backendStatus === 'online' ? '#10b981' : backendStatus === 'offline' ? '#ef4444' : '#f59e0b'
                            }}
                        ></span>
                        {backendStatus === 'online' ? 'RAG Pipeline Ready' : backendStatus === 'offline' ? 'Backend Offline' : 'Checking Connection...'}
                    </div>
                </header>

                {view === 'upload' ? (
                    <Dashboard onStartAnalysis={handleStartAnalysis} backendStatus={backendStatus} />
                ) : (
                    <ChatInterface 
                        messages={messages} 
                        onSendMessage={handleSendMessage} 
                        backendStatus={backendStatus} 
                        isThinking={isThinking}
                    />
                )}
            </main>
        </div>
    );
}

export default App;
