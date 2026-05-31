import React, { useState } from 'react';

export default function Navbar({ currentView, onNavigate, theme, onToggleTheme }) {
  const [menuOpen, setMenuOpen] = useState(false);

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
        </nav>
      </aside>
    </>
  );
}