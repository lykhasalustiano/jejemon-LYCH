import os
import json
from datetime import datetime

HISTORY_FILE = 'history.json'

def save_translation(original, normalized):
    history = load_history()
    history.append({
        'timestamp': current_time(),
        'original': original,
        'normalized': normalized
    })
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        return json.load(f)

def current_time():
    return datetime.now().isoformat()
