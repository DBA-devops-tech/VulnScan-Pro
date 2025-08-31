import requests
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime
import ssl
import socket

class WebScanner:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'VulnScan-Pro/1.0 Security Scanner'
        })

    def scan_website(self, target):
        """Comprehensive web vulnerability scan"""
        if not target.startswith(('http://', 'https://')):
            target = f'http://{target}'

        results = {
            'target': target,
            'scan_type': 'web_scan',
            'start_time': datetime.now().isoformat(),
            'vulnerabilities': [],
            'security_headers': {},
            'ssl_info': {},
            'server_info': {}
        }

        try:
            # Basic HTTP request
            response = self.session.get(target, timeout=10, verify=False)
            results['status_code'] = response.status_code
            results['server_info'] = dict(response.headers)

            # Check security headers
            results['security_headers'] = self.check_security_headers(response.headers)

            # Check for common vulnerabilities
            results['vulnerabilities'].extend(self.check_common_vulnerabilities(target, response))

            # SSL/TLS check for HTTPS sites
            if target.startswith('https://'):
                results['ssl_info'] = self.check_ssl_security(target)

            # Check for information disclosure
            results['vulnerabilities'].extend(self.check_information_disclosure(response))

        except Exception as e:
            results['error'] = str(e)

        results['end_time'] = datetime.now().isoformat()
        return results

    def check_security_headers(self, headers):
        """Check for important security headers"""
        security_headers = {
            'X-Frame-Options': headers.get('X-Frame-Options', 'Missing'),
            'X-Content-Type-Options': headers.get('X-Content-Type-Options', 'Missing'),
            'X-XSS-Protection': headers.get('X-XSS-Protection', 'Missing'),
            'Strict-Transport-Security': headers.get('Strict-Transport-Security', 'Missing'),
            'Content-Security-Policy': headers.get('Content-Security-Policy', 'Missing'),
            'Referrer-Policy': headers.get('Referrer-Policy', 'Missing')
        }
        return security_headers

    def check_common_vulnerabilities(self, target, response):
        """Check for common web vulnerabilities"""
        vulnerabilities = []

        # Check for directory listing
        if 'Index of /' in response.text or 'Directory Listing' in response.text:
            vulnerabilities.append({
                'type': 'Directory Listing Enabled',
                'severity': 'Medium',
                'description': 'Directory listing is enabled, which may expose sensitive files'
            })

        # Check for server information disclosure
        server_header = response.headers.get('Server', '').lower()
        if 'apache' in server_header and '/' in server_header:
            vulnerabilities.append({
                'type': 'Server Version Disclosure',
                'severity': 'Low',
                'description': f'Server version disclosed: {response.headers.get("Server")}'
            })

        # Check for missing security headers
        if not response.headers.get('X-Frame-Options'):
            vulnerabilities.append({
                'type': 'Missing X-Frame-Options Header',
                'severity': 'Medium',
                'description': 'X-Frame-Options header is missing, site may be vulnerable to clickjacking'
            })

        if not response.headers.get('Content-Security-Policy'):
            vulnerabilities.append({
                'type': 'Missing Content Security Policy',
                'severity': 'Medium',
                'description': 'CSP header is missing, site may be vulnerable to XSS attacks'
            })

        # Check for HTTP methods
        try:
            options_response = self.session.options(target)
            allowed_methods = options_response.headers.get('Allow', '')
            if 'TRACE' in allowed_methods.upper():
                vulnerabilities.append({
                    'type': 'HTTP TRACE Method Enabled',
                    'severity': 'Low',
                    'description': 'TRACE method is enabled, may lead to Cross-Site Tracing attacks'
                })
        except:
            pass

        return vulnerabilities

    def check_ssl_security(self, target):
        """Check SSL/TLS configuration"""
        try:
            hostname = urlparse(target).hostname
            context = ssl.create_default_context()

            with socket.create_connection((hostname, 443)) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()

                    return {
                        'protocol': ssock.version(),
                        'cipher': cipher[0] if cipher else 'Unknown',
                        'certificate_subject': dict(x[0] for x in cert['subject']),
                        'certificate_issuer': dict(x[0] for x in cert['issuer']),
                        'not_after': cert['notAfter'],
                        'not_before': cert['notBefore']
                    }
        except Exception as e:
            return {'error': str(e)}

    def check_information_disclosure(self, response):
        """Check for information disclosure vulnerabilities"""
        vulnerabilities = []

        # Check for sensitive comments in HTML
        html_comments = re.findall(r'<!--.*?-->', response.text, re.DOTALL)
        for comment in html_comments:
            if any(keyword in comment.lower() for keyword in ['password', 'admin', 'debug', 'todo', 'fixme']):
                vulnerabilities.append({
                    'type': 'Sensitive Information in HTML Comments',
                    'severity': 'Low',
                    'description': 'HTML comments contain potentially sensitive information'
                })
                break

        # Check for error messages
        error_patterns = [
            r'mysql_.*error',
            r'warning.*mysql_',
            r'postgresql.*error',
            r'ora-\d+',
            r'microsoft.*odbc.*sql',
            r'sqlite.*error'
        ]

        for pattern in error_patterns:
            if re.search(pattern, response.text, re.IGNORECASE):
                vulnerabilities.append({
                    'type': 'Database Error Message Disclosure',
                    'severity': 'Medium',
                    'description': 'Database error messages detected, may reveal system information'
                })
                break

        return vulnerabilities
