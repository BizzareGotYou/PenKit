# PenKit

A collection of penetration testing utilities in Python for web enumeration and reconnaissance.

## Tools

### 1. Directory Brute Forcer (`dir_bruteforce.py`)
Bruteforces directories/files on a target URL using a wordlist.

**Usage:**
```bash
python dir_bruteforce.py <base_url> <wordlist.txt> [--ext php,txt,zip] [--codes 200,301,302,403] [--verbose]
```
Example:
```bash
python dir_bruteforce.py https://target.site/ wordlist.txt --ext php,txt,zip
```

---

### 2. HTTP Info Tool (`http_info.py`)
Fetches and displays HTTP status, headers, SSL info, and a snippet of the response body.

**Usage:**
```bash
python http_info.py <url> [--body N] [--follow]
```
Example:
```bash
python http_info.py https://target.site/ --body 500 --follow
```

---

### 3. Main Launcher (`main.py`)
Interactive menu to run any tool.

**Usage:**
```bash
python main.py
```

---

## Installation

1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Requirements

- Python 3.7+
- See `requirements.txt` for pip packages.

---

## Wordlists

A sample `wordlist.txt` is provided, but you can use your own or get larger lists from [SecLists](https://github.com/danielmiessler/SecLists).

---

## .gitignore

A `.gitignore` is included to prevent committing unnecessary files like `.pyc` and environment files.

---

## Disclaimer

This toolkit is for **educational purposes and authorized testing only**. Do not use against systems without permission.