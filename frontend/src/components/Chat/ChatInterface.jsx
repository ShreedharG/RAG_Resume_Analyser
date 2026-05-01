import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';

const ChatInterface = ({ messages, onSendMessage }) => {
    const [input, setInput] = useState("");
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(scrollToBottom, [messages]);

    const handleSubmit = (e) => {
        if (e) e.preventDefault();
        if (input.trim()) {
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
                            <div className="message-bubble">{msg.content}</div>
                        </div>
                    ))
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                <div className="input-wrapper">
                    <textarea 
                        placeholder="Ask a question about your resume..." 
                        rows="1"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                    />
                    <button className="send-btn" onClick={handleSubmit}>
                        <i className="fas fa-paper-plane"></i>
                    </button>
                </div>
                <p className="disclaimer">AI-generated content. Verify important details.</p>
            </div>
        </div>
    );
};

export default ChatInterface;
