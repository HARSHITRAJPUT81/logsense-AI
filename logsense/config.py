import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("LOGSENSE_MODEL", "claude-sonnet-4-6")

# Properly expand ~ to full home directory path
_db_path = os.getenv("LOGSENSE_DB", "~/.logsense/history.db")
DB_PATH = Path(_db_path).expanduser().resolve()

def ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
