import React, { useState, useEffect } from 'react';

export default function MyReports({ onViewReport, onNewUpload }) {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchReports = async () => {
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('/api/reports/my-reports', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (data.status === 'success') {
        setReports(data.reports);
      } else {
        setError('Failed to load reports');
      }
    } catch {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchReports(); }, []);

  const handleClearAll = async () => {
    if (!confirm('Delete all reports?')) return;
    const token = localStorage.getItem('token');
    try {
      const res = await fetch('/api/reports/my-reports', {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (data.status === 'success') {
        setReports([]);
      }
    } catch {
      setError('Failed to clear reports');
    }
  };

  const handleDelete = async (e, reportId) => {
    e.stopPropagation();
    if (!confirm('Delete this report?')) return;
    const token = localStorage.getItem('token');
    try {
      const res = await fetch(`/api/reports/report/${reportId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await res.json();
      if (data.status === 'success') {
        setReports(prev => prev.filter(r => r.report_id !== reportId));
      }
    } catch {
      setError('Failed to delete');
    }
  };

  if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

  return (
    <div className="dashboard-layout my-reports-container">
      <header className="result-header">
        <h1>My Reports</h1>
        <div style={{ display: 'flex', gap: '10px' }}>
          {reports.length > 0 && <button className="btn-secondary btn-clear-all" onClick={handleClearAll}>Clear All</button>}
          <button className="btn-primary" onClick={onNewUpload}>New Analysis</button>
        </div>
      </header>

      {error && <p className="auth-error">{error}</p>}

      {reports.length === 0 ? (
        <div className="glass-panel" style={{ textAlign: 'center', padding: '40px' }}>
          <p style={{ color: 'var(--text-muted)', fontSize: '1.1rem' }}>No reports yet</p>
          <button className="btn-primary" onClick={onNewUpload} style={{ marginTop: '16px' }}>Upload your first report</button>
        </div>
      ) : (
        <div className="reports-list">
          {reports.map((r) => (
            <div key={r.report_id} className="glass-panel report-card" onClick={() => onViewReport(r.report_id)}>
              <div className="report-card-info">
                <span className="report-card-name">{r.filename}</span>
                <span className="report-card-date">{r.created_at ? r.created_at.slice(0, 10) : ''}</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                <span className={`status-badge ${r.status === 'completed' ? 'badge-normal' : 'badge-abnormal'}`}>{r.status}</span>
                <button className="report-delete-btn" onClick={(e) => handleDelete(e, r.report_id)} title="Delete">✕</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
