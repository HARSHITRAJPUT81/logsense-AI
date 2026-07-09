"""Security utilities for LogSense AI."""
import os
import platform
from pathlib import Path
from typing import Optional

MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def _get_allowed_directories():
    system = platform.system()
    if system == "Windows":
        return [
            "C:\\Windows\\System32\\winevt\\Logs",
            "C:\\Windows\\Logs",
            "C:\\Users",
            str(Path.home()),
        ]
    elif system == "Darwin":
        return [
            "/var/log",
            "/tmp",
            "/Library/Logs",
            str(Path.home()),
        ]
    else:
        return [
            "/var/log",
            "/tmp",
            str(Path.home()),
        ]

def validate_log_path(file_path: Path) -> tuple:
    try:
        resolved = file_path.resolve()
        if not resolved.exists():
            return False, f"File not found: {file_path}"
        if not resolved.is_file():
            return False, f"Path is not a file: {file_path}"
        size = resolved.stat().st_size
        if size > MAX_FILE_SIZE_BYTES:
            return False, f"File too large ({size // 1024 // 1024}MB). Max: {MAX_FILE_SIZE_MB}MB"
        allowed_directories = _get_allowed_directories()
        allowed = any(
            str(resolved).lower().startswith(allowed_dir.lower())
            for allowed_dir in allowed_directories
        )
        if not allowed:
            return False, (
                f"Access denied: {resolved}\n"
                f"Allowed directories: {', '.join(allowed_directories)}"
            )
        return True, None
    except PermissionError:
        return False, f"Permission denied: {file_path}"
    except Exception as e:
        return False, f"Invalid path: {e}"

def sanitize_log_line(line: str) -> str:
    line = line[:500]
    line = line.replace("\x00", "")
    return line

def mask_sensitive_data(text: str) -> str:
    import re
    text = re.sub(
        r'\b(\d{1,3})\.\d{1,3}\.\d{1,3}\.(\d{1,3})\b',
        r'\1.xxx.xxx.\2', text
    )
    text = re.sub(
        r'(password|passwd|secret|token|key|api_key)=[^\s&]+',
        r'\1=***MASKED***', text, flags=re.IGNORECASE
    )
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '***@***.***', text
    )
    return text
