import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import ScanForm from './components/ScanForm';
import ResultsTable from './components/ResultsTable';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [currentView, setCurrentView] = useState('dashboard');

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setCurrentView('dashboard');
  };

  if (!token) {
    return <Login setToken={setToken} />;
  }

  return (
    <div className="App">
      <nav className="navbar">
        <div className="nav-brand">
          <h2>🔍 VulnScan Pro</h2>
        </div>
        <div className="nav-menu">
          <button 
            className={currentView === 'dashboard' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentView('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={currentView === 'scan' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentView('scan')}
          >
            New Scan
          </button>
          <button 
            className={currentView === 'results' ? 'nav-btn active' : 'nav-btn'}
            onClick={() => setCurrentView('results')}
          >
            Scan History
          </button>
          <button className="nav-btn logout" onClick={logout}>
            Logout
          </button>
        </div>
      </nav>

      <main className="main-content">
        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'scan' && <ScanForm />}
        {currentView === 'results' && <ResultsTable />}
      </main>
    </div>
  );
}

export default App;