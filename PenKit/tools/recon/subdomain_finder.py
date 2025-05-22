import argparse
import dns.resolver

def main():
    parser = argparse.ArgumentParser(description="Subdomain Finder (DNS brute force)")
    parser.add_argument('domain', help="Target domain (e.g. example.com)")
    parser.add_argument('-w', '--wordlist', required=True, help="Wordlist file for subdomains")
    parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads (default 10)")
    args = parser.parse_args()

    # Read wordlist
    with open(args.wordlist) as f:
        words = [line.strip() for line in f if line.strip() and not line.startswith('#')]

    from concurrent.futures import ThreadPoolExecutor

    found = []

    def check_subdomain(sub):
        fqdn = f"{sub}.{args.domain}"
        try:
            dns.resolver.resolve(fqdn, 'A')
            print(f"[+] Found: {fqdn}")
            found.append(fqdn)
        except Exception:
            pass  # Not found

    print(f"[*] Scanning {len(words)} potential subdomains on {args.domain} with {args.threads} threads...")
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        executor.map(check_subdomain, words)

    print(f"\n[!] Done. {len(found)} subdomains found.")

if __name__ == "__main__":
    main()