import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ResultsTable = () => {
  const [scans, setScans] = useState([]);
  const [selectedScan, setSelectedScan] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchScans();
  }, []);

  const fetchScans = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.get('http://localhost:5000/api/scans', { headers });
      setScans(response.data);
    } catch (error) {
      console.error('Error fetching scans:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchScanDetails = async (scanId) => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.get(`http://localhost:5000/api/scan/${scanId}`, { headers });
      setSelectedScan(response.data);
    } catch (error) {
      console.error('Error fetching scan details:', error);
    }
  };

  const getSeverityColor = (severity) => {
    switch(severity?.toLowerCase()) {
      case 'high': return '#e74c3c';
      case 'medium': return '#f39c12';
      case 'low': return '#f1c40f';
      default: return '#95a5a6';
    }
  };

  if (loading) {
    return <div className="loading">Loading scan history...</div>;
  }

  return (
    <div className="results-container">
      <div className="results-header">
        <h2>📊 Scan History & Results</h2>
        <p>View and analyze your security scan results</p>
      </div>

      <div className="results-layout">
        <div className="scans-list">
          <h3>Scan History</h3>
          {scans.length > 0 ? (
            <div className="scans-table">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Target</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Date</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {scans.map((scan) => (
                    <tr key={scan.id} className={selectedScan?.id === scan.id ? 'selected' : ''}>
                      <td>#{scan.id}</td>
                      <td>{scan.target}</td>
                      <td>
                        <span className="scan-type">{scan.scan_type}</span>
                      </td>
                      <td>
                        <span className={`status ${scan.status}`}>
                          {scan.status}
                        </span>
                      </td>
                      <td>{new Date(scan.created_at).toLocaleDateString()}</td>
                      <td>
                        <button 
                          className="btn btn-sm btn-outline"
                          onClick={() => fetchScanDetails(scan.id)}
                        >
                          View Details
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="no-data">
              <p>No scans found. Start your first security scan!</p>
            </div>
          )}
        </div>

        {selectedScan && (
          <div className="scan-details">
            <h3>Scan Details - #{selectedScan.id}</h3>
            <div className="scan-meta">
              <div className="meta-item">
                <strong>Target:</strong> {selectedScan.target}
              </div>
              <div className="meta-item">
                <strong>Type:</strong> {selectedScan.scan_type}
              </div>
              <div className="meta-item">
                <strong>Status:</strong> 
                <span className={`status ${selectedScan.status}`}>
                  {selectedScan.status}
                </span>
              </div>
              <div className="meta-item">
                <strong>Started:</strong> {new Date(selectedScan.created_at).toLocaleString()}
              </div>
              {selectedScan.completed_at && (
                <div className="meta-item">
                  <strong>Completed:</strong> {new Date(selectedScan.completed_at).toLocaleString()}
                </div>
              )}
            </div>

            {selectedScan.results && (
              <div className="scan-results">
                <h4>🔍 Scan Results</h4>

                {selectedScan.results.port_scan && (
                  <div className="result-section">
                    <h5>Port Scan Results</h5>
                    <div className="ports-info">
                      <p><strong>Open Ports:</strong> {selectedScan.results.port_scan.open_ports?.join(', ') || 'None'}</p>
                    </div>

                    {selectedScan.results.port_scan.vulnerabilities && (
                      <div className="vulnerabilities">
                        <h6>Port-related Vulnerabilities:</h6>
                        {selectedScan.results.port_scan.vulnerabilities.map((vuln, index) => (
                          <div key={index} className="vulnerability-item" 
                               style={{ borderLeftColor: getSeverityColor(vuln.severity) }}>
                            <h6>{vuln.type}</h6>
                            <p><strong>Severity:</strong> {vuln.severity}</p>
                            <p>{vuln.description}</p>
                            {vuln.port && <p><strong>Port:</strong> {vuln.port}</p>}
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {selectedScan.results.web_scan && (
                  <div className="result-section">
                    <h5>Web Security Scan Results</h5>

                    {selectedScan.results.web_scan.vulnerabilities && (
                      <div className="vulnerabilities">
                        <h6>Web Vulnerabilities:</h6>
                        {selectedScan.results.web_scan.vulnerabilities.map((vuln, index) => (
                          <div key={index} className="vulnerability-item"
                               style={{ borderLeftColor: getSeverityColor(vuln.severity) }}>
                            <h6>{vuln.type}</h6>
                            <p><strong>Severity:</strong> {vuln.severity}</p>
                            <p>{vuln.description}</p>
                          </div>
                        ))}
                      </div>
                    )}

                    {selectedScan.results.web_scan.security_headers && (
                      <div className="security-headers">
                        <h6>Security Headers Analysis:</h6>
                        <div className="headers-grid">
                          {Object.entries(selectedScan.results.web_scan.security_headers).map(([header, value]) => (
                            <div key={header} className="header-item">
                              <strong>{header}:</strong> 
                              <span className={value === 'Missing' ? 'missing' : 'present'}>
                                {value}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}

            {selectedScan.error && (
              <div className="scan-error">
                <h4>❌ Scan Error</h4>
                <p>{selectedScan.error}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ResultsTable;