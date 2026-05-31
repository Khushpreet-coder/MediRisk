import React, { useState, useRef } from 'react';

export default function Upload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef(null);

  const handleIconClick = () => {
    fileInputRef.current?.click();
  };
  
  const handleInferenceSubmission = async (e) => {
    e.preventDefault();
    if (!file) return;
    

    const formData = new FormData();
    formData.append("file", file);
    setIsLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch("/api/reports/upload", {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: formData,
      });

      const payload = await response.json();
      const reportId = payload.report_id || (payload.data && payload.data.report_id);

      if (reportId) {
        onUploadSuccess(reportId);
      } else {
        alert("Verification rejection: Missing structural ID metadata keys.");
        setIsLoading(false);
      }
    } catch (err) {
      console.error(err);
      alert("Network disruption mapping pipeline. Ensure API instance lifecycle is online.");
      setIsLoading(false);
    }
  };

  return (
    <div className="upload-wrapper">
      <div className="upload-card glass-panel">
        <h1 style={{ marginBottom: '28px' }}>Ingest Health Profiles</h1>
        
        <form onSubmit={handleInferenceSubmission}>
          <div className="upload-dropzone">
            <input 
              type="file" 
              accept="image/*,application/pdf"
              onChange={(e) => setFile(e.target.files[0])}
              disabled={isLoading}
              className="upload-input"
              id="file-input"
              ref={fileInputRef}
            />
            <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '6px' }}>Drag & drop or click to upload your medical report</p>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.78rem', marginBottom: '20px' }}>Supports PDF, PNG, JPG — up to 50MB</p>
            <div className="upload-icon-container" onClick={handleIconClick} style={{ cursor: 'pointer' }}>
              <svg viewBox="0 0 48 48" fill="none" className="upload-icon-svg" xmlns="http://www.w3.org/2000/svg">
                <rect x="10" y="28" width="28" height="14" rx="4" stroke="currentColor" strokeWidth="2" fill="none" />
                <path d="M24 8 L24 30 M16 18 L24 8 L32 18" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
              </svg>
            </div>
            <label htmlFor="file-input" className="upload-label" style={{ cursor: 'pointer' }}>
              {file ? file.name : "Choose File"}
            </label>
          </div>

          <button type="submit" className="btn-primary upload-submit" disabled={isLoading || !file} style={{ marginTop: '20px' }}>
            {isLoading ? "Running Neural Parsing Pipeline..." : "Start Analysis"}
          </button>
        </form>

        {isLoading && <div className="spinner"></div>}
      </div>
    </div>
  );
}