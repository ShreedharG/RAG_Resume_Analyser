import React from 'react';
import './AnalysisResult.css';

const AnalysisResult = ({ data }) => {
    // If data is a string, try to parse it
    let parsedData = data;
    if (typeof data === 'string') {
        try {
            // Clean the string if it contains markdown code blocks
            const cleanJson = data.replace(/```json\n?|```/g, '').trim();
            parsedData = JSON.parse(cleanJson);
        } catch (e) {
            return <pre className="json-response">{data}</pre>;
        }
    }

    const matching = parsedData.matching_skills || parsedData.matching;
    const missing = parsedData.missing_skills || parsedData.missing;
    const reason = parsedData.reason;

    const showMatching = matching !== undefined;
    const showMissing = missing !== undefined;

    return (
        <div className="analysis-result">
            {(showMatching || showMissing) && (
                <div className="result-grid">
                    {showMatching && (
                        <div className="result-card matched">
                            <div className="card-header">
                                <i className="fas fa-check-circle"></i>
                                <span>Matched Skills</span>
                            </div>
                            <div className="skills-list">
                                {Array.isArray(matching) && matching.length > 0 && matching[0] !== "" ? (
                                    matching.map((skill, i) => (
                                        skill && <span key={i} className="skill-pill match">{skill}</span>
                                    ))
                                ) : (
                                    <span className="no-data">No specific matches found</span>
                                )}
                            </div>
                        </div>
                    )}

                    {showMissing && (
                        <div className="result-card missing">
                            <div className="card-header">
                                <i className="fas fa-exclamation-circle"></i>
                                <span>Missing Skills</span>
                            </div>
                            <div className="skills-list">
                                {Array.isArray(missing) && missing.length > 0 && missing[0] !== "" ? (
                                    missing.map((skill, i) => (
                                        skill && <span key={i} className="skill-pill miss">{skill}</span>
                                    ))
                                ) : (
                                    <span className="no-data">No missing critical skills</span>
                                )}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {reason !== undefined && (
                <div className="result-card reason">
                    <div className="card-header">
                        <i className="fas fa-lightbulb"></i>
                        <span>Expert Analysis</span>
                    </div>
                    <p className="reason-text">{reason || "No detailed analysis provided."}</p>
                </div>
            )}
        </div>
    );
};

export default AnalysisResult;
