"""Security utilities for LogSense AI."""
import os
from pathlib import Path
from typing import Optional


# Maximum log file size allowed (50MB)
MAX_FILE_SIZE_MB = 50
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Allowed log directories - only real log paths
ALLOWED_DIRECTORIES = [
    "/var/log",
    "/tmp",
    str(Path.home()),
]


def validate_log_path(file_path: Path) -> tuple[bool, Optional[str]]:
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

        # Check file is in an allowed directory
        allowed = any(
            str(resolved).startswith(allowed_dir)
            for allowed_dir in ALLOWED_DIRECTORIES
        )
        if not allowed:
            return False, (
                f"Access denied: {resolved}\n"
                f"Allowed directories: {', '.join(ALLOWED_DIRECTORIES)}"
            )

        return True, None

    except PermissionError:
        return False, f"Permission denied: {file_path}"
    except Exception as e:
        return False, f"Invalid path: {e}"


def sanitize_log_line(line: str) -> str:
    """Remove potentially dangerous characters from log lines before sending to AI."""
    # Limit line length to prevent prompt injection attacks
    line = line[:500]
    # Remove null bytes
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
    # Mask passwords in logs like "password=secret123"
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
