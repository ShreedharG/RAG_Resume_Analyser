import React from 'react';
import './Sidebar.css';

const Sidebar = ({ history, activeSession, onNewChat, onSelectSession }) => {
    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <div className="logo">
                    <i className="fas fa-brain-circuit"></i>
                    <span>Resume Intel</span>
                </div>
                <button className="new-chat-btn" onClick={onNewChat}>
                    <i className="fas fa-plus"></i>
                    <span>New Chat</span>
                </button>
            </div>
            
            <div className="history-section">
                <p className="section-title">Recent Analysis</p>
                <div className="chat-history">
                    {history.length === 0 ? (
                        <p className="empty-history">No past sessions</p>
                    ) : (
                        history.map((item) => (
                            <div 
                                key={item.id} 
                                className={`history-item ${activeSession === item.id ? 'active' : ''}`}
                                onClick={() => onSelectSession(item.id)}
                            >
                                <i className="fas fa-message"></i>
                                <span>{item.title}</span>
                            </div>
                        ))
                    )}
                </div>
            </div>

            <div className="sidebar-footer">
                <div className="user-profile">
                    <div className="avatar">S</div>
                    <div className="user-info">
                        <span className="username">Shreedhar G</span>
                        <span className="plan">Premium Plan</span>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
