import './Sidebar.css';

const Sidebar = ({ history, activeSession, onNewChat, onSelectSession, onDeleteSession }) => {
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
                        history.map((item) => {
                            const date = new Date(item.created_at);
                            const formattedDate = date.toLocaleDateString(undefined, { month: 'short', day: 'numeric' });
                            const formattedTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

                            return (
                                <div 
                                    key={item.id} 
                                    className={`history-item ${activeSession === item.id ? 'active' : ''}`}
                                    onClick={() => onSelectSession(item.id)}
                                >
                                    <div className="history-icon">
                                        <i className="fas fa-file-pdf"></i>
                                    </div>
                                    <div className="history-content">
                                        <div className="history-filenames">
                                            <span className="resume-name">{item.resume_name || "Untitled"}</span>
                                            <span className="vs-label">vs</span>
                                            <span className="jd-name">{item.jd_name || "JD"}</span>
                                        </div>
                                        <div className="history-meta">
                                            <span>{formattedDate}</span>
                                            <span className="separator">•</span>
                                            <span>{formattedTime}</span>
                                        </div>
                                    </div>
                                    <button 
                                        className="delete-btn"
                                        title="Delete session"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            onDeleteSession(item.id);
                                        }}
                                    >
                                        <i className="fas fa-trash-can"></i>
                                    </button>
                                </div>
                            );
                        })
                    )}
                </div>
            </div>

            <div className="sidebar-footer">
                <div className="user-profile">
                    <div className="avatar">S</div>
                    <div className="user-info">
                        <span className="username">Shreedhar G</span>
                    </div>
                </div>
            </div>
        </aside>
    );
};

export default Sidebar;
