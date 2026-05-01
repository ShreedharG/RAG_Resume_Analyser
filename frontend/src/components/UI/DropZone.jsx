import React, { useRef, useState } from 'react';
import './DropZone.css';

const DropZone = ({ title, icon, onFileSelect, accept = ".pdf" }) => {
    const fileInputRef = useRef(null);
    const [fileName, setFileName] = useState("");
    const [isDragging, setIsDragging] = useState(false);

    const handleFile = (file) => {
        if (file) {
            setFileName(file.name);
            onFileSelect(file);
        }
    };

    const onDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        handleFile(e.dataTransfer.files[0]);
    };

    return (
        <div 
            className={`drop-zone ${isDragging ? 'drag-over' : ''} ${fileName ? 'has-file' : ''}`}
            onClick={() => fileInputRef.current.click()}
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={onDrop}
        >
            <div className="drop-zone-content">
                <div className="icon-wrapper">
                    <i className={icon}></i>
                </div>
                <h3>{title}</h3>
                <p>{fileName ? `Attached: ${fileName}` : <>Drag & drop or <span>browse</span></>}</p>
                <input 
                    type="file" 
                    hidden 
                    accept={accept} 
                    ref={fileInputRef}
                    onChange={(e) => handleFile(e.target.files[0])}
                />
            </div>
            {fileName && <div className="file-preview">PDF Ready for Analysis</div>}
        </div>
    );
};

export default DropZone;
