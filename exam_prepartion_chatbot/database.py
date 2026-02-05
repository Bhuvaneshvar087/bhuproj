import json
import os

PERF_FILE = "data/performance.json"

def load_performance():
    if not os.path.exists(PERF_FILE):
        return {}
    with open(PERF_FILE, "r") as f:
        return json.load(f)

def save_performance(data):
    with open(PERF_FILE, "w") as f:
        json.dump(data, f, indent=4)
