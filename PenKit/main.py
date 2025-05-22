import subprocess
import sys
import os

TOOLS = {
    "Recon": {
        "Subdomain Finder": "tools/recon/subdomain_finder.py",
        "Port Scanner": "tools/recon/port_scanner.py"
    },
    "Web Enumeration": {
        "Directory Brute Forcer": "tools/web_enum/dir_bruteforce.py",
        "HTTP Info Tool": "tools/web_enum/http_info.py"
    },
    "Vulnerability Scanners": {
        "Login Bruteforcer": "tools/vuln/login_bruteforce.py",
        "XSS Scanner": "tools/vuln/xss_scanner.py"
    },
    "Utilities": {
        "Hash Identifier": "tools/utils/hash_identifier.py",
        "Password Generator": "tools/utils/password_gen.py"
    }
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_menu():
    clear()
    print("==== PenTester CLI ====\n")
    idx = 1
    tool_map = {}
    for category, tools in TOOLS.items():
        print(f"{category}:")
        for name, path in tools.items():
            print(f"  [{idx}] {name}")
            tool_map[str(idx)] = path
            idx += 1
    print(f"  [0] Exit\n")
    return tool_map

def main():
    while True:
        tool_map = print_menu()
        choice = input("Select a tool by number: ").strip()
        if choice == '0':
            print("Exiting. Happy hacking!")
            break
        elif choice in tool_map:
            script_path = tool_map[choice]
            if not os.path.isfile(script_path):
                print(f"[!] Script not found: {script_path}")
                input("Press Enter to continue...")
                continue
            try:
                subprocess.run([sys.executable, script_path])
            except Exception as e:
                print(f"[!] Error: {e}")
            input("\nPress Enter to return to the menu...")
        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")

if __name__ == '__main__':
    main()