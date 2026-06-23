import random, sys
from datetime import datetime, timedelta

LINES = [
    "INFO  Starting worker process pid=4821",
    "WARNING  Slow query detected (812ms) on users table",
    "ERROR  Database connection refused: could not connect to server",
    "ERROR  Traceback (most recent call last): psycopg2.OperationalError",
    "CRITICAL  Out of memory: kill process 4821 (worker) score 980",
    "WARNING  Retry attempt 3/5 for upstream service payments-api",
    "ERROR  Connection timed out while contacting auth-service:8443",
    "ERROR  Failed to write to disk: No space left on device",
    "INFO  Health check passed",
]

out = sys.argv[1] if len(sys.argv) > 1 else "sample.log"
start = datetime.now() - timedelta(minutes=30)
with open(out, "w") as f:
    for i in range(200):
        ts = (start + timedelta(seconds=i*9)).strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{ts} {random.choice(LINES)}\n")
print(f"Sample log written to {out}")
