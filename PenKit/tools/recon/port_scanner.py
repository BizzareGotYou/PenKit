import argparse
import socket
import sys

def parse_ports(port_str):
    """Parse a port range like '20-80' or a list like '22,80,443'."""
    ports = set()
    if '-' in port_str:
        start, end = map(int, port_str.split('-'))
        ports.update(range(start, end + 1))
    else:
        ports.update(int(p.strip()) for p in port_str.split(','))
    return sorted(ports)

def scan_port(host, port, timeout=1.0):
    """Return True if port is open on host."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((host, port))
            return result == 0
    except Exception:
        return False

def main():
    parser = argparse.ArgumentParser(description="Port Scanner")
    parser.add_argument('target', help="Target host/IP")
    parser.add_argument('-p', '--ports', default="1-1024", help="Port range (e.g. 1-1024 or 22,80,443)")
    parser.add_argument('-t', '--timeout', type=float, default=0.5, help="Connection timeout (seconds)")
    args = parser.parse_args()

    if len(sys.argv) == 1: 
        parser.print_help()
        sys.exit(1)

    try:
        target_ip = socket.gethostbyname(args.target)
    except Exception as e:
        print(f"[!] Could not resolve {args.target}: {e}")
        return

    ports = parse_ports(args.ports)
    print(f"[*] Scanning {args.target} ({target_ip}) on ports: {args.ports}")

    for port in ports:
        if scan_port(target_ip, port, args.timeout):
            print(f"[+] Port {port} is OPEN")

if __name__ == "__main__":
    main()