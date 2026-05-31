import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Landing from './components/Landing';
import Upload from './components/Upload';
import Result from './components/Result';
import MyReports from './components/MyReports';
import Chat from './components/Chat';
import AuthModal from './components/AuthModal';
import './assets/style.css';

export default function App() {
  const [currentView, setCurrentView] = useState('landing');
  const [activeReportId, setActiveReportId] = useState(null);
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('mediRiskTheme') || 'dark';
  });
  const [user, setUser] = useState(() => {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    return token && username ? { token, username } : null;
  });
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState('login');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('mediRiskTheme', theme);
  }, [theme]);

  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

  const handleLoginSuccess = ({ username, token }) => {
    setUser({ username, token });
  };

  const openAuth = (mode) => { setAuthMode(mode); setShowAuth(true); };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setUser(null);
  };

  return (
    <div className="app-viewport-wrapper">
      <Navbar currentView={currentView} onNavigate={setCurrentView} theme={theme} onToggleTheme={toggleTheme} user={user} onShowAuth={() => openAuth('login')} onShowRegister={() => openAuth('register')} onLogout={handleLogout} />
      {showAuth && <AuthModal onClose={() => setShowAuth(false)} onLoginSuccess={handleLoginSuccess} initialMode={authMode} />}

      <main className="view-content-portal">
        {currentView === 'landing' && <Landing onNavigate={setCurrentView} user={user} onShowAuth={() => openAuth('login')} />}
        {currentView === 'upload' && (
          <Upload 
            onUploadSuccess={(id) => {
              setActiveReportId(id);
              setCurrentView('result');
            }} 
          />
        )}
        {currentView === 'result' && (
          <Result reportId={activeReportId} onReset={() => setCurrentView('upload')} onBack={() => setCurrentView('my-reports')} onChat={(id) => { setActiveReportId(id); setCurrentView('chat'); }} />
        )}
        {currentView === 'my-reports' && (
          <MyReports 
            onViewReport={(id) => { setActiveReportId(id); setCurrentView('result'); }}
            onNewUpload={() => setCurrentView('upload')}
          />
        )}
        {currentView === 'chat' && (
          <Chat reportId={activeReportId} onBack={() => activeReportId ? setCurrentView('result') : setCurrentView('landing')} />
        )}
      </main>
    </div>
  );
}