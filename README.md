# 🔍 LogSense AI

> AI-powered log analyzer for Linux, macOS and Windows — detects errors, crashes and anomalies, then explains the root cause and suggests a fix using LLaMA AI.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![AI](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-yellow)

> Built as a portfolio project to solve a real DevOps problem — making Linux log analysis fast and intelligent using AI.

---

## ⚡ Install in One Command

**Linux / macOS:**
```bash
curl -fsSL https://raw.githubusercontent.com/HARSHITRAJPUT81/logsense-AI/main/install.sh | bash
```

**Windows (PowerShell as Administrator):**
```powershell
irm https://raw.githubusercontent.com/HARSHITRAJPUT81/logsense-AI/main/install.ps1 | iex
```

> 💡 You need a free Groq API key from https://console.groq.com — the installer will ask for it automatically. No credit card needed.

---

## 💡 Why LogSense AI?

When something breaks on a Linux, Windows or macOS system, you normally have to manually search through thousands of log lines to find the problem. LogSense AI does this for you automatically — it finds the important lines, sends them to AI, and tells you exactly what went wrong and how to fix it.

---

## 🛠️ Commands

**Linux / macOS:**

| Command | What it does |
|---|---|
| `logsense analyze /var/log/syslog` | Scan system log for all issues |
| `logsense analyze /var/log/syslog --min-severity 80` | Show only errors and above |
| `logsense watch /var/log/syslog` | Monitor logs live in real time |
| `logsense report` | View history of all past analyses |

**Windows:**
```powershell
logsense analyze "$env:SystemRoot\System32\winevt\Logs\System.evtx"
logsense analyze "$env:SystemRoot\System32\winevt\Logs\Application.evtx"
```

---

## 🖥️ Supported Operating Systems

| OS | Install Command |
|---|---|
| Linux | `curl -fsSL .../install.sh \| bash` |
| macOS | `curl -fsSL .../install.sh \| bash` |
| Windows PowerShell | `irm .../install.ps1 \| iex` |

---

## ⚠️ Windows Users — Important Note

When creating your `.env` file on Windows, use this command (not `echo`):
```powershell
"GROQ_API_KEY=gsk_your_key_here" | Out-File -FilePath .env -Encoding utf8
```
Using `echo` on Windows creates a UTF-16 file which breaks Python.

---

## 🔒 Security

- Path traversal attack prevention
- Maximum file size limit 50MB
- Sensitive data masked before sending to AI
- API key stored locally in `.env` file — never shared
- Case-insensitive path validation for Windows

---

## 🏗️ Project Structure

logsense/
├── logsense/
│   ├── cli.py           # Commands: analyze / watch / report
│   ├── log_parser.py    # Detects errors by severity
│   ├── ai_analyzer.py   # Groq + LLaMA AI integration
│   ├── storage.py       # Saves history to SQLite
│   ├── security.py      # Input validation and data masking
│   └── config.py        # Loads environment variables
├── install.sh           # One-command installer Linux/macOS
├── install.ps1          # One-command installer Windows
├── install.bat          # Windows batch installer
├── requirements.txt
└── .env.example


---

## 🔧 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Typer | CLI framework |
| Rich | Terminal UI colors and tables |
| Groq + LLaMA | Free AI inference |
| SQLite | Local history storage |
| python-dotenv | Secure API key management |

---

## 📊 Example Output

Flagged lines in syslog
┏━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Line ┃ Severity ┃ Text                        ┃
┡━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 5    │ FATAL    │ Out of memory: kill process  │
│ 6    │ ERROR    │ Database connection refused  │
│ 11   │ ERROR    │ Connection timed out         │
└──────┴──────────┴─────────────────────────────┘
AI Analysis
Severity   : critical
Root cause : OOM kills and DB connection loss
Fix        : Increase memory, check DB pool


---

## 🗺️ Roadmap

- [ ] Filter logs by time (`--since 1h`)
- [ ] Support JSON structured logs
- [ ] Slack and Discord notifications
- [ ] Natural language log search
- [ ] Export reports to PDF
- [ ] Web version browser based

---

## 📄 License

MIT © 2026 Harshit Rajput

---

## 👨‍💻 Author

**Harshit Rajput**
- GitHub: [@HARSHITRAJPUT81](https://github.com/HARSHITRAJPUT81)
- Project: [github.com/HARSHITRAJPUT81/logsense-AI](https://github.com/HARSHITRAJPUT81/logsense-AI)

> ⭐ Star this repo if you found it useful!

