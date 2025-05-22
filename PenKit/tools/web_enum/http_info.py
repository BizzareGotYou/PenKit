import argparse
import requests
import ssl
import sys
from urllib.parse import urlparse
from pprint import pprint

def print_cert_info(cert):
    print("\n[*] SSL Certificate Info:")
    print(f"  Subject: {cert.get('subject')}")
    print(f"  Issuer: {cert.get('issuer')}")
    print(f"  Valid from: {cert.get('notBefore')}")
    print(f"  Valid until: {cert.get('notAfter')}")
    print(f"  Serial Number: {cert.get('serialNumber')}")
    print(f"  Version: {cert.get('version')}")

def get_cert_info(hostname, port=443):
    import socket
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
    return cert

def show_http_info(url, show_body=300, follow_redirects=False):
    try:
        resp = requests.get(url, allow_redirects=follow_redirects, timeout=10)
    except Exception as e:
        print(f"[!] Error: {e}")
        return

    print(f"\n=== {url} ===")
    print(f"Status: {resp.status_code} {resp.reason}")
    print(f"HTTP Version: {resp.raw.version if hasattr(resp.raw, 'version') else 'Unknown'}")
    print(f"URL after redirects: {resp.url}")
    print("\nHeaders:")
    for k, v in resp.headers.items():
        print(f"  {k}: {v}")

    if len(resp.history) > 0:
        print("\nRedirect chain:")
        for r in resp.history:
            print(f"  {r.status_code} -> {r.headers.get('Location')}")

    print("\nBody (first {} bytes):".format(show_body))
    body = resp.text[:show_body]
    print(body)
    if len(resp.text) > show_body:
        print("... [truncated]")

    # SSL Info for HTTPS
    parsed = urlparse(url)
    if parsed.scheme == "https":
        try:
            cert = get_cert_info(parsed.hostname, parsed.port or 443)
            print_cert_info(cert)
        except Exception as e:
            print(f"[!] Could not get certificate info: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HTTP Info Tool - Shows headers, status, and SSL info for a URL.")
    parser.add_argument('url', help="The URL to fetch")
    parser.add_argument('--body', type=int, default=300, help="How many bytes of the body to print")
    parser.add_argument('--follow', action='store_true', help="Follow redirects")
    args = parser.parse_args()

    show_http_info(args.url, show_body=args.body, follow_redirects=args.follow)