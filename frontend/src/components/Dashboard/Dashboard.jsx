import React, { useState } from 'react';
import DropZone from '../UI/DropZone';
import './Dashboard.css';

const Dashboard = ({ onStartAnalysis, backendStatus }) => {
    const [files, setFiles] = useState({ resume: null, jd: null });
    const [isLoading, setIsLoading] = useState(false);

    const handleFileSelect = (key, file) => {
        setFiles(prev => ({ ...prev, [key]: file }));
    };

    const handleStart = async () => {
        if (!isReady || isLoading) return;
        
        setIsLoading(true);
        try {
            await onStartAnalysis(files);
        } catch (error) {
            console.error("Analysis failed:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const isReady = files.resume && files.jd;
    const isBackendOnline = backendStatus === 'online';

    return (
        <div className="dashboard">
            <header className="dashboard-header">
                <h1>Analyze Your Fit</h1>
                <p>Upload your resume and the job description to get deep insights.</p>
            </header>
            
            <div className="drop-zones-grid">
                <DropZone 
                    title="Resume" 
                    icon="fas fa-file-pdf" 
                    onFileSelect={(file) => handleFileSelect('resume', file)}
                />
                <DropZone 
                    title="Job Description" 
                    icon="fas fa-briefcase" 
                    onFileSelect={(file) => handleFileSelect('jd', file)}
                />
            </div>
            
            <div className="actions">
                <button 
                    className="primary-btn" 
                    disabled={!isReady || isLoading || !isBackendOnline}
                    onClick={handleStart}
                >
                    {isLoading ? (
                        <><i className="fas fa-spinner fa-spin"></i> Initializing RAG...</>
                    ) : !isBackendOnline ? (
                        <><i className="fas fa-exclamation-triangle"></i> Backend Offline</>
                    ) : (
                        'Initialize RAG Analysis'
                    )}
                </button>
                {!isBackendOnline && (
                    <p style={{ color: 'var(--error)', fontSize: '0.85rem', marginTop: '0.5rem' }}>
                        Please ensure the backend server is running on port 8000
                    </p>
                )}
            </div>
        </div>
    );
};

export default Dashboard;
