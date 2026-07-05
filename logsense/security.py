"""Security utilities for LogSense AI."""
import os
import platform
from pathlib import Path
from typing import Optional

# Maximum log file size allowed (50MB)
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

def _get_allowed_directories():
    """Return allowed directories based on current OS."""
    system = platform.system()

    if system == "Windows":
        return [
            "C:\\Windows\\System32\\winevt\\Logs",
            "C:\\Windows\\Logs",
            "C:\\Users",
            str(Path.home()),
        ]
    elif system == "Darwin":  # macOS
        return [
            "/var/log",
            "/tmp",
            "/Library/Logs",
            str(Path.home()),
        ]
    else:  # Linux
        return [
            "/var/log",
            "/tmp",
            str(Path.home()),
        ]

def validate_log_path(file_path: Path) -> tuple:
    """
    Validate that a log file path is safe to read.
    Returns (is_safe, error_message)
    """
    try:
        # Resolve to absolute path (prevents path traversal like ../../etc/passwd)
        resolved = file_path.resolve()

        # Check file exists
        if not resolved.exists():
            return False, f"File not found: {file_path}"

        # Check it's actually a file not a directory
        if not resolved.is_file():
            return False, f"Path is not a file: {file_path}"

        # Check file size
        size = resolved.stat().st_size
        if size > MAX_FILE_SIZE_BYTES:
            return False, f"File too large ({size // 1024 // 1024}MB). Max allowed: {MAX_FILE_SIZE_MB}MB"

        # Get allowed directories for current OS
        allowed_directories = _get_allowed_directories()

        # Check file is in an allowed directory
        allowed = any(
            str(resolved).startswith(allowed_dir)
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
    """Remove potentially dangerous characters from log lines."""
    line = line[:500]
    line = line.replace("\x00", "")
    return line


def mask_sensitive_data(text: str) -> str:
    """Mask common sensitive patterns in log lines before sending to AI."""
    import re

    # Mask IP addresses partially
    text = re.sub(
        r'\b(\d{1,3})\.\d{1,3}\.\d{1,3}\.(\d{1,3})\b',
        r'\1.xxx.xxx.\2',
        text
    )
    # Mask passwords in logs
    text = re.sub(
        r'(password|passwd|secret|token|key|api_key)=[^\s&]+',
        r'\1=***MASKED***',
        text,
        flags=re.IGNORECASE
    )
    # Mask email addresses
    text = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        '***@***.***',
        text
    )
    return text
