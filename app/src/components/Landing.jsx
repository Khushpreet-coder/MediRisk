import React, { useState, useEffect } from 'react';

const healthTips = [
  { icon: '💧', title: "Stay Hydrated", tip: "Drink at least 8 glasses of water daily to maintain proper hydration and kidney function." },
  { icon: '🚶', title: "Move Daily", tip: "Walking 30 minutes a day can reduce the risk of heart disease by up to 35%." },
  { icon: '😴', title: "Sleep Well", tip: "Adults need 7-9 hours of sleep per night for optimal immune function and brain health." },
  { icon: '🥗', title: "Eat Colorful", tip: "Eat a variety of colorful fruits and vegetables to ensure a wide range of essential nutrients." },
  { icon: '🩺', title: "Stay Proactive", tip: "Regular health check-ups can detect potential issues early when they're most treatable." },
  { icon: '🧘', title: "Manage Stress", tip: "Chronic stress raises cortisol levels — try deep breathing or meditation for 5 minutes daily." },
  { icon: '💪', title: "Build Strength", tip: "Include strength training twice a week to maintain muscle mass and bone density as you age." },
  { icon: '☀️', title: "Soak the Sun", tip: "Get 15-20 minutes of morning sunlight for vitamin D production and better sleep cycles." },
];

export default function Landing({ onNavigate, user, onShowAuth }) {
  const [activeStep, setActiveStep] = useState(null);
  const [tipIndex, setTipIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setTipIndex(prev => (prev + 1) % healthTips.length);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  const steps = [
    { id: 0, title: "Upload & OCR", summary: "Uses PyTesseract and OpenCV to convert raw scans into machine-readable text with CLAHE enhancement." },
    { id: 1, title: "LLM Parsing", summary: "Analyzes structured data against guidelines to identify abnormalities and synthesize findings." },
    { id: 2, title: "RAG Retrieval", summary: "Queries our vector database to find medical reference ranges relevant to your specific markers." },
    { id: 3, title: "LLM", summary: "Analyzes structured data and RAG results to provide comprehensive insights." },
    { id: 4, title: "Summary generation", summary: "Creates concise, evidence-based summaries of key findings to facilitate rapid clinical decision-making." }
  ];

  return (
    <div style={{ width: '100%' }}>
      {/* Hero Section */}
      <section className="section-full hero-section" id="home">
        <div className="hero-split">
          <div className="hero-content">
            <h1>Healthcare AI,<br />Simplified for Modern Healthcare.</h1>
            <p>Fast, accurate, and automated medical report understanding
            powered by next-generation AI systems.</p>
            <button className="btn-primary" onClick={() => user ? onNavigate('upload') : onShowAuth()}>Get Started</button>
          </div>

          <div className="hero-card glass-panel">
            <div className="report-card-header">
              <div className="report-card-icon">🏥</div>
              <div>
                <div className="report-card-title">LABORATORY REPORT</div>
                <div className="report-card-subtitle">AI Report Analysis</div>
              </div>
            </div>
            <div className="report-card-divider" />

            <table className="report-table">
              <thead>
                <tr>
                  <th>Test Name</th>
                  <th>Result Value</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>Hemoglobin</td>
                  <td>13.2 g/dL</td>
                  <td><span className="badge badge-normal">Normal</span></td>
                </tr>
                <tr>
                  <td>WBC Count</td>
                  <td>4800 /µL</td>
                  <td><span className="badge badge-normal">Normal</span></td>
                </tr>
                <tr>
                  <td>Platelet Count</td>
                  <td>145000 /µL</td>
                  <td><span className="badge badge-low">Low</span></td>
                </tr>
                <tr>
                  <td>Blood Sugar</td>
                  <td>126 mg/dL</td>
                  <td><span className="badge badge-high">High</span></td>
                </tr>
                <tr>
                  <td>Cholesterol</td>
                  <td>198 mg/dL</td>
                  <td><span className="badge badge-normal">Normal</span></td>
                </tr>
              </tbody>
            </table>

            <div className="report-card-divider" />

            <div className="ecg-section">
              <div className="ecg-label">Live ECG Monitoring</div>
              <div className="ecg-wave">
                <svg viewBox="0 0 400 60" className="ecg-svg">
                  <polyline
                    className="ecg-line"
                    points="0,30 20,30 30,30 40,30 50,30 60,30 70,30 80,30 90,30 100,30 110,30 120,30 130,30 140,30 150,30 160,30 170,30 180,30 190,30 200,30 210,30 220,30 225,10 230,50 235,30 240,30 250,30 260,30 270,30 280,30 290,30 300,30 310,30 320,30 330,30 340,30 350,30 360,30 370,30 380,30 390,30 400,30"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features">
        <h2 style={{ textAlign: 'center', marginBottom: '80px', fontSize: '2.5rem' }}>Features</h2>

        <div className="feature-card">
          <div className="feature-img feature-svg-wrap">
            <svg viewBox="0 0 500 300" fill="none" xmlns="http://www.w3.org/2000/svg" className="feature-svg">
              <defs>
                <linearGradient id="redGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="rgba(239,68,68,0.2)" />
                  <stop offset="100%" stopColor="rgba(239,68,68,0.05)" />
                </linearGradient>
                <linearGradient id="yellowGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="rgba(234,179,8,0.2)" />
                  <stop offset="100%" stopColor="rgba(234,179,8,0.05)" />
                </linearGradient>
                <linearGradient id="greenGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="rgba(16,185,129,0.2)" />
                  <stop offset="100%" stopColor="rgba(16,185,129,0.05)" />
                </linearGradient>
                <filter id="glowRed">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                </filter>
                <filter id="glowYellow">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                </filter>
              </defs>

              <rect x="65" y="48" width="370" height="40" rx="10" fill="var(--badge-bg)" />
              <text x="85" y="74" fontSize="13" fontWeight="800" fill="var(--badge-text)" letterSpacing="1.5">REPORT ANALYSIS</text>
              <circle cx="400" cy="68" r="6" fill="rgba(16,185,129,0.5)" filter="url(#glowRed)">
                <animate attributeName="opacity" values="0.4;1;0.4" dur="2s" repeatCount="indefinite" />
              </circle>
              <circle cx="400" cy="68" r="3" fill="#10b981">
                <animate attributeName="opacity" values="0.6;1;0.6" dur="2s" repeatCount="indefinite" />
              </circle>

              <rect x="65" y="100" width="370" height="36" rx="8" fill="url(#redGrad)" stroke="#ef4444" strokeWidth="0.5" filter="url(#glowRed)">
                <animate attributeName="opacity" values="0.85;1;0.85" dur="1.5s" repeatCount="indefinite" />
              </rect>
              <rect x="78" y="108" width="8" height="20" rx="4" fill="#ef4444" />
              <text x="96" y="123" fontSize="12" fill="#ef4444" fontWeight="700">Hemoglobin — 7.2 g/dL</text>
              <rect x="330" y="108" width="95" height="20" rx="10" fill="rgba(239,68,68,0.2)" stroke="#ef4444" strokeWidth="0.5" />
              <text x="346" y="122" fontSize="9" fill="#ef4444" fontWeight="800" letterSpacing="0.5">CRITICAL</text>

              <rect x="65" y="144" width="370" height="36" rx="8" fill="url(#redGrad)" stroke="#ef4444" strokeWidth="0.5" filter="url(#glowRed)">
                <animate attributeName="opacity" values="0.85;1;0.85" dur="1.8s" repeatCount="indefinite" />
              </rect>
              <rect x="78" y="152" width="8" height="20" rx="4" fill="#ef4444" />
              <text x="96" y="167" fontSize="12" fill="#ef4444" fontWeight="700">WBC Count — 14,200 /µL</text>
              <rect x="330" y="152" width="95" height="20" rx="10" fill="rgba(239,68,68,0.2)" stroke="#ef4444" strokeWidth="0.5" />
              <text x="342" y="166" fontSize="9" fill="#ef4444" fontWeight="800" letterSpacing="0.5">ELEVATED</text>

              <rect x="65" y="188" width="370" height="36" rx="8" fill="url(#yellowGrad)" stroke="#eab308" strokeWidth="0.5" filter="url(#glowYellow)" />
              <rect x="78" y="196" width="8" height="20" rx="4" fill="#eab308" />
              <text x="96" y="211" fontSize="12" fill="#eab308" fontWeight="700">Platelet Count — 95,000 /µL</text>
              <rect x="330" y="196" width="95" height="20" rx="10" fill="rgba(234,179,8,0.2)" stroke="#eab308" strokeWidth="0.5" />
              <text x="340" y="210" fontSize="9" fill="#eab308" fontWeight="800" letterSpacing="0.5">BORDERLINE</text>

              <rect x="65" y="232" width="370" height="36" rx="8" fill="url(#greenGrad)" stroke="#10b981" strokeWidth="0.5" />
              <rect x="78" y="240" width="8" height="20" rx="4" fill="#10b981" />
              <text x="96" y="255" fontSize="12" fill="#10b981" fontWeight="700">Cholesterol — 180 mg/dL</text>
              <rect x="330" y="240" width="85" height="20" rx="10" fill="rgba(16,185,129,0.15)" stroke="#10b981" strokeWidth="0.5" />
              <text x="347" y="254" fontSize="9" fill="#10b981" fontWeight="800" letterSpacing="0.5">NORMAL</text>

              <circle cx="435" cy="35" r="16" fill="var(--bg-card)" stroke="var(--border-light)" strokeWidth="1" />
              <text x="435" y="40" fontSize="14" textAnchor="middle" fill="var(--text)" fontWeight="800">!</text>
            </svg>
          </div>
          <div className="feature-text">
            <h3>Highlight potential Issues</h3>
            <p>Automatically identifies and highlights potential issues in laboratory data that may require further investigation.</p>
          </div>
        </div>

        <div className="feature-card reverse">
          <div className="feature-img feature-svg-wrap">
            <svg viewBox="0 0 500 300" fill="none" xmlns="http://www.w3.org/2000/svg" className="feature-svg">
              <defs>
                <linearGradient id="blueGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="rgba(59,130,246,0.2)" />
                  <stop offset="100%" stopColor="rgba(59,130,246,0.05)" />
                </linearGradient>
                <linearGradient id="purpleGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="rgba(139,92,246,0.2)" />
                  <stop offset="100%" stopColor="rgba(139,92,246,0.05)" />
                </linearGradient>
              </defs>

              <circle cx="140" cy="120" r="50" fill="url(#blueGrad)" stroke="rgba(59,130,246,0.35)" strokeWidth="1" />
              <text x="140" y="126" fontSize="26" textAnchor="middle" fill="#3b82f6">📚</text>
              <text x="140" y="195" fontSize="12" textAnchor="middle" fill="var(--text-muted)" fontWeight="600">Medical</text>
              <text x="140" y="211" fontSize="12" textAnchor="middle" fill="var(--text-muted)" fontWeight="600">Textbooks</text>

              <circle cx="250" cy="90" r="50" fill="url(#purpleGrad)" stroke="rgba(139,92,246,0.35)" strokeWidth="1" />
              <text x="250" y="96" fontSize="26" textAnchor="middle" fill="#8b5cf6">🧬</text>
              <text x="250" y="165" fontSize="12" textAnchor="middle" fill="var(--text-muted)" fontWeight="600">Clinical</text>
              <text x="250" y="181" fontSize="12" textAnchor="middle" fill="var(--text-muted)" fontWeight="600">Research</text>

              <circle cx="360" cy="120" r="50" fill="url(#blueGrad)" stroke="rgba(59,130,246,0.35)" strokeWidth="1" />
              <text x="360" y="126" fontSize="26" textAnchor="middle" fill="#3b82f6">📋</text>
              <text x="360" y="195" fontSize="12" textAnchor="middle" fill="var(--text-muted)" fontWeight="600">Lab</text>
              <text x="360" y="211" fontSize="12" textAnchor="middle" fill="var(--text-muted)" fontWeight="600">Guidelines</text>

              <circle cx="250" cy="255" r="36" fill="var(--badge-bg)" stroke="var(--badge-text)" strokeWidth="0.8" />
              <text x="250" y="262" fontSize="30" textAnchor="middle" fill="var(--badge-text)">🧠</text>

              <line x1="180" y1="108" x2="210" y2="98" stroke="var(--text-muted)" strokeWidth="1.5" strokeDasharray="5 4" opacity="0.5" />
              <line x1="290" y1="98" x2="320" y2="108" stroke="var(--text-muted)" strokeWidth="1.5" strokeDasharray="5 4" opacity="0.5" />
              <line x1="250" y1="140" x2="250" y2="219" stroke="var(--text-muted)" strokeWidth="1.5" strokeDasharray="5 4" opacity="0.5" />
            </svg>
          </div>
          <div className="feature-text">
            <h3>Add Domain Knowledge</h3>
            <p>Integrates extensive medical domain knowledge to provide contextually relevant insights and improve the accuracy of the analysis.</p>
          </div>
        </div>

        <div className="feature-card">
          <div className="feature-img feature-svg-wrap">
            <svg viewBox="0 0 500 300" fill="none" xmlns="http://www.w3.org/2000/svg" className="feature-svg">
              <defs>
                <linearGradient id="cyanGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="rgba(6,182,212,0.2)" />
                  <stop offset="100%" stopColor="rgba(6,182,212,0.05)" />
                </linearGradient>
                <linearGradient id="emeraldGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="rgba(16,185,129,0.2)" />
                  <stop offset="100%" stopColor="rgba(16,185,129,0.05)" />
                </linearGradient>
                <filter id="glowCyan">
                  <feGaussianBlur stdDeviation="3" result="blur" />
                  <feMerge><feMergeNode in="blur" /><feMergeNode in="SourceGraphic" /></feMerge>
                </filter>
              </defs>

              <rect x="50" y="30" width="175" height="240" rx="14" fill="var(--bg-card)" stroke="var(--border-light)" strokeWidth="1" />
              <rect x="65" y="48" width="145" height="6" rx="3" fill="var(--text-muted)" opacity="0.25" />
              <rect x="65" y="62" width="100" height="4" rx="2" fill="var(--text-muted)" opacity="0.15" />

              <rect x="65" y="85" width="145" height="22" rx="6" fill="rgba(239,68,68,0.1)" />
              <text x="73" y="100" fontSize="10" fill="#ef4444" fontWeight="600">▌Hemoglobin · Low</text>

              <rect x="65" y="115" width="145" height="22" rx="6" fill="rgba(234,179,8,0.1)" />
              <text x="73" y="130" fontSize="10" fill="#eab308" fontWeight="600">▌Platelets · Borderline</text>

              <rect x="65" y="145" width="145" height="22" rx="6" fill="rgba(16,185,129,0.1)" />
              <text x="73" y="160" fontSize="10" fill="#10b981" fontWeight="600">▌Cholesterol · Normal</text>

              <rect x="65" y="175" width="145" height="22" rx="6" fill="rgba(239,68,68,0.1)" />
              <text x="73" y="190" fontSize="10" fill="#ef4444" fontWeight="600">▌WBC · Elevated</text>

              <rect x="65" y="205" width="145" height="22" rx="6" fill="rgba(16,185,129,0.1)" />
              <text x="73" y="220" fontSize="10" fill="#10b981" fontWeight="600">▌Creatinine · Normal</text>

              <rect x="65" y="240" width="145" height="20" rx="6" fill="var(--badge-bg)" />
              <text x="137" y="254" fontSize="10" textAnchor="middle" fill="var(--badge-text)" fontWeight="700">+ 3 more</text>

              <line x1="245" y1="40" x2="245" y2="270" stroke="var(--border-light)" strokeWidth="1.5" strokeDasharray="6 5" />

              <rect x="275" y="40" width="185" height="44" rx="10" fill="url(#cyanGrad)" stroke="rgba(6,182,212,0.3)" strokeWidth="0.8" filter="url(#glowCyan)" />
              <text x="290" y="58" fontSize="11" fill="#06b6d4" fontWeight="800" letterSpacing="0.5">AI SUMMARY</text>
              <text x="290" y="73" fontSize="9" fill="var(--text-muted)">Generated by LLaMA 3 · 70B</text>

              <rect x="275" y="96" width="185" height="40" rx="8" fill="var(--bg-card)" stroke="var(--border)" strokeWidth="0.5" />
              <circle cx="292" cy="116" r="4" fill="#ef4444">
                <animate attributeName="opacity" values="0.4;1;0.4" dur="1.5s" repeatCount="indefinite" />
              </circle>
              <text x="304" y="112" fontSize="9.5" fill="var(--text)" fontWeight="600">2 critical flags detected</text>
              <text x="304" y="126" fontSize="9" fill="var(--text-muted)">Immediate attention required</text>

              <rect x="275" y="146" width="185" height="40" rx="8" fill="var(--bg-card)" stroke="var(--border)" strokeWidth="0.5" />
              <circle cx="292" cy="166" r="4" fill="#eab308" />
              <text x="304" y="162" fontSize="9.5" fill="var(--text)" fontWeight="600">1 borderline result</text>
              <text x="304" y="176" fontSize="9" fill="var(--text-muted)">Follow-up recommended</text>

              <rect x="275" y="196" width="185" height="40" rx="8" fill="var(--bg-card)" stroke="var(--border)" strokeWidth="0.5" />
              <circle cx="292" cy="216" r="4" fill="#10b981" />
              <text x="304" y="212" fontSize="9.5" fill="var(--text)" fontWeight="600">2 normal results</text>
              <text x="304" y="226" fontSize="9" fill="var(--text-muted)">Within reference range</text>

              <rect x="275" y="253" width="185" height="28" rx="8" fill="url(#emeraldGrad)" stroke="rgba(16,185,129,0.3)" strokeWidth="0.8" />
              <text x="367" y="272" fontSize="11" textAnchor="middle" fill="#10b981" fontWeight="800" letterSpacing="0.5">DOWNLOAD REPORT</text>
            </svg>
          </div>
          <div className="feature-text">
            <h3>Summarize Findings</h3>
            <p>Provides concise, evidence-based summaries of key findings to facilitate rapid clinical decision-making.</p>
          </div>
        </div>
      </section>

      {/* Health Tips Section */}
      <section className="health-tips-section" id="health-tips">
        <div className="health-tips-header">
          <span className="health-tips-badge">Daily Wellness</span>
          <h2>Health Tips for You</h2>
          <p>Simple daily habits for a healthier life</p>
        </div>
        <div className="health-tip-card glass-panel">
          <div className="health-tip-glow" />
          <div className="health-tip-inner">
            <span className="health-tip-icon">{healthTips[tipIndex].icon}</span>
            <div className="health-tip-content">
              <span className="health-tip-label">{healthTips[tipIndex].title}</span>
              <p className="health-tip-text">{healthTips[tipIndex].tip}</p>
            </div>
          </div>
          <div className="health-tip-footer">
            <div className="health-tip-dots">
              {healthTips.map((_, i) => (
                <button key={i} className={`health-tip-dot ${i === tipIndex ? 'active' : ''}`} onClick={() => setTipIndex(i)} aria-label={`Tip ${i + 1}`} />
              ))}
            </div>

          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works">
        <h2>How It Works</h2>
        <p>From upload to insight — our AI pipeline in five simple steps.</p>
        <div className="pipeline-container">
          {steps.map((step, idx) => (
            <React.Fragment key={step.id}>
              <div
                className={`step-card ${activeStep === step.id ? 'active' : ''}`}
                onClick={() => setActiveStep(activeStep === step.id ? null : step.id)}
              >
                <div className="step-number">{String(step.id + 1).padStart(2, '0')}</div>
                <h4>{step.title}</h4>
                <div className="step-summary">{step.summary}</div>
              </div>
              {idx < steps.length - 1 && <span className="step-arrow">→</span>}
            </React.Fragment>
          ))}
        </div>
      </section>
    </div>
  );
}