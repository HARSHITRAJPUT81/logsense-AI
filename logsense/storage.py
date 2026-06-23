import sqlite3
from datetime import datetime
from typing import List, Tuple
from .config import DB_PATH, ensure_db_dir

def init_db() -> sqlite3.Connection:
    ensure_db_dir()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, timestamp TEXT, severity TEXT,
            root_cause TEXT, suggested_fix TEXT, summary TEXT, raw_excerpt TEXT
        )
    """)
    conn.commit()
    return conn

def save_event(source: str, analysis: dict, raw_excerpt: str) -> None:
    conn = init_db()
    conn.execute(
        "INSERT INTO events (source,timestamp,severity,root_cause,suggested_fix,summary,raw_excerpt) VALUES (?,?,?,?,?,?,?)",
        (source, datetime.now().isoformat(), analysis.get("severity","unknown"),
         analysis.get("root_cause",""), analysis.get("suggested_fix",""),
         analysis.get("summary",""), raw_excerpt[:2000]),
    )
    conn.commit()
    conn.close()

def get_recent_events(limit: int = 20) -> List[Tuple]:
    conn = init_db()
    cur = conn.execute(
        "SELECT timestamp, source, severity, summary FROM events ORDER BY id DESC LIMIT ?", (limit,)
    )
    rows = cur.fetchall()
    conn.close()
    return rows
