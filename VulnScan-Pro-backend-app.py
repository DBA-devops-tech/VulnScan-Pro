from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime, timedelta
import threading
from scanner.port_scanner import PortScanner
from scanner.web_scanner import WebScanner
from scanner.report_generator import ReportGenerator
from utils.database import init_db, get_db_connection
import json

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'vulnscan-pro-secret-key-change-in-production'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

CORS(app)
jwt = JWTManager(app)

# Initialize database
init_db()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if user already exists
    cursor.execute('SELECT id FROM users WHERE username = ? OR email = ?', (username, email))
    if cursor.fetchone():
        return jsonify({'message': 'User already exists'}), 400

    # Create new user
    hashed_password = generate_password_hash(password)
    cursor.execute(
        'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
        (username, email, hashed_password)
    )
    conn.commit()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, password_hash FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password):
        access_token = create_access_token(identity=user['id'])
        return jsonify({'access_token': access_token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/api/scan', methods=['POST'])
@jwt_required()
def start_scan():
    user_id = get_jwt_identity()
    data = request.get_json()

    target = data.get('target')
    scan_type = data.get('scan_type', 'basic')

    if not target:
        return jsonify({'message': 'Target is required'}), 400

    # Create scan record
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO scans (user_id, target, scan_type, status) VALUES (?, ?, ?, ?)',
        (user_id, target, scan_type, 'running')
    )
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Start scan in background thread
    def run_scan():
        try:
            scanner = WebScanner()
            port_scanner = PortScanner()

            # Perform scans based on type
            results = {}
            if scan_type in ['basic', 'comprehensive']:
                results['port_scan'] = port_scanner.scan_ports(target)
                results['web_scan'] = scanner.scan_website(target)

            # Update scan results
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE scans SET results = ?, status = ?, completed_at = ? WHERE id = ?',
                (json.dumps(results), 'completed', datetime.now(), scan_id)
            )
            conn.commit()
            conn.close()

        except Exception as e:
            # Update scan with error
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE scans SET status = ?, error = ? WHERE id = ?',
                ('failed', str(e), scan_id)
            )
            conn.commit()
            conn.close()

    thread = threading.Thread(target=run_scan)
    thread.daemon = True
    thread.start()

    return jsonify({'scan_id': scan_id, 'message': 'Scan started'}), 200

@app.route('/api/scans', methods=['GET'])
@jwt_required()
def get_scans():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM scans WHERE user_id = ? ORDER BY created_at DESC',
        (user_id,)
    )
    scans = cursor.fetchall()
    conn.close()

    return jsonify([dict(scan) for scan in scans])

@app.route('/api/scan/<int:scan_id>', methods=['GET'])
@jwt_required()
def get_scan_details(scan_id):
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM scans WHERE id = ? AND user_id = ?',
        (scan_id, user_id)
    )
    scan = cursor.fetchone()
    conn.close()

    if not scan:
        return jsonify({'message': 'Scan not found'}), 404

    scan_dict = dict(scan)
    if scan_dict['results']:
        scan_dict['results'] = json.loads(scan_dict['results'])

    return jsonify(scan_dict)

@app.route('/api/dashboard/stats', methods=['GET'])
@jwt_required()
def get_dashboard_stats():
    user_id = get_jwt_identity()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Get total scans
    cursor.execute('SELECT COUNT(*) as total FROM scans WHERE user_id = ?', (user_id,))
    total_scans = cursor.fetchone()['total']

    # Get recent scans
    cursor.execute(
        'SELECT COUNT(*) as recent FROM scans WHERE user_id = ? AND created_at > ?',
        (user_id, datetime.now() - timedelta(days=7))
    )
    recent_scans = cursor.fetchone()['recent']

    # Get vulnerabilities found (mock data for demo)
    cursor.execute(
        'SELECT COUNT(*) as completed FROM scans WHERE user_id = ? AND status = "completed"',
        (user_id,)
    )
    completed_scans = cursor.fetchone()['completed']

    conn.close()

    return jsonify({
        'total_scans': total_scans,
        'recent_scans': recent_scans,
        'completed_scans': completed_scans,
        'vulnerabilities_found': completed_scans * 3  # Mock calculation
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
