import re
from dataclasses import dataclass
from typing import List, Tuple

SEVERITY_PATTERNS: List[Tuple[int, str, re.Pattern]] = [
    (100, "FATAL",    re.compile(r"\b(panic|segfault|fatal|out of memory|oom[ -]?killer)\b", re.I)),
    (90,  "CRITICAL", re.compile(r"\b(critical|emergency)\b", re.I)),
    (80,  "ERROR",    re.compile(r"\b(error|exception|traceback|failed|failure)\b", re.I)),
    (60,  "NETWORK",  re.compile(r"\b(connection refused|timed? ?out|denied|unreachable|reset by peer)\b", re.I)),
    (40,  "WARNING",  re.compile(r"\b(warn(ing)?|deprecated|retry(ing)?)\b", re.I)),
]

@dataclass
class LogEntry:
    raw: str
    severity: int
    label: str
    line_number: int

def classify_line(line: str) -> Tuple[int, str]:
    for score, label, pattern in SEVERITY_PATTERNS:
        if pattern.search(line):
            return score, label
    return 0, "INFO"

def parse_lines(lines: List[str], start_line: int = 1) -> List[LogEntry]:
    entries = []
    for i, line in enumerate(lines, start=start_line):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        score, label = classify_line(line)
        if score > 0:
            entries.append(LogEntry(raw=line, severity=score, label=label, line_number=i))
    return entries
