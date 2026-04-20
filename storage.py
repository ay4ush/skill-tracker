import json
import os

class StorageHandler:
    def __init__(self, filepath="skills.json"):
        self.filepath = filepath

    def load_data(self):
        if not os.path.exists(self.filepath):
            return {}
        try:
            with open(self.filepath, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def save_data(self, data):
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)
