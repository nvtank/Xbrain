import json
from datetime import datetime

LOG_FILE = "logs/trace.jsonl"


def log_event(data):
    payload = {
        "timestamp": str(datetime.now()),
        **data,
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(payload) + "\n")
