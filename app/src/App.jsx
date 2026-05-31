import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Landing from './components/Landing';
import Upload from './components/Upload';
import Result from './components/Result';
import './assets/style.css';

export default function App() {
  const [currentView, setCurrentView] = useState('landing');
  const [activeReportId, setActiveReportId] = useState(null);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('mediRiskTheme') || 'dark';
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('mediRiskTheme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

  return (
    <div className="app-viewport-wrapper">
      <Navbar currentView={currentView} onNavigate={setCurrentView} theme={theme} onToggleTheme={toggleTheme} />

      <main className="view-content-portal">
        {currentView === 'landing' && <Landing onNavigate={setCurrentView} />}
        {currentView === 'upload' && (
          <Upload 
            onUploadSuccess={(id) => {
              setActiveReportId(id);
              setCurrentView('result');
            }} 
          />
        )}
        {currentView === 'result' && (
          <Result reportId={activeReportId} onReset={() => setCurrentView('upload')} />
        )}
      </main>
    </div>
  );
}