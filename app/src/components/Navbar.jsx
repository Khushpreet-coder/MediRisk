import React, { useState } from 'react';

export default function Navbar({ currentView, onNavigate, theme, onToggleTheme, user, onShowAuth, onShowRegister, onLogout }) {
  const [menuOpen, setMenuOpen] = useState(false);
  const [dropdownOpen, setDropdownOpen] = useState(false);

  const handleNavClick = (e, sectionId) => {
    e.preventDefault();
    setMenuOpen(false);
    const scrollToSection = () => {
      const el = document.getElementById(sectionId);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    };
    if (currentView !== 'landing') {
      onNavigate('landing');
      setTimeout(scrollToSection, 100);
    } else {
      scrollToSection();
    }
  };

  const navLinks = [
    { name: "Home", sectionId: "home" },
    { name: "how it works", sectionId: "how-it-works" },
    { name: "Features", sectionId: "features" },
  ];

  return (
    <>
      <header className="navbar">
        <div className="logo">🩺 MediRisk Analyzer</div>
        
        <nav className="nav-desktop">
          {navLinks.map((link, index) => (
            <a key={index} href={`#${link.sectionId}`} className="nav-link" onClick={(e) => handleNavClick(e, link.sectionId)}>
              {link.name}
            </a>
          ))}
          <button className="theme-toggle" onClick={onToggleTheme} aria-label="Toggle theme">
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
          {user ? (
            <div className="nav-user" onClick={() => setDropdownOpen(!dropdownOpen)} onBlur={() => setTimeout(() => setDropdownOpen(false), 150)} tabIndex="0">
              <span className="nav-avatar">{user.username.charAt(0).toUpperCase()}</span>
              {dropdownOpen && (
                <div className="nav-dropdown">
                  <button className="nav-dropdown-item" onClick={(e) => { e.stopPropagation(); setDropdownOpen(false); onNavigate('my-reports'); }}>My Reports</button>
                    <button className="nav-dropdown-item" onClick={(e) => { e.stopPropagation(); setDropdownOpen(false); onNavigate('chat'); }}>Ask AI</button>
                    <button className="nav-dropdown-logout" onClick={(e) => { e.stopPropagation(); onLogout(); }}>Sign Out</button>
                </div>
              )}
            </div>
          ) : (
            <>
              <button className="nav-auth-btn nav-auth-reg" onClick={onShowRegister}>Register</button>
              <button className="nav-auth-btn" onClick={onShowAuth}>Sign In</button>
            </>
          )}
        </nav>

        <div className="nav-mobile-controls">
          <button className="theme-toggle" onClick={onToggleTheme} aria-label="Toggle theme">
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
          <button className="hamburger" onClick={() => setMenuOpen(true)} aria-label="Open menu">
            <span></span>
            <span></span>
            <span></span>
          </button>
        </div>
      </header>

      {menuOpen && <div className="sidebar-overlay" onClick={() => setMenuOpen(false)} />}

      <aside className={`sidebar ${menuOpen ? 'sidebar-open' : ''}`}>
        <div className="sidebar-header">
          <span className="logo">🩺 MediRisk Analyzer</span>
          <button className="sidebar-close" onClick={() => setMenuOpen(false)}>✕</button>
        </div>
        <nav className="sidebar-nav">
          {navLinks.map((link, index) => (
            <a key={index} href={`#${link.sectionId}`} className="sidebar-link" onClick={(e) => handleNavClick(e, link.sectionId)}>
              {link.name}
            </a>
          ))}
          {user && (
            <button className="sidebar-link" onClick={() => { setMenuOpen(false); onNavigate('my-reports'); }}>
              My Reports
            </button>
          )}
          {user && (
            <button className="sidebar-link" onClick={() => { setMenuOpen(false); onNavigate('chat'); }}>
              Ask AI
            </button>
          )}
        </nav>
        <div className="sidebar-auth">
          {user ? (
            <div className="sidebar-user">
              <span className="nav-avatar">{user.username.charAt(0).toUpperCase()}</span>
              <span>{user.username}</span>
              <button className="sidebar-logout" onClick={() => { setMenuOpen(false); onLogout(); }}>Sign Out</button>
            </div>
          ) : (
            <div className="sidebar-auth-btns">
              <button className="sidebar-link sidebar-signin" onClick={() => { setMenuOpen(false); onShowRegister(); }}>Register</button>
              <button className="sidebar-link sidebar-signin" onClick={() => { setMenuOpen(false); onShowAuth(); }}>Sign In</button>
            </div>
          )}
        </div>
      </aside>
    </>
  );
}