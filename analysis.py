# import re

# class JejemonTranslator:
#     JEJEMON_MAP = {
#         "7h": "cityh", "0": "o", "4q": "ako", 
#         "aq": "ako", "p": "pa", "l": "ll",
#         "3": "e", "1": "i", "2": "to", "4": "for",
#         "u": "you", "r": "are", "y": "why",
#         "pls": "please", "kc": "kasi", "prn": "pero"
#     }

#     @classmethod
#     def normalize(cls, text):
#         """Convert Jejemon text to standard Filipino"""
#         text = text.lower()
#         for jej, norm in cls.JEJEMON_MAP.items():
#             text = re.sub(rf'\b{jej}\b', norm, text)
#         text = re.sub(r'(.)\1{2,}', r'\1', text)
#         return text.capitalize()

#     @classmethod
#     def analyze(cls, text):
#         """Return translation with statistics"""
#         normalized = cls.normalize(text)
#         return {
#             'original': text,
#             'normalized': normalized,
#             'length_diff': len(text) - len(normalized),
#             'changed': text.lower() != normalized.lower()
# 
#         }


import json

# para 'to sa lexicon file
# para mabasa ng system at maka pag analyze siya
def load_lexicons():
    with open("lexicon/alphabet.json", "r", encoding="utf-8") as f:
        alphabet = json.load(f)

    with open("lexicon/emoticons.json", "r", encoding="utf-8") as f:
        emoticons = json.load(f)

    with open("lexicon/special_characters.json", "r", encoding="utf-8") as f:
        special_chars = json.load(f)

    return alphabet, emoticons, special_chars

def build_reverse_lexicon(alphabet):
    reverse = {}
    for normal, variants in alphabet.items():
        for v in variants:
            reverse[v.lower()] = normal
    return reverse

def normalize(text):
    alphabet, emoticons, special_chars = load_lexicons()
    reverse_lex = build_reverse_lexicon(alphabet)

    text = text.strip()
    i = 0
    normalized = ""
    lowered = text.lower()

    while i < len(text):
        found = False

        for length in [3, 2, 1]:
            if i + length <= len(text):
                chunk = lowered[i:i+length]
                if chunk in reverse_lex:
                    normalized += reverse_lex[chunk]
                    i += length
                    found = True
                    break

        if not found:
            char = text[i]
            if char in special_chars:
                i += 1
            elif any(char in values for values in emoticons.values()):
                i += 1
            else:
                normalized += char.lower()
                i += 1

    return normalized
