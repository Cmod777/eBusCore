# === BLOCK 1: Import and automatic dependency installation ===
import subprocess
import sys
import os

REQUIRED = ["colorama", "detect-secrets"]

for pkg in REQUIRED:
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        print(f"[+] Installing missing package: {pkg}")
        subprocess.run([sys.executable, "-m", "pip", "install", pkg])

import re
from colorama import Fore, Style, init

init(autoreset=True)

# === BLOCK 2: Custom regex rules by severity ===
RULES = {
    'HIGH': [
        r'\b(id_rsa|PRIVATE\s+KEY)\b',
        r'\b(AI_KEY|SECRET|TOKEN)[\w-]*\b',
        r'\b(?:[A-Za-z0-9_]{20,})\b',  # long random strings
    ],
    'MEDIUM': [
        r'\b(chat_id|bearer|authorization)\b',
        r'\b(ssh|scp|authorized_keys)\b',
        r'\b(crontab|@reboot|nohup)\b',
    ],
    'LOW': [
        r'/home/\w+',
        r'\b(docker\s+exec|ebusctl)\b',
        r'\bchmod\s+\+x\b',
    ]
}

# === BLOCK 3: Highlight match in context ===
def highlight_match(text, match, color):
    start, end = match.span()
    return text[:start] + color + match.group(0) + Style.RESET_ALL + text[end:]

# === BLOCK 4: Custom scan engine ===
def custom_scan(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        for severity, patterns in RULES.items():
            for pattern in patterns:
                for match in re.finditer(pattern, line, re.IGNORECASE):
                    color = {
                        'HIGH': Fore.RED,
                        'MEDIUM': Fore.YELLOW,
                        'LOW': Fore.GREEN
                    }[severity]

                    # Extract context
                    context = lines[max(i-2, 0):min(i+3, len(lines))]
                    context_output = []
                    for j, ctx_line in enumerate(context):
                        idx = i - 2 + j
                        if idx == i:
                            ctx_line = highlight_match(ctx_line.rstrip(), match, color)
                        else:
                            ctx_line = ctx_line.rstrip()
                        context_output.append(f"{idx+1:>4} | {ctx_line}")

                    print(f"\n{color}[{severity}] Match: '{match.group(0)}' at line {i+1}{Style.RESET_ALL}")
                    print('\n'.join(context_output))
                    print("-" * 60)

# === BLOCK 5: Run detect-secrets ===
def run_detect_secrets(path):
    print(f"{Fore.CYAN}[detect-secrets] Running scan on: {path}{Style.RESET_ALL}")
    try:
        result = subprocess.run(["detect-secrets", "scan", path], capture_output=True, text=True)
        print(result.stdout)
    except FileNotFoundError:
        print(f"{Fore.RED}detect-secrets is not installed or not in PATH{Style.RESET_ALL}")

# === BLOCK 6: Entry point ===
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python3 leakscan.py <file_to_scan>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.isfile(filepath):
        print(f"{Fore.RED}File not found: {filepath}{Style.RESET_ALL}")
        sys.exit(1)

    print(f"{Fore.GREEN}[+] Starting LEAKSCAN on {filepath}{Style.RESET_ALL}")

    run_detect_secrets(filepath)
    print(f"{Fore.GREEN}\n[+] Running custom regex scan...{Style.RESET_ALL}")
    custom_scan(filepath)
