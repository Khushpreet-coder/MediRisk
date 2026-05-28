// import React from 'react';

// export default function Landing({ onNavigate }) {
//   const steps = [
//     { title: "Secure Upload & OCR", desc: "Digital ingestion and high-precision extraction." },
//     { title: "RAG Context Retrieval", desc: "Cross-referencing biomarkers with medical indices." },
//     { title: "Llama-3 Synthesis", desc: "Generating a compassionate, personalized summary." }
//   ];

//   return (
//     <div style={{ padding: '80px 10%', color: '#f8fafc', maxWidth: '1000px', margin: '0 auto' }}>
      
//       {/* Hero */}
//       <section style={{ marginBottom: '100px' }}>
//         <h1 style={{ fontSize: '48px', fontWeight: '700', marginBottom: '20px' }}>AI-Powered Clinical Analysis</h1>
//         <p style={{ color: '#94a3b8', fontSize: '18px', marginBottom: '30px' }}>Your medical reports, simplified by AI.</p>
//         <button className="btn" onClick={() => onNavigate('upload')}>Upload Laboratory Report</button>
//       </section>

      

//       {/* Engine Core Features (Simplified) */}
//       <section>
//         <h2 style={{ marginBottom: '30px' }}>Engine Core Components</h2>
//         <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
//           {['Native Parser', 'RAG Verification', 'Anomaly Flagging'].map((feat, i) => (
//             <div key={i} className="glass-panel" style={{ padding: '20px', borderRadius: '12px', textAlign: 'center' }}>
//               <h4 style={{ margin: '0 0 10px 0' }}>{feat}</h4>
//             </div>
//           ))}
//         </div>
//       </section>

//       {/* Ladder / Timeline How It Works */}
//       <section style={{ marginBottom: '100px' }}>
//         <h2 style={{ marginBottom: '50px', textAlign: 'center' }}>How It Works</h2>
//         <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', position: 'relative' }}>
//           {/* The Vertical Line */}
//           <div style={{ position: 'absolute', left: '24px', top: '0', bottom: '0', width: '2px', background: '#334155' }}></div>
          
//           {steps.map((step, i) => (
//             <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '30px', zIndex: 1 }}>
//               <div style={{ width: '50px', height: '50px', borderRadius: '50%', background: '#3b82f6', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold' }}>{i + 1}</div>
//               <div className="glass-panel" style={{ padding: '20px', flex: 1, borderRadius: '12px' }}>
//                 <h3 style={{ margin: '0 0 5px 0' }}>{step.title}</h3>
//                 <p style={{ margin: 0, color: '#94a3b8', fontSize: '14px' }}>{step.desc}</p>
//               </div>
//             </div>
//           ))}
//         </div>
//       </section>
//     </div>
//   );
// }

// import React from 'react';
// import React, { useState } from 'react';

// export default function Landing({ onNavigate }) {
//   const steps = [
//     { title: "01. Secure Upload & OCR", desc: "Digital ingestion and high-precision extraction." },
//     { title: "02. RAG Context Retrieval", desc: "Cross-referencing biomarkers with medical indices." },
//     { title: "03. Llama-3 Synthesis", desc: "Generating a compassionate, personalized summary." }
//   ];

//   return (
//     <div style={{ width: '100%' }}>
//       {/* Navbar */}
      

//       {/* Hero: Left Aligned */}
//       {/* Hero: Left Aligned Content + Right Aligned Image */}
// <section className="section-full" id="home" 
//   style={{ 
//     height: '100vh', 
//     display: 'flex', 
//     alignItems: 'center', 
//     justifyContent: 'space-between',
//     padding: '0 5%'
//   }}>
  
//   {/* Left: Text Content */}
//   <div style={{ flex: 1, maxWidth: '600px' }}>
//     <h1 style={{ fontSize: '64px', marginBottom: '20px', lineHeight: '1.1' }}>
//       Clinical Intelligence, Simplified.
//     </h1>
//     <p style={{ fontSize: '20px', color: '#94a3b8', marginBottom: '40px' }}>
//       Transform complex laboratory data into actionable health insights 
//       using RAG-grounded AI analysis.
//     </p>
//     <button className="btn-primary" onClick={() => onNavigate('upload')}>Get Started</button>
//   </div>

//   {/* Right: Illustration/Image */}
//   <div style={{ flex: 1, display: 'flex', justifyContent: 'center' }}>
//     <img 
//       src="/path-to-your-medical-ai-graphic.png" 
//       alt="Clinical AI Analysis" 
//       style={{ width: '80%', maxWidth: '500px', borderRadius: '20px', filter: 'drop-shadow(0 20px 25px rgb(0 0 0 / 0.3))' }} 
//     />
//   </div>
// </section>



//       {/* Ladder: Centered */}
//       export default function Landing({ onNavigate }) {
//   const [activeStep, setActiveStep] = useState(null);

//   const steps = [
//     { id: 0, title: "01. Upload & OCR", summary: "Uses PyTesseract and OpenCV to convert raw scans into machine-readable text with CLAHE enhancement." },
//     { id: 1, title: "02. RAG Retrieval", summary: "Queries our vector database to find medical reference ranges relevant to your specific markers." },
//     { id: 2, title: "03. LLM Parsing", summary: "Analyzes structured data against guidelines to identify abnormalities and synthesize findings." },
//     { id: 3, title: "04. CQS Score", summary: "Our custom Benchmarking engine calculates the Clinical Quality Score to ensure output reliability." }
//   ];

//   return (
//     <section className="section-full" id="how-it-works" style={{ background: '#0f172a', padding: '80px 20px' }}>
//       <h2 style={{ textAlign: 'center', marginBottom: '60px' }}>How It Works</h2>
      
//       {/* Interactive Pipeline Container */}
//       <div className="pipeline-container">
//         <div className="pipeline-line"></div>
//         <div className="pulse-orb"></div>
        
//         {steps.map((step) => (
//           <div 
//             key={step.id} 
//             className={`node ${activeStep === step.id ? 'active' : ''}`}
//             onClick={() => setActiveStep(activeStep === step.id ? null : step.id)}
//             style={{ 
//               borderColor: step.id === 3 ? '#10b981' : '#3b82f6',
//               color: step.id === 3 ? '#10b981' : 'white'
//             }}
//           >
//             <h4 style={{ margin: 0 }}>{step.title}</h4>
//             <div className="node-summary" style={{ marginTop: '10px', fontSize: '13px', color: '#94a3b8' }}>
//               {step.summary}
//             </div>
//           </div>
//         ))}
//       </div>
      
//       <p style={{ textAlign: 'center', marginTop: '60px', color: '#94a3b8' }}>
//         Click a node to explore the technical research methodology behind each stage.
//       </p>
//     </section>
//   );
// }

//       {/* Engine Components: Left Aligned */}
//       <section className="section-full" id="features">
//         <h2 style={{ marginBottom: '40px' }}>Features</h2>
//         <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '20px' }}>
//           {['Native Parser', 'RAG Verification', 'Anomaly Flagging'].map((feat, i) => (
//             <div key={i} className="glass-panel" style={{ padding: '30px', borderRadius: '12px' }}>
//               <h4>{feat}</h4>
//             </div>
//           ))}
//         </div>
//       </section>

      
//     </div>
//   );
// }

import React, { useState } from 'react';
import tickmarkImg from '../assets/images/report_tickmark.jpg';
import domainImg from '../assets/images/Add domain know.jpg';
import summaryImg from '../assets/images/summary.jpg';

export default function Landing({ onNavigate }) {
  const [activeStep, setActiveStep] = useState(null);

  const steps = [
    { id: 0, title: "Upload & OCR", summary: "Uses PyTesseract and OpenCV to convert raw scans into machine-readable text with CLAHE enhancement." },
    { id: 1, title: "LLM Parsing", summary: "Analyzes structured data against guidelines to identify abnormalities and synthesize findings." },
    { id: 2, title: "RAG Retrieval", summary: "Queries our vector database to find medical reference ranges relevant to your specific markers." },
    { id: 3, title: "LLM", summary: "Analyzes structured data and RAG results to provide comprehensive insights." },
    { id: 4, title: "Summary generation", summary: "Creates concise, evidence-based summaries of key findings to facilitate rapid clinical decision-making." }
  ];
  const features = [
  { title: "Native Parser", desc: "Our proprietary engine converts complex, noisy lab scans into structured machine-readable JSON.", img: "/parser.svg" },
  { title: "RAG Verification", desc: "We ground LLM outputs in verified medical indices to eliminate hallucinations and ensure clinical accuracy.", img: "/rag.svg" },
  { title: "Anomaly Flagging", desc: "Automated threshold monitoring highlights critical results that require immediate clinical intervention.", img: "/anomaly.svg" }
];

  return (
    <div style={{ width: '100%' }}>
      {/* Hero Section */}
      <section className="section-full hero-section" id="home">
  <div className="hero-content">
    <h1>Healthcare AI,<br />Simplified for Modern Healthcare.</h1>
    <p>Fast, accurate, and automated medical report understanding
    powered by next-generation AI systems.</p>
    <button className="btn-primary" onClick={() => onNavigate('upload')}>Get Started</button>
  </div>
</section>

{/* Add your Features section here */}
<section id="features">
  {/* Your feature cards... */}
</section>



      <section className="section-full" id="features">
  <h2 style={{ textAlign: 'center', marginBottom: '80px' }}>Features</h2>
  
 
  
  {/* Card 1 */}
  <div className="feature-card">
    <img src={tickmarkImg} className="feature-img" alt="Highlight Issues" />
    <div className="feature-text">
      <h3>Highlight potential Issues</h3>
      <p>Automatically identifies and highlights potential issues in laboratory data that may require further investigation.</p>
    </div>
  </div>

  {/* Card 2: Reversed */}
  <div className="feature-card reverse">
    <img src={domainImg} className="feature-img" alt="Domain Knowledge" />
    <div className="feature-text">
      <h3>Add Domain Knowledge</h3>
      <p>Integrates extensive medical domain knowledge to provide contextually relevant insights and improve the accuracy of the analysis.</p>
    </div>
  </div>

  {/* Card 3: Standard */}
  <div className="feature-card">
    <img src={summaryImg} className="feature-img" alt="Summarize Findings" />
    <div className="feature-text">
      <h3>Summarize Findings</h3>
      <p>Provides concise, evidence-based summaries of key findings to facilitate rapid clinical decision-making.</p>
    </div>
  </div>
</section>


      {/* Interactive Pipeline Section */}
      <section className="section-full" id="how-it-works" style={{ background: '#0f172a', padding: '80px 20px' }}>
        <h2 style={{ textAlign: 'center', marginBottom: '60px' }}>How It Works</h2>
        <div className="pipeline-container">
          <div className="pipeline-line"></div>
          <div className="pulse-orb"></div>
          {steps.map((step) => (
            <div 
              key={step.id} 
              className={`node ${activeStep === step.id ? 'active' : ''}`}
              onClick={() => setActiveStep(activeStep === step.id ? null : step.id)}
              style={{ borderColor: step.id === 3 ? '#10b981' : '#3b82f6', color: step.id === 3 ? '#10b981' : 'white' }}
            >
              <h4 style={{ margin: 0 }}>{step.title}</h4>
              <div className="node-summary" style={{ marginTop: '10px', fontSize: '13px', color: '#94a3b8' }}>
                {step.summary}
              </div>
            </div>
          ))}
        </div>
        
      </section>

      {/* Features Section */}
      



    </div>
  );
}