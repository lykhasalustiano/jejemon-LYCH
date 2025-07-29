# take note: paki linis na din whole code after magawa and paki check other folder 
# kung may need din idagdag sa mga bawat file para smooth ang program also paki accurate lahat ng name ng function.

import json

def load_lexicons():
    with open("lexicon/alphabet.json", "r", encoding="utf-8") as f:
        alphabet = json.load(f)
    with open("lexicon/emoticons.json", "r", encoding="utf-8") as f:
        emoticons = json.load(f)
    with open("lexicon/special_characters.json", "r", encoding="utf-8") as f:
        special_chars = json.load(f)
    with open("lexicon/jejemon.json", "r", encoding="utf-8") as f:
        jejemon = json.load(f)
    with open("lexicon/corpora_words.txt", "r", encoding="utf-8") as f:
        corpora = set(line.strip().lower() for line in f if line.strip())
    return alphabet, emoticons, special_chars, jejemon, corpora


def build_reverse_lexicon(alphabet):

    reverse = {}
    
    for normal, variants in alphabet.items():
        for v in variants:
            reverse[v.lower()] = normal
    return reverse
