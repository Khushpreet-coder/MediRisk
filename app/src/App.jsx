// src/App.jsx
import React, { useState } from 'react';
import Navbar from './components/Navbar'; // <-- Import your new component
import Landing from './components/Landing';
import Upload from './components/Upload';
import Result from './components/Result';
import './assets/style.css';

export default function App() {
  const [currentView, setCurrentView] = useState('landing');
  const [activeReportId, setActiveReportId] = useState(null);

  return (
    <div className="app-viewport-wrapper">
      {/* Clean, state-aware Navbar component insertion */}
      <Navbar currentView={currentView} onNavigate={setCurrentView} />

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