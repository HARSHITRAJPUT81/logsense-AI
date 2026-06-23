# 🔍 LogSense AI

> An AI-powered Linux log analyzer CLI that automatically detects errors, crashes, and anomalies in log files and provides intelligent root-cause analysis with suggested fixes.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![AI](https://img.shields.io/badge/AI-Groq%20LLaMA-orange)
![Platform](https://img.shields.io/badge/Platform-Linux-yellow)

---

## 🚀 The Problem It Solves

Anyone running a Linux server knows this pain:
- Something breaks at 2AM
- You `grep -i error /var/log/syslog` through thousands of lines
- You manually try to figure out *what* went wrong and *why*

**LogSense AI automates this entire process.**
It finds the important lines, understands the context, and tells you exactly what happened and what to do next.

---

## ✨ Features

- **Static Analysis** — scan any log file and get a flagged-line table instantly
- **Live Monitoring** — tail log files in real time, auto-trigger AI when issues accumulate
- **AI Root-Cause Analysis** — powered by LLaMA via Groq (free), explains *why* things broke
- **History & Reports** — every analysis saved locally in SQLite for future review
- **Format Agnostic** — works on syslog, nginx, app logs, journalctl exports, anything
- **Works Offline** — pattern-based flagging works even without an API key

---

## 📦 Installation

**Requirements:** Python 3.10+, Linux (or WSL/macOS)

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/logsense.git
cd logsense

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Set up your free API key (get one at https://console.groq.com)
cp .env.example .env
nano .env  # paste your GROQ_API_KEY
```

---

## 🛠️ Usage

**Analyze a log file:**
```bash
logsense analyze /var/log/syslog
```

**Watch a log file live:**
```bash
sudo logsense watch /var/log/nginx/error.log
```

**View analysis history:**
```bash
logsense report
```

**Test with a sample log:**
```bash
python3 generate_sample_log.py sample.log
logsense analyze sample.log
```

---

## 📊 Example Output
Flagged lines in syslog
---

## 🏗️ Project Structure
---

## 🔧 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.10+ | Core language |
| Typer | CLI framework |
| Rich | Terminal UI (tables, colors) |
| Groq + LLaMA | Free AI inference |
| SQLite | Local history storage |
| python-dotenv | Secure config management |

---

## 🗺️ Roadmap

- [ ] Add `--since` flag to filter logs by time range
- [ ] Support structured JSON log formats
- [ ] Slack/Discord notifications for critical events
- [ ] Natural language log search: `logsense search "database errors last night"`
- [ ] Package as a systemd service for always-on monitoring
- [ ] Export reports to PDF/HTML

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

---

## 📄 License

MIT — see [LICENSE](LICENSE)

---

## 👨‍💻 Author

**Harshit** — built as a portfolio project combining Linux systems knowledge with AI.

> ⭐ If you found this useful, please star the repo!
