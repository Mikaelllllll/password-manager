import os
import json

RECENT_PATH = 'recent_files.json'

def load_recent_files():
    if os.path.exists(RECENT_PATH):
        with open(RECENT_PATH, 'r') as f:
            return json.load(f)
    return {"keys": [], "passwords": []}

def save_recent_file(file_type, path):
    recent = load_recent_files()
    if path not in recent[file_type]:
        recent[file_type].insert(0, path)
        recent[file_type] = recent[file_type][:5]  # Keep max 5 recent
    with open(RECENT_PATH, 'w') as f:
        json.dump(recent, f)
        