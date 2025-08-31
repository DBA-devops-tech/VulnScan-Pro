import React, { useState } from 'react';
import axios from 'axios';

const ScanForm = () => {
  const [formData, setFormData] = useState({
    target: '',
    scan_type: 'basic'
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      const response = await axios.post('http://localhost:5000/api/scan', formData, { headers });
      setMessage(`Scan started successfully! Scan ID: ${response.data.scan_id}`);
      setFormData({ target: '', scan_type: 'basic' });
    } catch (error) {
      setMessage(error.response?.data?.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="scan-form-container">
      <div className="scan-form-header">
        <h2>🎯 Start New Security Scan</h2>
        <p>Configure and launch a comprehensive security assessment</p>
      </div>

      <div className="scan-form-card">
        <form onSubmit={handleSubmit} className="scan-form">
          <div className="form-group">
            <label htmlFor="target">Target URL/IP Address</label>
            <input
              type="text"
              id="target"
              name="target"
              value={formData.target}
              onChange={handleChange}
              required
              placeholder="e.g., example.com or 192.168.1.1"
              className="form-control"
            />
            <small className="form-help">
              Enter a domain name, IP address, or URL to scan
            </small>
          </div>

          <div className="form-group">
            <label htmlFor="scan_type">Scan Type</label>
            <select
              id="scan_type"
              name="scan_type"
              value={formData.scan_type}
              onChange={handleChange}
              className="form-control"
            >
              <option value="basic">Basic Scan</option>
              <option value="comprehensive">Comprehensive Scan</option>
              <option value="port_only">Port Scan Only</option>
              <option value="web_only">Web Vulnerabilities Only</option>
            </select>
            <small className="form-help">
              Choose the type of security assessment to perform
            </small>
          </div>

          <div className="scan-types-info">
            <h4>Scan Type Information</h4>
            <div className="scan-info-grid">
              <div className="scan-info-item">
                <h5>🔍 Basic Scan</h5>
                <p>Quick assessment covering common ports and basic web vulnerabilities</p>
              </div>
              <div className="scan-info-item">
                <h5>🔬 Comprehensive Scan</h5>
                <p>In-depth analysis including advanced port scanning and web security testing</p>
              </div>
              <div className="scan-info-item">
                <h5>🌐 Port Scan Only</h5>
                <p>Focus on network ports and services discovery</p>
              </div>
              <div className="scan-info-item">
                <h5>📄 Web Vulnerabilities Only</h5>
                <p>Web application security assessment and vulnerability detection</p>
              </div>
            </div>
          </div>

          {message && (
            <div className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}

          <div className="form-actions">
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Starting Scan...
                </>
              ) : (
                <>
                  🚀 Start Scan
                </>
              )}
            </button>
          </div>
        </form>

        <div className="scan-warning">
          <h4>⚠️ Important Notice</h4>
          <p>
            Only scan systems you own or have explicit permission to test. 
            Unauthorized scanning may be illegal and could violate terms of service.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ScanForm;