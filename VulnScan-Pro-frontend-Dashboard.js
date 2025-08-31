import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_scans: 0,
    recent_scans: 0,
    completed_scans: 0,
    vulnerabilities_found: 0
  });
  const [recentScans, setRecentScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      // Fetch stats
      const statsResponse = await axios.get('http://localhost:5000/api/dashboard/stats', { headers });
      setStats(statsResponse.data);

      // Fetch recent scans
      const scansResponse = await axios.get('http://localhost:5000/api/scans', { headers });
      setRecentScans(scansResponse.data.slice(0, 5)); // Last 5 scans

    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading dashboard...</div>;
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h2>Security Dashboard</h2>
        <p>Overview of your security scanning activities</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-icon">📊</div>
          <div className="stat-info">
            <h3>{stats.total_scans}</h3>
            <p>Total Scans</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">⚡</div>
          <div className="stat-info">
            <h3>{stats.recent_scans}</h3>
            <p>Scans This Week</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">✅</div>
          <div className="stat-info">
            <h3>{stats.completed_scans}</h3>
            <p>Completed Scans</p>
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-icon">🚨</div>
          <div className="stat-info">
            <h3>{stats.vulnerabilities_found}</h3>
            <p>Vulnerabilities Found</p>
          </div>
        </div>
      </div>

      <div className="recent-activity">
        <h3>Recent Scan Activity</h3>
        {recentScans.length > 0 ? (
          <div className="scans-table">
            <table>
              <thead>
                <tr>
                  <th>Target</th>
                  <th>Type</th>
                  <th>Status</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {recentScans.map((scan) => (
                  <tr key={scan.id}>
                    <td>{scan.target}</td>
                    <td>
                      <span className="scan-type">{scan.scan_type}</span>
                    </td>
                    <td>
                      <span className={`status ${scan.status}`}>{scan.status}</span>
                    </td>
                    <td>{new Date(scan.created_at).toLocaleDateString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="no-data">
            <p>No scans performed yet. Start your first security scan!</p>
          </div>
        )}
      </div>

      <div className="quick-actions">
        <h3>Quick Actions</h3>
        <div className="action-buttons">
          <button className="action-btn">
            <span>🎯</span>
            <div>
              <h4>Quick Scan</h4>
              <p>Perform a basic security scan</p>
            </div>
          </button>
          <button className="action-btn">
            <span>🔍</span>
            <div>
              <h4>Deep Scan</h4>
              <p>Comprehensive vulnerability assessment</p>
            </div>
          </button>
          <button className="action-btn">
            <span>📋</span>
            <div>
              <h4>Generate Report</h4>
              <p>Create detailed security report</p>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;