import React, { useState, useRef, useEffect } from 'react';

export default function Chat({ reportId, onBack }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [reportInfo, setReportInfo] = useState(null);
  const chatEnd = useRef(null);

  useEffect(() => {
    if (reportId) {
      const token = localStorage.getItem('token');
      fetch(`/api/reports/report/${reportId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
        .then(r => r.json())
        .then(data => {
          if (data.status === 'success') {
            setReportInfo({ id: data.report_id, filename: data.filename });
          }
        })
        .catch(() => {});
    }
  }, [reportId]);

  useEffect(() => {
    chatEnd.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;
    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setLoading(true);

    const token = localStorage.getItem('token');
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message: userMsg, report_id: reportId || null })
      });
      const data = await res.json();
      setMessages(prev => [...prev, { role: 'ai', text: data.response || 'No response' }]);
    } catch {
      setMessages(prev => [...prev, { role: 'ai', text: 'Sorry, something went wrong.' }]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="dashboard-layout chat-container">
      <header className="result-header">
        <h1>{reportInfo ? 'Ask About Report' : 'Medical Chat'}</h1>
        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          {reportInfo && <span className="chat-report-badge">{reportInfo.filename}</span>}
          {onBack && <button className="btn-secondary" onClick={onBack}>Back</button>}
        </div>
      </header>

      {!reportId && messages.length === 0 && (
        <div className="chat-welcome">
          <p>Ask me any medical question. I can help explain lab results, medical terms, and general health topics.</p>
        </div>
      )}

      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`chat-msg ${m.role === 'user' ? 'chat-msg-user' : 'chat-msg-ai'}`}>
            <div className="chat-msg-bubble">{m.text}</div>
          </div>
        ))}
        {loading && (
          <div className="chat-msg chat-msg-ai">
            <div className="chat-msg-bubble"><span className="chat-typing">Thinking</span></div>
          </div>
        )}
        <div ref={chatEnd} />
      </div>

      <div className="chat-input-bar">
        <textarea
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type your question..."
          rows={1}
        />
        <button className="btn-primary chat-send" onClick={sendMessage} disabled={loading || !input.trim()}>Send</button>
      </div>
    </div>
  );
}
