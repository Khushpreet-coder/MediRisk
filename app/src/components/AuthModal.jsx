import React, { useState } from 'react';

export default function AuthModal({ onClose, onLoginSuccess, initialMode }) {
  const [mode, setMode] = useState(initialMode || 'login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const API = '/api/auth/auth';

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const endpoint = mode === 'login' ? `${API}/login` : `${API}/register`;
      const res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || 'Something went wrong');
        return;
      }

      if (mode === 'login') {
        const token = data.access_token;
        localStorage.setItem('token', token);
        localStorage.setItem('username', username);
        onLoginSuccess({ username, token });
        onClose();
      } else {
        setMode('login');
        setError('Registered successfully! Please log in.');
      }
    } catch {
      setError('Network error. Is the server running?');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-overlay" onClick={onClose}>
      <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
        <button className="auth-close" onClick={onClose}>✕</button>
        <h2>{mode === 'login' ? 'Welcome Back' : 'Create Account'}</h2>
        <p className="auth-subtitle">
          {mode === 'login' ? 'Sign in to access your reports' : 'Register to start analysing'}
        </p>

        <form onSubmit={handleSubmit} className="auth-form">
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            className="auth-input"
          />
          <div className="password-wrap">
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Password (min 8 chars, 1 letter, 1 digit)"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="auth-input"
              minLength={8}
            />
            <button type="button" className="password-toggle" onClick={() => setShowPassword(!showPassword)} tabIndex={-1}>
              {showPassword ? '👁️' : '👁️'}
            </button>
          </div>
          {error && <p className="auth-error">{error}</p>}
          <button type="submit" className="btn-primary auth-submit" disabled={loading}>
            {loading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Register'}
          </button>
        </form>

        <p className="auth-toggle">
          {mode === 'login' ? (
            <>Don't have an account? <button onClick={() => { setMode('register'); setError(''); }} className="auth-link">Register</button></>
          ) : (
            <>Already registered? <button onClick={() => { setMode('login'); setError(''); }} className="auth-link">Sign In</button></>
          )}
        </p>
      </div>
    </div>
  );
}
