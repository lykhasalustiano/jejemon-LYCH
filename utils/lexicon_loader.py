import json

# this code loads lexicons from JSON files

def load_lexicons():

    with open("lexicon/alphabet.json", "r", encoding="utf-8") as f:
        alphabet = json.load(f)
    with open("lexicon/emoticons.json", "r", encoding="utf-8") as f:
        emoticons = json.load(f)
    with open("lexicon/special_characters.json", "r", encoding="utf-8") as f:
        special_chars = json.load(f)
    with open("lexicon/jejemon.json", "r", encoding="utf-8") as f:
        jejemon = json.load(f)

    return alphabet, emoticons, special_chars, jejemon

# This function builds a reverse lexicon for quick lookup
# It maps each variant to its standard form.

def build_reverse_lexicon(alphabet):
    reverse = {}
    for normal, variants in alphabet.items():
        for variant in variants:
            reverse[variant.lower()] = normal
    return reverse
