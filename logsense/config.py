import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("LOGSENSE_MODEL", "claude-sonnet-4-6")
DB_PATH = Path(os.getenv("LOGSENSE_DB", str(Path.home() / ".logsense" / "history.db")))

def ensure_db_dir() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
