import React, { useState } from 'react';
import DropZone from '../UI/DropZone';
import './Dashboard.css';

const Dashboard = ({ onStartAnalysis }) => {
    const [files, setFiles] = useState({ resume: null, jd: null });
    const [isLoading, setIsLoading] = useState(false);

    const handleFileSelect = (key, file) => {
        setFiles(prev => ({ ...prev, [key]: file }));
    };

    const handleStart = async () => {
        setIsLoading(true);
        await onStartAnalysis(files);
        setIsLoading(false);
    };

    const isReady = files.resume && files.jd;

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
                    disabled={!isReady || isLoading}
                    onClick={handleStart}
                >
                    {isLoading ? (
                        <><i className="fas fa-spinner fa-spin"></i> Initializing RAG...</>
                    ) : (
                        'Initialize RAG Analysis'
                    )}
                </button>
            </div>
        </div>
    );
};

export default Dashboard;
