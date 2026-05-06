import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';
import AnalysisResult from './AnalysisResult';

const ChatInterface = ({ messages, onSendMessage, backendStatus, isThinking }) => {
    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages, isThinking]);

    const handleSubmit = (e) => {
        if (e) e.preventDefault();
        if (input.trim() && backendStatus === 'online' && !isThinking) {
            onSendMessage(input);
            setInput("");
        }
    };

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    const isBackendOnline = backendStatus === 'online';

    return (
        <div className="chat-interface">
            <div className="messages-container">
                {messages.length === 0 ? (
                    <div className="empty-chat">
                        <div className="welcome-card">
                            <i className="fas fa-comments"></i>
                            <h2>Start Conversation</h2>
                            <p>Ask anything about the alignment between your resume and the JD.</p>
                            <div className="suggestion-chips">
                                {["How well do I fit this role?", "What key skills am I missing?", "Summarize the job"].map(chip => (
                                    <button key={chip} className="chip" onClick={() => onSendMessage(chip)}>{chip}</button>
                                ))}
                            </div>
                        </div>
                    </div>
                ) : (
                    messages.map((msg, i) => (
                        <div key={i} className={`message ${msg.role}`}>
                            <div className="message-avatar">
                                <i className={`fas fa-${msg.role === 'ai' ? 'robot' : 'user'}`}></i>
                            </div>
                            <div className="message-bubble">
                                {typeof msg.content === 'string' ? (
                                    msg.content.trim().startsWith('{') || msg.content.trim().startsWith('```json') ? (
                                        <AnalysisResult data={msg.content} />
                                    ) : (
                                        msg.content
                                    )
                                ) : (
                                    <AnalysisResult data={msg.content} />
                                )}
                            </div>
                        </div>
                    ))
                )}
                
                {isThinking && (
                    <div className="thinking-wrapper">
                        <div className="message-avatar" style={{ background: 'var(--accent)' }}>
                            <i className="fas fa-robot"></i>
                        </div>
                        <div className="thinking-box">
                            <div className="dot-loader">
                                <span></span>
                                <span></span>
                                <span></span>
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                <div className="input-wrapper">
                    <textarea 
                        placeholder={isBackendOnline ? "Ask a question about your resume..." : "Backend offline - cannot send messages"}
                        rows="1"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        disabled={!isBackendOnline}
                    />
                    <button className="send-btn" onClick={handleSubmit} disabled={!isBackendOnline || !input.trim()}>
                        <i className="fas fa-paper-plane"></i>
                    </button>
                </div>
                <p className="disclaimer">
                    {isBackendOnline ? "AI-generated content. Verify important details." : "Backend connection required to send messages."}
                </p>
            </div>
        </div>
    );
};

export default ChatInterface;
