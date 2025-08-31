import socket
import threading
from datetime import datetime
import nmap

class PortScanner:
    def __init__(self):
        self.open_ports = []
        self.closed_ports = []

    def scan_port(self, target, port, timeout=3):
        """Scan a single port on target"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target, port))
            sock.close()

            if result == 0:
                self.open_ports.append(port)
                return True
            else:
                self.closed_ports.append(port)
                return False
        except:
            return False

    def scan_ports(self, target, port_range=(1, 1000)):
        """Scan multiple ports on target"""
        print(f"Starting port scan on {target}...")
        start_time = datetime.now()

        # Common ports to scan
        common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080]

        results = {
            'target': target,
            'scan_type': 'port_scan',
            'start_time': start_time.isoformat(),
            'open_ports': [],
            'services': {},
            'vulnerabilities': []
        }

        # Use threading for faster scanning
        threads = []
        for port in common_ports:
            t = threading.Thread(target=self.scan_port, args=(target, port))
            t.start()
            threads.append(t)

        # Wait for all threads to complete
        for t in threads:
            t.join()

        results['open_ports'] = self.open_ports.copy()

        # Identify services on open ports
        service_map = {
            21: 'FTP',
            22: 'SSH', 
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            135: 'RPC',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            1723: 'PPTP',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            5900: 'VNC',
            8080: 'HTTP-Alt'
        }

        for port in self.open_ports:
            if port in service_map:
                results['services'][port] = service_map[port]

                # Add potential vulnerabilities based on open services
                if port == 21:
                    results['vulnerabilities'].append({
                        'type': 'FTP Service Detected',
                        'severity': 'Medium',
                        'port': port,
                        'description': 'FTP service may be vulnerable to brute force attacks'
                    })
                elif port == 23:
                    results['vulnerabilities'].append({
                        'type': 'Telnet Service Detected',
                        'severity': 'High',
                        'port': port,
                        'description': 'Telnet transmits data in plaintext and is highly insecure'
                    })
                elif port == 3389:
                    results['vulnerabilities'].append({
                        'type': 'RDP Service Detected',
                        'severity': 'Medium',
                        'port': port,
                        'description': 'RDP may be vulnerable to brute force and exploitation attacks'
                    })

        end_time = datetime.now()
        results['end_time'] = end_time.isoformat()
        results['duration'] = str(end_time - start_time)

        # Reset for next scan
        self.open_ports = []
        self.closed_ports = []

        return results

    def advanced_scan(self, target):
        """Advanced scan using nmap (if available)"""
        try:
            nm = nmap.PortScanner()
            results = nm.scan(target, '22-443')
            return results
        except:
            # Fallback to basic scan if nmap not available
            return self.scan_ports(target)
