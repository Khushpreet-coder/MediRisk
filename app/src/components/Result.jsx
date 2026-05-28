// // src/components/Result.jsx
// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
//         setReportData(json.data);
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;
//   if (!reportData) return <div className="dashboard-layout"><p>No analysis metrics found file context empty.</p></div>;

//   const tests = reportData.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status).toLowerCase() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       <div className="panel-grid">
//         {/* Left Col: Dynamic Table Component */}
//         <div className="panel-col glass-panel" style={{ overflowX: 'auto' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.map((test, index) => {
//                 const status = String(test.status || '').toLowerCase().trim();
//                 const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                 return (
//                   <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                     <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                     <td>{test.value || '-'}</td>
//                     <td>{test.unit || '-'}</td>
//                     <td>{test.reference_range || '-'}</td>
//                     <td>{test.status || '-'}</td>
//                   </tr>
//                 );
//               })}
//             </tbody>
//           </table>
//         </div>

//         {/* Right Col: Context Text Box Panel */}
//         <div className="panel-col glass-panel">
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.7', color: '#cbd5e1' }}>
//             {reportData.summary ? (
//               reportData.summary.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '14px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : "No clinical analysis notes generated."}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// src/components/Result.jsx
// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
//         setReportData(json.data);
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;
//   if (!reportData) return <div className="dashboard-layout"><p>No analysis metrics found file context empty.</p></div>;

//   const tests = reportData.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status).toLowerCase() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       <div className="panel-grid">
//         {/* Left Col: Dynamic Table Component */}
//         <div className="panel-col glass-panel" style={{ overflowX: 'auto' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.map((test, index) => {
//                 const status = String(test.status || '').toLowerCase().trim();
//                 const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                 return (
//                   <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                     <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                     <td>{test.value || '-'}</td>
//                     <td>{test.unit || '-'}</td>
//                     <td>{test.reference_range || '-'}</td>
//                     <td>{test.status || '-'}</td>
//                   </tr>
//                 );
//               })}
//             </tbody>
//           </table>
//         </div>

//         {/* Right Col: Context Text Box Panel */}
//         <div className="panel-col glass-panel">
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.7', color: '#cbd5e1' }}>
//             {reportData.summary ? (
//               reportData.summary.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '14px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : "No clinical analysis notes generated."}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// src/components/Result.jsx
// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [summaryText, setSummaryText] = useState("");
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         console.log("📥 Dashboard Payload Successfully Received:", json);

//         // Map top level values out of SQLAlchemy column strings safely
//         setSummaryText(json.summary || "");

//         // Map the inner parsed text JSON data object safely
//         if (json.extracted_data) {
//           setReportData(json.extracted_data);
//         } else {
//           setReportData(json);
//         }
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

//   // Safe validation check matching your backend data objects properties
//   if (!reportData && !summaryText) {
//     return (
//       <div className="dashboard-layout" style={{ paddingTop: '140px', textAlign: 'center' }}>
//         <p>No analysis metrics found file context empty.</p>
//         <button className="btn" onClick={onReset} style={{ marginTop: '20px' }}>Go Back</button>
//       </div>
//     );
//   }

//   // Gracefully reference data models array targets if nested inside extracted_data context dictionary
//   const tests = reportData?.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status).toLowerCase() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       <div className="panel-grid">
//         {/* Left Col: Dynamic Table Component */}
//         <div className="panel-col glass-panel" style={{ overflowX: 'auto' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? (
//                 tests.map((test, index) => {
//                   const status = String(test.status || '').toLowerCase().trim();
//                   const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                   return (
//                     <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                       <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                       <td>{test.value || '-'}</td>
//                       <td>{test.unit || '-'}</td>
//                       <td>{test.reference_range || '-'}</td>
//                       <td>{test.status || '-'}</td>
//                     </tr>
//                   );
//                 })
//               ) : (
//                 <tr>
//                   <td colSpan="5" style={{ textAlign: 'center', padding: '20px', color: '#94a3b8' }}>
//                     No matrix array metrics stored in report dataset record.
//                   </td>
//                 </tr>
//               )}
//             </tbody>
//           </table>
//         </div>

//         {/* Right Col: Context Text Box Panel */}
//         <div className="panel-col glass-panel">
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.7', color: '#cbd5e1', marginTop: '15px' }}>
//             {summaryText ? (
//               summaryText.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '14px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : (
//               <p style={{ color: '#94a3b8',style: 'italic' }}>No clinical analysis notes generated.</p>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [summaryText, setSummaryText] = useState("");
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         console.log("📥 Dashboard Payload Successfully Received:", json);

//         // Map top level values out of SQLAlchemy column strings safely
//         setSummaryText(json.summary || "");

//         // Map the inner parsed text JSON data object safely
//         if (json.extracted_data) {
//           // ✅ FIX: Safely parse the string block into a structured JS object if it arrives as raw text
//           const parsedData = typeof json.extracted_data === "string" 
//             ? JSON.parse(json.extracted_data) 
//             : json.extracted_data;
            
//           setReportData(parsedData);
//         } else {
//           setReportData(json);
//         }
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

//   // Safe validation check matching your backend data objects properties
//   if (!reportData && !summaryText) {
//     return (
//       <div className="dashboard-layout" style={{ paddingTop: '140px', textAlign: 'center' }}>
//         <p>No analysis metrics found file context empty.</p>
//         <button className="btn" onClick={onReset} style={{ marginTop: '20px' }}>Go Back</button>
//       </div>
//     );
//   }

//   // Gracefully reference data models array targets if nested inside extracted_data context dictionary
//   const tests = reportData?.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status).toLowerCase() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       <div className="panel-grid">
//         {/* Left Col: Dynamic Table Component */}
//         <div className="panel-col glass-panel" style={{ overflowX: 'auto' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? (
//                 tests.map((test, index) => {
//                   const status = String(test.status || '').toLowerCase().trim();
//                   const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                   return (
//                     <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                       <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                       <td>{test.value || '-'}</td>
//                       <td>{test.unit || '-'}</td>
//                       <td>{test.reference_range || '-'}</td>
//                       <td>{test.status || '-'}</td>
//                     </tr>
//                   );
//                 })
//               ) : (
//                 <tr>
//                   <td colSpan="5" style={{ textAlign: 'center', padding: '20px', color: '#94a3b8' }}>
//                     No matrix array metrics stored in report dataset record.
//                   </td>
//                 </tr>
//               )}
//             </tbody>
//           </table>
//         </div>

//         {/* Right Col: Context Text Box Panel */}
//         <div className="panel-col glass-panel">
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.7', color: '#cbd5e1', marginTop: '15px' }}>
//             {summaryText ? (
//               summaryText.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '14px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : (
//               <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No clinical analysis notes generated.</p>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }


// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [summaryText, setSummaryText] = useState("");
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         console.log("📥 Dashboard Payload Successfully Received:", json);

//         // Map top level clinical summary text natively
//         setSummaryText(json.summary || "");

//         // ✅ FIXED MATCHING STRUCTURE:
//         // Your backend already handles json.loads() before returning!
//         if (json.extracted_data) {
//           setReportData(json.extracted_data);
//         } else {
//           setReportData(json);
//         }
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

//   // Safe validation check matching your backend data objects properties
//   if (!reportData && !summaryText) {
//     return (
//       <div className="dashboard-layout" style={{ paddingTop: '140px', textAlign: 'center' }}>
//         <p>No analysis metrics found file context empty.</p>
//         <button className="btn" onClick={onReset} style={{ marginTop: '20px' }}>Go Back</button>
//       </div>
//     );
//   }

//   // Safe mapping pointing directly to the tests array extracted from your backend schema configuration
//   const tests = reportData?.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status || '').toLowerCase().trim() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       <div className="panel-grid">
//         {/* Left Col: Dynamic Table Component */}
//         <div className="panel-col glass-panel" style={{ overflowX: 'auto' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? (
//                 tests.map((test, index) => {
//                   const status = String(test.status || '').toLowerCase().trim();
//                   const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                   return (
//                     <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                       <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                       <td>{test.value || '-'}</td>
//                       <td>{test.unit || '-'}</td>
//                       <td>{test.reference_range || '-'}</td>
//                       <td style={{ fontWeight: status !== 'normal' ? 'bold' : 'normal' }}>{test.status || '-'}</td>
//                     </tr>
//                   );
//                 })
//               ) : (
//                 <tr>
//                   <td colSpan="5" style={{ textAlign: 'center', padding: '20px', color: '#94a3b8' }}>
//                     No matrix array metrics stored in report dataset record.
//                   </td>
//                 </tr>
//               )}
//             </tbody>
//           </table>
//         </div>

//         {/* Right Col: Context Text Box Panel */}
//         <div className="panel-col glass-panel">
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.7', color: '#cbd5e1', marginTop: '15px' }}>
//             {summaryText ? (
//               summaryText.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '14px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : (
//               <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No clinical analysis notes generated.</p>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }


// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [summaryText, setSummaryText] = useState("");
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         console.log("📥 Dashboard Payload Successfully Received:", json);

//         // Map top level clinical summary text natively
//         setSummaryText(json.summary || "");

//         // ✅ FIXED MATCHING STRUCTURE:
//         // Your backend already handles json.loads() before returning!
//         if (json.extracted_data) {
//           setReportData(json.extracted_data);
//         } else {
//           setReportData(json);
//         }
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

//   // Safe validation check matching your backend data objects properties
//   if (!reportData && !summaryText) {
//     return (
//       <div className="dashboard-layout" style={{ paddingTop: '140px', textAlign: 'center' }}>
//         <p>No analysis metrics found file context empty.</p>
//         <button className="btn" onClick={onReset} style={{ marginTop: '20px' }}>Go Back</button>
//       </div>
//     );
//   }

//   // Safe mapping pointing directly to the tests array extracted from your backend schema configuration
//   const tests = reportData?.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status || '').toLowerCase().trim() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       <div className="panel-grid">
//         {/* Left Col: Dynamic Table Component */}
//         <div className="panel-col glass-panel" style={{ overflowX: 'auto' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? (
//                 tests.map((test, index) => {
//                   const status = String(test.status || '').toLowerCase().trim();
//                   const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                   return (
//                     <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                       <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                       <td>{test.value || '-'}</td>
//                       <td>{test.unit || '-'}</td>
//                       <td>{test.reference_range || '-'}</td>
//                       <td style={{ fontWeight: status !== 'normal' ? 'bold' : 'normal' }}>{test.status || '-'}</td>
//                     </tr>
//                   );
//                 })
//               ) : (
//                 <tr>
//                   <td colSpan="5" style={{ textAlign: 'center', padding: '20px', color: '#94a3b8' }}>
//                     No matrix array metrics stored in report dataset record.
//                   </td>
//                 </tr>
//               )}
//             </tbody>
//           </table>
//         </div>

//         {/* Right Col: Context Text Box Panel */}
//         <div className="panel-col glass-panel">
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.7', color: '#cbd5e1', marginTop: '15px' }}>
//             {summaryText ? (
//               summaryText.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '14px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : (
//               <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No clinical analysis notes generated.</p>
//             )}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }


// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [summaryText, setSummaryText] = useState("");
//   const [processingStatus, setProcessingStatus] = useState("");
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         console.log("📥 Dashboard Payload Successfully Received:", json);

//         setSummaryText(json.summary || "");
//         setProcessingStatus(json.processing_status || "");

//         if (json.extracted_data) {
//           setReportData(json.extracted_data);
//         } else {
//           setReportData(json);
//         }
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

//   // Check if the backend flagged this specific record row as a failed pipeline execution
//   if (processingStatus === "failed") {
//     return (
//       <div className="dashboard-layout" style={{ paddingTop: '140px', textAlign: 'center' }}>
//         <h2>❌ Processing Run Failed</h2>
//         <p style={{ color: '#94a3b8', marginTop: '10px' }}>
//           This historical record (ID: {reportId}) failed during the backend OCR/LLM generation step.
//         </p>
//         <button className="btn" onClick={onReset} style={{ marginTop: '20px' }}>Upload a New File</button>
//       </div>
//     );
//   }

//   const tests = reportData?.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status || '').toLowerCase().trim() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       {/* Stacked Layout Structure */}
//       <div className="panel-stack" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        
//         {/* Top: Laboratory Matrix Table */}
//         <div className="glass-panel" style={{ overflowX: 'auto', width: '100%' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left', marginTop: '15px' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? (
//                 tests.map((test, index) => {
//                   const status = String(test.status || '').toLowerCase().trim();
//                   const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                   return (
//                     <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                       <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                       <td>{test.value || '-'}</td>
//                       <td>{test.unit || '-'}</td>
//                       <td>{test.reference_range || '-'}</td>
//                       <td style={{ fontWeight: status !== 'normal' ? 'bold' : 'normal' }}>{test.status || '-'}</td>
//                     </tr>
//                   );
//                 })
//               ) : (
//                 <tr>
//                   <td colSpan="5" style={{ textAlign: 'center', padding: '30px', color: '#94a3b8' }}>
//                     No valid data metrics found for Report ID #{reportId}. Please run a fresh file scan.
//                   </td>
//                 </tr>
//               )}
//             </tbody>
//           </table>
//         </div>

//         {/* Bottom: Summary Panel */}
//         <div className="glass-panel" style={{ width: '100%' }}>
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.8', color: '#cbd5e1', marginTop: '15px', fontSize: '15px' }}>
//             {summaryText ? (
//               summaryText.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '16px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : (
//               <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No clinical analysis notes available for this record entry.</p>
//             )}
//           </div>
//         </div>

//       </div>
//     </div>
//   );
// }


// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [summaryText, setSummaryText] = useState("");
//   const [processingStatus, setProcessingStatus] = useState("");
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         console.log("📥 Dashboard Payload Successfully Received:", json);

//         setSummaryText(json.summary || "");
//         setProcessingStatus(json.processing_status || "");

//         if (json.extracted_data) {
//           setReportData(json.extracted_data);
//         } else {
//           setReportData(json);
//         }
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

//   // Check if the backend flagged this specific record row as a failed pipeline execution
//   if (processingStatus === "failed") {
//     return (
//       <div className="dashboard-layout" style={{ paddingTop: '140px', textAlign: 'center' }}>
//         <h2>❌ Processing Run Failed</h2>
//         <p style={{ color: '#94a3b8', marginTop: '10px' }}>
//           This historical record (ID: {reportId}) failed during the backend OCR/LLM generation step.
//         </p>
//         <button className="btn" onClick={onReset} style={{ marginTop: '20px' }}>Upload a New File</button>
//       </div>
//     );
//   }

//   const tests = reportData?.tests || [];
//   const abnormalCount = tests.filter(t => String(t.status || '').toLowerCase().trim() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       {/* Stacked Layout Structure */}
//       <div className="panel-stack" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        
//         {/* Top: Laboratory Matrix Table */}
//         <div className="glass-panel" style={{ overflowX: 'auto', width: '100%' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left', marginTop: '15px' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? (
//                 tests.map((test, index) => {
//                   const status = String(test.status || '').toLowerCase().trim();
//                   const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                   return (
//                     <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                       <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                       <td>{test.value || '-'}</td>
//                       <td>{test.unit || '-'}</td>
//                       <td>{test.reference_range || '-'}</td>
//                       <td style={{ fontWeight: status !== 'normal' ? 'bold' : 'normal' }}>{test.status || '-'}</td>
//                     </tr>
//                   );
//                 })
//               ) : (
//                 <tr>
//                   <td colSpan="5" style={{ textAlign: 'center', padding: '30px', color: '#94a3b8' }}>
//                     No valid data metrics found for Report ID #{reportId}. Please run a fresh file scan.
//                   </td>
//                 </tr>
//               )}
//             </tbody>
//           </table>
//         </div>

//         {/* Bottom: Summary Panel */}
//         <div className="glass-panel" style={{ width: '100%' }}>
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.8', color: '#cbd5e1', marginTop: '15px', fontSize: '15px' }}>
//             {summaryText ? (
//               summaryText.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '16px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : (
//               <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No clinical analysis notes available for this record entry.</p>
//             )}
//           </div>
//         </div>

//       </div>
//     </div>
//   );
// }


// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [summaryText, setSummaryText] = useState("");
//   const [processingStatus, setProcessingStatus] = useState("");
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchReportMetrics = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         console.log("📥 Dashboard Payload Successfully Received:", json);

//         setSummaryText(json.summary || "");
//         setProcessingStatus(json.processing_status || "");

//         if (json.extracted_data) {
//           setReportData(json.extracted_data);
//         } else {
//           setReportData(json);
//         }
//       } catch (err) {
//         console.error("Dashboard fetching failure:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchReportMetrics();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

//   if (processingStatus === "failed") {
//     return (
//       <div className="dashboard-layout" style={{ paddingTop: '140px', textAlign: 'center' }}>
//         <h2>❌ Processing Run Failed</h2>
//         <p style={{ color: '#94a3b8', marginTop: '10px' }}>
//           This historical record (ID: {reportId}) failed during the backend OCR/LLM generation step.
//         </p>
//         <button className="btn" onClick={onReset} style={{ marginTop: '20px' }}>Upload a New File</button>
//       </div>
//     );
//   }

//   const tests = reportData?.tests || [];
//   const ragContext = reportData?.rag_context || [];
//   const abnormalCount = tests.filter(t => String(t.status || '').toLowerCase().trim() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       {/* Widget Layer */}
//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       {/* Stacked Layout Structure */}
//       <div className="panel-stack" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        
//         {/* Top: Laboratory Matrix Table */}
//         <div className="glass-panel" style={{ overflowX: 'auto', width: '100%' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left', marginTop: '15px' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter Axis</th>
//                 <th>Observed Value</th>
//                 <th>Dimension</th>
//                 <th>Reference Bounds</th>
//                 <th>State Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? (
//                 tests.map((test, index) => {
//                   const status = String(test.status || '').toLowerCase().trim();
//                   const rowClass = status === 'high' ? 'high-row' : status === 'low' ? 'low-row' : 'normal-row';
//                   return (
//                     <tr key={index} className={rowClass} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                       <td style={{ padding: '14px 8px' }}><strong>{test.test_name || '-'}</strong></td>
//                       <td>{test.value || '-'}</td>
//                       <td>{test.unit || '-'}</td>
//                       <td>{test.reference_range || '-'}</td>
//                       <td style={{ fontWeight: status !== 'normal' ? 'bold' : 'normal' }}>{test.status || '-'}</td>
//                     </tr>
//                   );
//                 })
//               ) : (
//                 <tr>
//                   <td colSpan="5" style={{ textAlign: 'center', padding: '30px', color: '#94a3b8' }}>
//                     No valid data metrics found for Report ID #{reportId}. Please run a fresh file scan.
//                   </td>
//                 </tr>
//               )}
//             </tbody>
//           </table>
//         </div>

//         {/* Middle: Live Vector Database Verification Layer (Great for Teachers!) */}
//         <div className="glass-panel" style={{ width: '100%', borderLeft: '4px solid #38bdf8' }}>
//           <h2>📚 Retrieved RAG Medical Context (ChromaDB Verification)</h2>
//           <p style={{ fontSize: '13px', color: '#94a3b8', marginTop: '4px' }}>
//             Below are the raw text chunks selected via semantic ranking algorithm directly supporting the executive generation step:
//           </p>
//           <div style={{ marginTop: '15px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
//             {ragContext.length > 0 && ragContext[0] !== "No structured metrics available to query vector storage." ? (
//               ragContext.map((chunk, idx) => (
//                 <div key={idx} style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '6px', fontSize: '13.5px', border: '1px solid rgba(255,255,255,0.05)', color: '#cbd5e1', lineHeight: '1.6' }}>
//                   <span style={{ color: '#38bdf8', fontWeight: 'bold', display: 'block', marginBottom: '4px' }}>Knowledge Source Vector #{idx + 1}:</span>
//                   "{chunk}"
//                 </div>
//               ))
//             ) : (
//               <p style={{ color: '#ef4444', fontStyle: 'italic' }}>No reference vectors fetched. Ensure the laboratory matrix table parses elements successfully.</p>
//             )}
//           </div>
//         </div>

//         {/* Bottom: Summary Panel */}
//         <div className="glass-panel" style={{ width: '100%' }}>
//           <h2>📝 RAG System Synthesis Guidance Summary</h2>
//           <div style={{ lineHeight: '1.8', color: '#cbd5e1', marginTop: '15px', fontSize: '15px' }}>
//             {summaryText ? (
//               summaryText.split('\n\n').map((para, i) => (
//                 <p key={i} style={{ marginBottom: '16px' }}>
//                   {para.replace(/\*\*/g, '')}
//                 </p>
//               ))
//             ) : (
//               <p style={{ color: '#94a3b8', fontStyle: 'italic' }}>No clinical analysis notes available for this record entry.</p>
//             )}
//           </div>
//         </div>

//       </div>
//     </div>
//   );
// }


// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [reportData, setReportData] = useState(null);
//   const [loading, setLoading] = useState(true);

// // Replace your existing useEffect logic with this:
// useEffect(() => {
//   const fetchReportMetrics = async () => {
//     try {
//       const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//       const json = await res.json();
      
//       console.log("DEBUG: API Response Received:", json);

//       // The backend returns the report at the top level
//       // The structured tests are inside 'extracted_data'
//       if (json.extracted_data) {
//         setReportData({
//           tests: json.extracted_data.tests || [],
//           rag_context: json.extracted_data.rag_context || [],
//           summary: json.summary || json.extracted_data.summary || ""
//         });
//       }
//     } catch (err) {
//       console.error("Dashboard fetch error:", err);
//     } finally {
//       setLoading(false);
//     }
//   };
//   if (reportId) fetchReportMetrics();
// }, [reportId]);

//   if (loading) return <div className="dashboard-layout"><div className="spinner">Loading Analysis...</div></div>;

//   const tests = reportData?.tests || [];
//   const ragContext = reportData?.rag_context || [];
//   const summaryText = reportData?.summary || "";
//   const abnormalCount = tests.filter(t => String(t.status || '').toLowerCase().trim() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       <div className="panel-stack" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
        
//         {/* Laboratory Matrix Table */}
//         <div className="glass-panel" style={{ overflowX: 'auto', width: '100%' }}>
//           <h2>📊 Laboratory Test Matrix Array</h2>
//           <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px', textAlign: 'left', marginTop: '15px' }}>
//             <thead>
//               <tr style={{ borderBottom: '2px solid rgba(255,255,255,0.1)', height: '40px', color: '#94a3b8' }}>
//                 <th style={{ padding: '8px' }}>Test Parameter</th>
//                 <th>Value</th>
//                 <th>Unit</th>
//                 <th>Reference</th>
//                 <th>Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {tests.length > 0 ? tests.map((test, index) => (
//                 <tr key={index} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
//                   <td style={{ padding: '14px 8px' }}><strong>{test.test_name}</strong></td>
//                   <td>{test.value}</td>
//                   <td>{test.unit || '-'}</td>
//                   <td>{test.reference_range || '-'}</td>
//                   <td style={{ color: test.status !== 'Normal' ? '#f87171' : '#4ade80' }}>{test.status}</td>
//                 </tr>
//               )) : <tr><td colSpan="5" style={{ textAlign: 'center', padding: '30px' }}>No metrics found.</td></tr>}
//             </tbody>
//           </table>
//         </div>

//         {/* RAG Context Layer */}
//         <div className="glass-panel" style={{ width: '100%', borderLeft: '4px solid #38bdf8' }}>
//           <h2>📚 Retrieved RAG Medical Context</h2>
//           <div style={{ marginTop: '15px', display: 'flex', flexDirection: 'column', gap: '10px' }}>
//             {ragContext.length > 0 ? ragContext.map((chunk, idx) => (
//               <div key={idx} style={{ padding: '12px', background: 'rgba(255,255,255,0.03)', borderRadius: '6px', fontSize: '13px', border: '1px solid rgba(255,255,255,0.05)' }}>
//                 <span style={{ color: '#38bdf8', fontWeight: 'bold' }}>Source #{idx + 1}: </span>
//                 {chunk}
//               </div>
//             )) : <p>No RAG context retrieved.</p>}
//           </div>
//         </div>

//         {/* Final Summary */}
//         <div className="glass-panel" style={{ width: '100%' }}>
//           <h2>📝 RAG System Synthesis Summary</h2>
//           <div style={{ lineHeight: '1.8', color: '#cbd5e1', marginTop: '15px' }}>
//             {summaryText || "No clinical analysis notes available."}
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [data, setData] = useState({ tests: [], summary: "Loading...", rag_context: [] });
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchData = async () => {
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         // --- DATA DETECTIVE LOGIC ---
//         // Searches for 'tests', 'summary', and 'rag_context' anywhere in the response
//         const findKey = (obj, key) => {
//           if (obj[key]) return obj[key];
//           for (let k in obj) {
//             if (typeof obj[k] === 'object' && obj[k] !== null) {
//               const found = findKey(obj[k], key);
//               if (found !== undefined) return found;
//             }
//           }
//           return null;
//         };

//         setData({
//           tests: findKey(json, 'tests') || [],
//           summary: findKey(json, 'summary') || "No clinical summary found.",
//           rag_context: findKey(json, 'rag_context') || []
//         });

//       } catch (err) {
//         console.error("Dashboard error:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     if (reportId) fetchData();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout">Loading Analysis...</div>;

//   const { tests, rag_context, summary } = data;
//   const abnormalCount = tests.filter(t => String(t.status || '').toLowerCase() !== 'normal').length;

//   return (
//     <div className="dashboard-layout">
//       <header className="dash-header">
//         <h1>Analysis Summary Output</h1>
//         <button className="btn" onClick={onReset}>🔬 Scan Another File</button>
//       </header>

//       <div className="stats-box">
//         <div className="stat-card glass-panel"><h3>{tests.length}</h3><p>Parsed Biometrics</p></div>
//         <div className="stat-card glass-panel alert"><h3>{abnormalCount}</h3><p>Anomalies Flagged</p></div>
//       </div>

//       {/* Laboratory Matrix */}
//       <div className="glass-panel" style={{ width: '100%', marginBottom: '20px' }}>
//         <h2>📊 Laboratory Test Matrix Array</h2>
//         <table style={{ width: '100%', borderCollapse: 'collapse' }}>
//           <thead>
//             <tr style={{ color: '#94a3b8', borderBottom: '1px solid #333' }}>
//               <th style={{ padding: '10px' }}>Parameter</th><th>Value</th><th>Status</th>
//             </tr>
//           </thead>
//           <tbody>
//             {tests.map((t, i) => (
//               <tr key={i} style={{ borderBottom: '1px solid #222' }}>
//                 <td style={{ padding: '10px' }}>{t.test_name}</td>
//                 <td>{t.value} {t.unit}</td>
//                 <td style={{ color: t.status !== 'Normal' ? '#f87171' : '#4ade80' }}>{t.status}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>

//       {/* Synthesis Summary */}
//       <div className="glass-panel">
//         <h2>📝 RAG System Synthesis Summary</h2>
//         <p style={{ lineHeight: '1.6', color: '#cbd5e1' }}>{summary}</p>
//       </div>

//       {/* RAG Context */}
//       <div className="glass-panel" style={{ marginTop: '20px' }}>
//         <h2>📚 Retrieved Context</h2>
//         {rag_context.map((c, i) => <p key={i} style={{ fontSize: '12px', color: '#64748b' }}>• {c}</p>)}
//       </div>
//     </div>
//   );
// }


// import React, { useState, useEffect } from 'react';

// export default function Result({ reportId, onReset }) {
//   const [data, setData] = useState({ tests: [], summary: "Loading analysis..." });
//   const [loading, setLoading] = useState(true);

//   useEffect(() => {
//     const fetchData = async () => {
//       if (!reportId) return;
//       try {
//         const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
//         const json = await res.json();
        
//         // This targets the JSON exactly as your backend saves it
//         const payload = json.extracted_data || {};
        
//         setData({
//           tests: payload.tests || [],
//           summary: json.summary || payload.summary || "No clinical summary available."
//         });
//       } catch (err) {
//         console.error("Fetch error:", err);
//       } finally {
//         setLoading(false);
//       }
//     };
//     fetchData();
//   }, [reportId]);

//   if (loading) return <div className="dashboard-layout">Loading...</div>;

//   return (
//     <div className="dashboard-layout" style={{ maxWidth: '1000px', margin: '40px auto', padding: '0 20px' }}>
//       <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '40px' }}>
//         <h1>Clinical Analysis</h1>
//         <button className="btn" onClick={onReset}>Scan Another</button>
//       </header>

//       {/* Wide, Open Table */}
//       <div className="glass-panel" style={{ padding: '30px', marginBottom: '40px' }}>
//         <h2 style={{ marginBottom: '20px' }}>Laboratory Test Results</h2>
//         {data.tests.length > 0 ? (
//           <table style={{ width: '100%', borderCollapse: 'collapse' }}>
//             <thead>
//               <tr style={{ color: '#94a3b8', borderBottom: '1px solid #333' }}>
//                 <th style={{ padding: '15px', textAlign: 'left' }}>Parameter</th>
//                 <th style={{ padding: '15px', textAlign: 'left' }}>Value</th>
//                 <th style={{ padding: '15px', textAlign: 'left' }}>Status</th>
//               </tr>
//             </thead>
//             <tbody>
//               {data.tests.map((t, i) => (
//                 <tr key={i} style={{ borderBottom: '1px solid #222' }}>
//                   <td style={{ padding: '15px' }}>{t.test_name}</td>
//                   <td style={{ padding: '15px' }}>{t.value} {t.unit}</td>
//                   <td style={{ padding: '15px', color: t.status !== 'Normal' ? '#f87171' : '#4ade80' }}>{t.status}</td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         ) : (
//           <p style={{ padding: '20px', color: '#64748b' }}>No lab data found in the report. Please check the backend extraction log.</p>
//         )}
//       </div>

//       {/* Spacious Summary */}
//       <div className="glass-panel" style={{ padding: '40px' }}>
//         <h2>Clinical Summary</h2>
//         <p style={{ lineHeight: '2', fontSize: '16px', color: '#cbd5e1' }}>{data.summary}</p>
//       </div>
//     </div>
//   );
// }


import React, { useState, useEffect } from 'react';

export default function Result({ reportId, onReset }) {
  const [data, setData] = useState({ tests: [], summary: "Loading analysis..." });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      if (!reportId) return;
      try {
        const res = await fetch(`http://127.0.0.1:8000/reports/report/${reportId}`);
        const json = await res.json();
        const payload = json.extracted_data || {};
        
        setData({
          tests: payload.tests || [],
          summary: json.summary || payload.summary || "No clinical summary available."
        });
      } catch (err) {
        console.error("Fetch error:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [reportId]);

  const handleDownload = () => {
    const content = `CLINICAL ANALYSIS SUMMARY\n\n${data.summary}`;
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `medical_summary_${reportId}.txt`;
    a.click();
  };

  if (loading) return <div className="dashboard-layout"><div className="spinner"></div></div>;

  return (
    <div className="dashboard-layout" style={{ maxWidth: '1000px', margin: '40px auto', padding: '0 20px' }}>
      <header style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '40px' }}>
        <h1>Clinical Analysis</h1>
        <button className="btn-primary" onClick={onReset}>Scan Another</button>
      </header>

      {/* Lab Results Table */}
      <div className="glass-panel" style={{ padding: '30px', marginBottom: '40px' }}>
        <h2 style={{ marginBottom: '20px' }}>Laboratory Test Results</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ color: '#94a3b8', borderBottom: '1px solid #334155' }}>
              <th style={{ padding: '15px', textAlign: 'left' }}>Parameter</th>
              <th style={{ padding: '15px', textAlign: 'left' }}>Value</th>
              <th style={{ padding: '15px', textAlign: 'left' }}>Status</th>
            </tr>
          </thead>
          <tbody>
            {data.tests.map((t, i) => (
              <tr key={i} style={{ borderBottom: '1px solid #1e293b' }}>
                <td style={{ padding: '15px' }}>{t.test_name}</td>
                <td style={{ padding: '15px' }}>{t.value} {t.unit}</td>
                <td style={{ padding: '15px', color: t.status !== 'Normal' ? '#f87171' : '#4ade80' }}>
                  {t.status}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Summary Section */}
      <div className="glass-panel" style={{ padding: '40px' }}>
        <h2 style={{ marginBottom: '20px' }}>Clinical Summary</h2>
        <p style={{ lineHeight: '1.8', fontSize: '18px', color: '#cbd5e1', marginBottom: '30px' }}>
          {data.summary}
        </p>

        {/* Action Area */}
        <div style={{ borderTop: '1px solid #1e293b', paddingTop: '20px' }}>
          <button className="btn-primary" onClick={handleDownload}>
            Download Summary
          </button>
          <p style={{ marginTop: '20px', fontSize: '0.85rem', color: '#64748b', fontStyle: 'italic' }}>
            * Disclaimer: This summary is generated by AI. Please verify all clinical findings with a qualified medical professional before making healthcare decisions.
          </p>
        </div>
      </div>
    </div>
  );
}