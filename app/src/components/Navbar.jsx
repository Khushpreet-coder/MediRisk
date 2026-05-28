// // src/components/Navbar.jsx
// import React from 'react';

// export default function Navbar({ currentView, onNavigate }) {
//   return (
//     <header className="navbar glass-panel">
//       {/* Clicking the logo routes the user back to the primary landing frame */}
//       <div className="logo" onClick={() => onNavigate('landing')}>
//         🩺 MediRisk Analyzer
//       </div>
      
//       <nav style={{ display: 'flex', alignItems: 'center' }}>
//         <button 
//           onClick={() => onNavigate('landing')}
//           style={{ 
//             color: currentView === 'landing' ? '#3b82f6' : '#94a3b8',
//             borderBottom: currentView === 'landing' ? '2px solid #3b82f6' : 'none',
//             borderRadius: '0',
//             padding: '4px 0',
//             margin: '0 15px'
//           }}
//         >
//           Home
//         </button>
        
//         <button 
//           onClick={() => onNavigate('upload')}
//           style={{ 
//             color: currentView === 'upload' || currentView === 'result' ? '#3b82f6' : '#94a3b8',
//             borderBottom: currentView === 'upload' || currentView === 'result' ? '2px solid #3b82f6' : 'none',
//             borderRadius: '0',
//             padding: '4px 0',
//             margin: '0 15px'
//           }}
//         >
//           Analysis Console
//         </button>
//       </nav>

//       {/* Action button forces direct routing to the ingestion interface */}
//       <button 
//         className="btn" 
//         onClick={() => onNavigate('upload')}
//         style={{ padding: '10px 20px', fontSize: '14px' }}
//       >
//         Get Started
//       </button>
//     </header>
//   );
// }

// export default function Navbar({ onNavigate }) {
//   return (
//     <header style={{ 
//       display: 'flex', justifyContent: 'space-between', padding: '20px 5%', 
//       alignItems: 'center', borderBottom: '1px solid #1e293b' 
//     }}>
//       <div style={{ fontSize: '20px', fontWeight: 'bold' }}>🩺 MediRisk Analyzer</div>
//       <nav style={{ display: 'flex', gap: '20px' }}>
//         <a href="#home" className="nav-link">Home</a>
//         <a href="#features" className="nav-link">Features</a>
//         <a href="#" className="nav-link">How it works</a>
//       </nav>
//       {/* Removed Get Started Button */}
//     </header>
//   );
// }

import React from 'react';

export default function Navbar({ onNavigate }) {
  // Define links here for easy management
  const navLinks = [
    { name: "Home", href: "#home" },
    { name: "how it works", href: "#how-it-works" },
    { name: "Features", href: "#features" },
    
  ];

  return (
    <header className="navbar">
      <div className="logo">🩺 MediRisk Analyzer</div>
      
      <nav style={{ display: 'flex', gap: '5px' }}>
        {navLinks.map((link, index) => (
          link.action ? (
            // Render as button if it has a click action (like Upload)
            <button key={index} onClick={link.action} className="nav-link">
              {link.name}
            </button>
          ) : (
            // Render as standard link for scrolling
            <a key={index} href={link.href} className="nav-link">
              {link.name}
            </a>
          )
        ))}
      </nav>
    </header>
  );
}