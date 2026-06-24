## ⚡ Install in One Command

curl -fsSL https://raw.githubusercontent.com/HARSHITRAJPUT81/logsense/main/install.sh | bash

That's it! The installer handles everything automatically.

---
# 🔍 LogSense AI

> An AI-powered Linux log analyzer CLI that automatically detects errors, crashes, and anomalies in log files and provides intelligent root-cause analysis with suggested fixes.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![AI](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)
![Platform](https://img.shields.io/badge/Platform-Linux-yellow)

---

## 🚀 Install in 3 Steps

```bash
# Step 1 - Clone
git clone https://github.com/HARSHITRAJPUT81/logsense.git
cd logsense

# Step 2 - Run installer (handles everything)
bash install.sh

# Step 3 - Analyze your system!
sudo logsense analyze /var/log/syslog
```

> 💡 You only need a **free Groq API key** from https://console.groq.com — the installer will ask for it automatically.

---

## 🛠️ Commands

| Command | What it does |
|---|---|
| `logsense analyze /var/log/syslog` | Scan a log file for issues |
| `logsense analyze /var/log/syslog --min-severity 80` | Show only errors and above |
| `logsense watch /var/log/syslog` | Monitor logs live in real time |
| `logsense report` | View history of past analyses |

---

## 📊 Example Output
Flagged lines in syslog
---

## 🔧 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Typer | CLI framework |
| Rich | Beautiful terminal UI |
| Groq + LLaMA | Free AI inference |
| SQLite | Local history storage |

---

## 🗺️ Roadmap

- [ ] Filter logs by time range (`--since 1h`)
- [ ] Support JSON structured logs
- [ ] Slack/Discord notifications
- [ ] Natural language search
- [ ] Export reports to PDF

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

## 👨‍💻 Author

**Harshit** — built as a portfolio project combining Linux + AI.

> ⭐ Star this repo if you found it useful!
## 👨‍💻 Author

**Harshit Rajput**

