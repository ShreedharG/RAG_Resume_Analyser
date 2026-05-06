import React from 'react';
import './LandingPage.css';

const LandingPage = ({ onEnterApp }) => {
    return (
        <div className="landing-container" onClick={onEnterApp}>
            <div className="background-glow"></div>
            <div className="floating-elements">
                <div className="float-item circle-1"></div>
                <div className="float-item circle-2"></div>
                <div className="float-item circle-3"></div>
            </div>
            
            <nav className="landing-nav">
                <div className="logo">
                    <i className="fas fa-brain"></i>
                    <span>Resume Intel</span>
                </div>
            </nav>

            <main className="hero-section">
                <div className="hero-content">
                    <div className="badge">AI-Powered Analysis</div>
                    <h1>Bridge the Gap Between <span className="gradient-text">You</span> and Your <span className="gradient-text">Dream Job</span></h1>
                    <p>
                        Upload your resume and a job description. Our advanced RAG pipeline 
                        identifies matching skills, missing keywords, and gives you actionable expert insights.
                    </p>
                    
                    <div className="cta-wrapper">
                        <button className="glow-button">
                            Get Started Free
                            <i className="fas fa-arrow-right"></i>
                        </button>
                        <span className="cta-hint">Click anywhere to begin your journey</span>
                    </div>
                </div>

                <div className="hero-visual">
                    <div className="visual-card">
                        <div className="card-mock-row"></div>
                        <div className="card-mock-row short"></div>
                        <div className="card-mock-row"></div>
                        <div className="card-mock-pills">
                            <div className="pill green">Matched</div>
                            <div className="pill yellow">Missing</div>
                        </div>
                    </div>
                </div>
            </main>

            <footer className="landing-footer">
                <div className="stats">
                    <div className="stat-item">
                        <span className="val">100%</span>
                        <span className="lbl">Local Processing</span>
                    </div>
                    <div className="stat-item">
                        <span className="val">Instant</span>
                        <span className="lbl">Skill Matching</span>
                    </div>
                    <div className="stat-item">
                        <span className="val">Advanced</span>
                        <span className="lbl">RAG Pipeline</span>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
