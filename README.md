# 🔍 VulnScan Pro - Professional Security Vulnerability Scanner

[![Security Scanner](https://img.shields.io/badge/Type-Security%20Scanner-red)](https://github.com/SyedhyperX/VulnScan-Pro)
[![Python](https://img.shields.io/badge/Backend-Python%20Flask-blue)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/Frontend-React.js-61dafb)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A comprehensive web-based security vulnerability scanner with an intuitive dashboard for penetration testers and cybersecurity professionals.

## 🌟 Features

### 🔍 **Comprehensive Scanning**
- **Port Scanning**: Advanced network port discovery and service enumeration
- **Web Vulnerability Assessment**: OWASP Top 10 and common web vulnerabilities
- **SSL/TLS Security Analysis**: Certificate validation and cipher strength testing
- **Security Headers Analysis**: Missing security headers detection
- **Information Disclosure Detection**: Sensitive data exposure identification

### 📊 **Professional Dashboard**
- Real-time scan monitoring and progress tracking
- Interactive vulnerability severity classification
- Detailed security reports with actionable insights
- Historical scan data and trend analysis
- Exportable reports (JSON, HTML, CSV)

### 🛡️ **Security Features**
- JWT-based authentication system
- Role-based access control
- Secure API endpoints
- Input validation and sanitization
- Rate limiting and abuse prevention

### 🚀 **Modern Tech Stack**
- **Backend**: Python Flask with RESTful APIs
- **Frontend**: React.js with modern UI components
- **Database**: SQLite with migration support
- **Security**: Bcrypt password hashing, JWT tokens
- **Styling**: Custom CSS with responsive design

## 🏗️ Project Structure

```
VulnScan-Pro/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── models.py              # Database models and schemas
│   ├── routes.py              # API route definitions
│   ├── scanner/
│   │   ├── port_scanner.py    # Network port scanning module
│   │   ├── web_scanner.py     # Web vulnerability scanner
│   │   └── report_generator.py # Report generation engine
│   ├── utils/
│   │   ├── auth.py           # Authentication utilities
│   │   └── database.py       # Database connection management
│   ├── requirements.txt       # Python dependencies
│   └── config.py             # Application configuration
├── frontend/
│   ├── public/
│   │   └── index.html        # Main HTML template
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js   # Main dashboard component
│   │   │   ├── ScanForm.js    # Scan configuration interface
│   │   │   ├── ResultsTable.js # Results visualization
│   │   │   └── Login.js       # Authentication component
│   │   ├── services/
│   │   │   └── api.js         # API service layer
│   │   ├── App.js            # Root React component
│   │   ├── App.css           # Application styling
│   │   └── index.js          # Application entry point
│   └── package.json          # Node.js dependencies
├── database/
│   └── schema.sql            # Database schema definitions
├── docker/
│   ├── Dockerfile            # Docker container configuration
│   └── docker-compose.yml    # Multi-container orchestration
└── docs/
    ├── README.md             # This file
    └── API_DOCS.md           # API documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ and npm installed  
- Git for version control

### 1. Clone the Repository
```bash
git clone https://github.com/SyedhyperX/VulnScan-Pro.git
cd VulnScan-Pro
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python -c "from utils.database import init_db; init_db()"

# Start Flask development server
python app.py
```

The backend API will be available at `http://localhost:5000`

### 3. Frontend Setup
```bash
# Open new terminal and navigate to frontend
cd frontend

# Install Node.js dependencies
npm install

# Start React development server
npm start
```

The frontend application will be available at `http://localhost:3000`

### 4. Access the Application
1. Open your browser and navigate to `http://localhost:3000`
2. Register a new account or login with existing credentials
3. Start your first security scan from the dashboard

## 💻 Usage Guide

### Authentication
1. **Register**: Create a new account with username, email, and password
2. **Login**: Authenticate using your credentials to receive a JWT token
3. **Dashboard Access**: Access all features through the secure dashboard

### Running Security Scans

#### Basic Scan
- **Target**: Enter domain name or IP address (e.g., `example.com` or `192.168.1.1`)
- **Scan Type**: Choose from Basic, Comprehensive, Port-only, or Web-only
- **Execution**: Click "Start Scan" and monitor progress in real-time

#### Scan Types Available
- **Basic Scan**: Quick assessment covering common ports and basic web vulnerabilities
- **Comprehensive Scan**: In-depth analysis including advanced port scanning and web security testing
- **Port Scan Only**: Focus on network ports and services discovery
- **Web Vulnerabilities Only**: Web application security assessment

### Analyzing Results
- **Dashboard Overview**: View scan statistics and recent activity
- **Detailed Results**: Click on any scan to view comprehensive vulnerability details
- **Severity Classification**: Vulnerabilities are classified as High, Medium, or Low severity
- **Export Reports**: Download scan results in JSON, HTML, or CSV format

## 🔧 API Documentation

### Authentication Endpoints
```http
POST /api/register
POST /api/login
```

### Scanning Endpoints  
```http
POST /api/scan          # Start new security scan
GET  /api/scans         # List all user scans  
GET  /api/scan/{id}     # Get specific scan details
```

### Dashboard Endpoints
```http
GET /api/dashboard/stats # Get dashboard statistics
```

All API endpoints require JWT authentication via `Authorization: Bearer <token>` header.

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build
```bash
# Build backend container
docker build -t vulnscan-backend ./backend

# Build frontend container  
docker build -t vulnscan-frontend ./frontend

# Run containers
docker run -d -p 5000:5000 vulnscan-backend
docker run -d -p 3000:3000 vulnscan-frontend
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
python -m pytest tests/
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 🔒 Security Considerations

### Ethical Usage
- **Permission Required**: Only scan systems you own or have explicit written permission to test
- **Legal Compliance**: Ensure compliance with local laws and regulations
- **Responsible Disclosure**: Report discovered vulnerabilities through proper channels

### Security Features
- **Input Validation**: All inputs are validated and sanitized
- **Rate Limiting**: API endpoints implement rate limiting to prevent abuse
- **Secure Authentication**: Passwords are hashed using bcrypt with salt
- **JWT Security**: Tokens include expiration and are cryptographically signed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For support, email [your-email@example.com] or create an issue on GitHub.

## 🚨 Disclaimer

This tool is intended for educational purposes and authorized security testing only. Users are responsible for ensuring they have proper authorization before scanning any systems. The developers are not responsible for any misuse of this tool.

---

**Built with ❤️ by [SyedhyperX](https://github.com/SyedhyperX)**

*Professional Security Scanner for Modern Cybersecurity Needs*
