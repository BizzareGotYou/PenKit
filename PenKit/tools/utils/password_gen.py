import argparse
import random
import string

def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    charset = ""
    if use_upper:
        charset += string.ascii_uppercase
    if use_lower:
        charset += string.ascii_lowercase
    if use_digits:
        charset += string.digits
    if use_symbols:
        charset += string.punctuation

    if not charset:
        raise ValueError("At least one character set must be enabled!")

    return ''.join(random.choice(charset) for _ in range(length))

def main():
    parser = argparse.ArgumentParser(description="Password Generator")
    parser.add_argument('-l', '--length', type=int, default=16, help="Password length (default: 16)")
    parser.add_argument('-n', '--number', type=int, default=1, help="Number of passwords to generate (default: 1)")
    parser.add_argument('--no-upper', action='store_true', help="Exclude uppercase letters")
    parser.add_argument('--no-lower', action='store_true', help="Exclude lowercase letters")
    parser.add_argument('--no-digits', action='store_true', help="Exclude digits")
    parser.add_argument('--no-symbols', action='store_true', help="Exclude symbols")
    args = parser.parse_args()

    use_upper = not args.no_upper
    use_lower = not args.no_lower
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols

    for i in range(args.number):
        pwd = generate_password(args.length, use_upper, use_lower, use_digits, use_symbols)
        print(pwd)

if __name__ == "__main__":
    main()