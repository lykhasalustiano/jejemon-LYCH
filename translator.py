import re
import json
import os
from datetime import datetime

class JejemonTranslator:
    JEJEMON_MAP = {
        "7h": "cityh", "0": "o", "4q": "ako", 
        "aq": "ako", "p": "pa", "l": "ll",
        "3": "e", "1": "i", "2": "to", "4": "for",
        "u": "you", "r": "are", "y": "why",
        "pls": "please", "kc": "kasi", "prn": "pero"
    }

    @classmethod
    def normalize(cls, text):
        """Convert Jejemon text to standard Filipino"""
        text = text.lower()
        for jej, norm in cls.JEJEMON_MAP.items():
            text = re.sub(rf'\b{jej}\b', norm, text)
        text = re.sub(r'(.)\1{2,}', r'\1', text)
        return text.capitalize()

    @classmethod
    def analyze(cls, text):
        """Return translation with statistics"""
        normalized = cls.normalize(text)
        return {
            'original': text,
            'normalized': normalized,
            'length_diff': len(text) - len(normalized),
            'changed': text.lower() != normalized.lower()
        }
