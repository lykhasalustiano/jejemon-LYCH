import os
import json

class TranslationMemory:
    HISTORY_FILE = 'translation_history.json'

    @classmethod
    def save(cls, original, normalized):
        history = cls.load()
        history.append({
            'timestamp': cls._current_time(),
            'original': original,
            'normalized': normalized
        })
        with open(cls.HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)

    @classmethod
    def load(cls):
        if not os.path.exists(cls.HISTORY_FILE):
            return []
        with open(cls.HISTORY_FILE, 'r') as f:
            return json.load(f)

    @staticmethod
    def _current_time():
        from datetime import datetime
        return datetime.now().isoformat()
