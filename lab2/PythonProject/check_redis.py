"""Small helper to show Redis list contents used by Lab4."""
import json
import sys

try:
    import redis
except ImportError:
    print("Please install redis: pip install redis")
    sys.exit(1)

KEY = "lab4:fire-prevention-inspections"

if len(sys.argv) > 1:
    KEY = sys.argv[1]

r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
items = r.lrange(KEY, 0, -1)
print(f"Found {len(items)} items in Redis key '{KEY}'")
for i, s in enumerate(items[:10], start=1):
    try:
        obj = json.loads(s)
    except Exception:
        obj = s
    print(i, obj)

