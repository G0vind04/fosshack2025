import json
import os

CONFIG_FILE = 'peers.json'

def load_peers():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_peers(peers):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(peers, f)