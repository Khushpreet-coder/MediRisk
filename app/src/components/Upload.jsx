// src/components/Upload.jsx
import React, { useState } from 'react';

export default function Upload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  
  const handleInferenceSubmission = async (e) => {
    e.preventDefault();
    if (!file) return;
    

    const formData = new FormData();
    formData.append("file", file);
    setIsLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/reports/upload", {
        method: "POST",
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
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', paddingTop: '180px' }}>
      <div className="container glass-panel" style={{ width: '550px', padding: '40px', textAlign: 'center' }}>
        <h1 style={{ marginBottom: '15px' }}>Ingest Health Profiles</h1>
        <p style={{ color: '#94a3b8', marginBottom: '30px' }}>Drop a clinical matrix payload sequence down below (PDF/Image formats).</p>
        
        <form onSubmit={handleInferenceSubmission} style={{ border: '2px dashed rgba(255,255,255,0.15)', padding: '40px 20px', borderRadius: '12px' }}>
          <input 
            type="file" 
            accept="image/*,application/pdf"
            onChange={(e) => setFile(e.target.files[0])}
            disabled={isLoading}
            style={{ display: 'block', margin: '0 auto 25px auto', color: '#94a3b8' }}
          />
          <button type="submit" style={{ width: '100%' }} disabled={isLoading || !file}>
            {isLoading ? "Running Neural Parsing Pipeline..." : "Start Analysis"}
          </button>
        </form>

        {isLoading && <div className="spinner"></div>}
      </div>
    </div>
  );
}