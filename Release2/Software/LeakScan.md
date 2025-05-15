# LeakScan – Lightweight Secret & Pattern Scanner

[![Version](https://img.shields.io/badge/version-1.0-blue.svg)](https://github.com/yourrepo)
[![Status](https://img.shields.io/badge/status-active--feedback--wanted-yellow.svg)](https://github.com/yourrepo/issues)

**LeakScan** is a hybrid script combining static secret scanning and custom pattern detection to help prevent accidental exposure of sensitive information in documentation and code files (e.g., `.md`, `.txt`, `.py`, etc.).

It integrates:

- [`detect-secrets`](https://github.com/ibm/detect-secrets) – robust detection of known secret types (tokens, keys, credentials, etc.)
- A custom regex engine – finds potentially dangerous strings like `ssh`, `id_rsa`, `chat_id`, `docker exec`, `crontab`, or command examples referencing sensitive areas
- **Contextual output with color-coded highlights** and severity labels (`LOW`, `MEDIUM`, `HIGH`)

---

## Features

- Auto-installs required dependencies (`detect-secrets`, `colorama`) if missing
- Scans any single file with a one-line command
- Shows **match context** (2 lines before/after) with colored highlights
- Flags risky keywords even if anonymized (useful in pre-publication reviews)

---

## Usage

```bash
python3 leakscan.py yourfile.md
```

The script will:

1. Ensure dependencies are installed
2. Run `detect-secrets scan`
3. Run the custom matcher
4. Print all hits with risk level and line context

---

## Example Output

```text
[HIGH] Match: 'id_rsa' at line 82
  80 | - User: `homeassistant_user`
  81 | - IP: `HOME_ASSISTANT_IP`
  82 | - Key path: `/-redacted-/-redacted-/id_rsa.pub`
```

Each match includes:
- A severity tag (`LOW`, `MEDIUM`, `HIGH`)
- The matched keyword, highlighted in color
- Contextual lines (±2)
- Separation bar for readability

---

## When to Use

- Before pushing documentation/code to public repositories
- During internal audits of automation scripts
- To build checklists for redacting technical content

---

## License

See [`LICENSE.md`](LICENSE.md) for licensing information.

---

## Contributions

Feedback, suggestions and improvements are welcome!  
You can open issues or submit pull requests via GitHub.
