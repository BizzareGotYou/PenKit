import argparse
import requests

def scan(base_url, wordlist, extensions=None, codes=None, verbose=False):
    if not base_url.endswith('/'):
        base_url += '/'
    with open(wordlist) as f:
        words = [line.strip() for line in f if line.strip()]
    if extensions:
        ext_list = [x if x.startswith('.') else f".{x}" for x in extensions.split(',')]
    else:
        ext_list = ['']

    # Wildcard/catch-all baseline check
    random_path = base_url + "thisshouldnotexist12345"
    try:
        baseline = requests.get(random_path, allow_redirects=False, timeout=5)
        baseline_status = baseline.status_code
        baseline_location = baseline.headers.get('Location', '')
        baseline_length = len(baseline.text)
        baseline_location_base = baseline_location.rsplit("/", 1)[0] + "/"
        print(f"[*] Wildcard baseline: {baseline_status}, Location: {baseline_location}, Length: {baseline_length}")
    except Exception as e:
        print(f"[!] Error accessing baseline path: {e}")
        return []

    print(f"[*] Starting scan on {base_url} with {len(words)} words and extensions {ext_list}")
    found = []
    for word in words:
        paths = [word] + [word + ext for ext in ext_list if ext]
        for path in paths:
            url = base_url + path
            try:
                resp = requests.get(url, allow_redirects=False, timeout=5)
                location = resp.headers.get('Location', '')
                location_base = location.rsplit("/", 1)[0] + "/" if location else None
                is_wildcard = (
                    resp.status_code == baseline_status and
                    location_base == baseline_location_base and
                    abs(len(resp.text) - baseline_length) < 20
                )
                if is_wildcard:
                    if verbose:
                        print(f"[!] Wildcard match for {url} (Location: {location})")
                    continue
                if resp.status_code in codes:
                    print(f"[+] {resp.status_code} - {url}")
                    found.append((resp.status_code, url))
                elif verbose:
                    print(f"[-] {resp.status_code} - {url}")
            except Exception as e:
                print(f"[!] Error accessing {url}: {e}")
    print(f"[*] Scan complete. {len(found)} hits found.")
    return found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Directory/File Bruteforcer with Wildcard Detection")
    parser.add_argument('url', help="Base URL (e.g. https://target.site/)")
    parser.add_argument('wordlist', help="Wordlist of directories/files")
    parser.add_argument('--ext', help="Comma-separated file extensions to try (e.g. php,txt,zip)")
    parser.add_argument('--codes', default="200,301,302,403", help="Status codes to report (default: 200,301,302,403)")
    parser.add_argument('--verbose', action='store_true', help="Show all requests, not just hits")
    args = parser.parse_args()

    code_list = [int(x.strip()) for x in args.codes.split(',') if x.strip()]
    scan(args.url, args.wordlist, extensions=args.ext, codes=code_list, verbose=args.verbose)