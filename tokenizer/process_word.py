from normalization.fuzzy_matching import fuzzy_jejemon_matching
from normalization.normalization_word import normalize_word
# Tokenizes text based on lexicons and reconstructs it into a readable format.
def process_word_with_fuzzy(word, jejemon_dict):
 
    if not word.strip():
        return word

    normalized = normalize_word(word)

    # Direct match in jejemon variants
    for normal, variants in jejemon_dict.items():
        if normalized in [v.lower() for v in variants]:
            return normal

    # Fuzzy match
    fuzzy = fuzzy_jejemon_matching(normalized, jejemon_dict)
    return fuzzy if fuzzy else normalized
