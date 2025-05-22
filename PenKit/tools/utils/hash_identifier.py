import argparse
import re

HASH_TYPES = [
    # (name, regex pattern, length)
    ("MD5", r"^[a-fA-F0-9]{32}$", 32),
    ("SHA1", r"^[a-fA-F0-9]{40}$", 40),
    ("SHA224", r"^[a-fA-F0-9]{56}$", 56),
    ("SHA256", r"^[a-fA-F0-9]{64}$", 64),
    ("SHA384", r"^[a-fA-F0-9]{96}$", 96),
    ("SHA512", r"^[a-fA-F0-9]{128}$", 128),
    ("NTLM", r"^[a-fA-F0-9]{32}$", 32),
    ("LM", r"^[a-fA-F0-9]{32}$", 32),
    ("bcrypt", r"^\$2[abxy]?\$\d{2}\$[./A-Za-z0-9]{53}$", 60),
    ("DES (crypt)", r"^[./A-Za-z0-9]{13}$", 13),
    ("MySQL v3", r"^[a-fA-F0-9]{16}$", 16),
    ("MySQL v4+", r"^\*[a-fA-F0-9]{40}$", 41),
    ("Cisco Type 7", r"^[0-9A-F]{16}$", 16),
    ("CRC32", r"^[a-fA-F0-9]{8}$", 8),
    ("SHA3-224", r"^[a-fA-F0-9]{56}$", 56),
    ("SHA3-256", r"^[a-fA-F0-9]{64}$", 64),
    ("SHA3-384", r"^[a-fA-F0-9]{96}$", 96),
    ("SHA3-512", r"^[a-fA-F0-9]{128}$", 128),
    ("RIPEMD-160", r"^[a-fA-F0-9]{40}$", 40),
    ("Ethereum address", r"^0x[a-fA-F0-9]{40}$", 42),
]

def identify_hash(hash_string):
    results = []
    for name, pattern, length in HASH_TYPES:
        if re.match(pattern, hash_string) and len(hash_string) == length:
            results.append(name)
    return results

def main():
    parser = argparse.ArgumentParser(description="Hash Identifier")
    parser.add_argument('hash_string', help="Hash string to identify")
    args = parser.parse_args()

    hash_input = args.hash_string.strip()
    results = identify_hash(hash_input)

    if results:
        print(f"[*] Possible hash types for '{hash_input}':")
        for r in results:
            print(f"  - {r}")
    else:
        print(f"[!] Could not identify hash type for: {hash_input}")

if __name__ == "__main__":
    main()