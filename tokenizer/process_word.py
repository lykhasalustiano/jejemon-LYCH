# take note: paki linis na din whole code after magawa and paki check other folder 
# kung may need din idagdag sa mga bawat file para smooth ang program also paki accurate lahat ng name ng function.

from normalization.fuzzy_matching import fuzzy_jejemon_matching
from normalization.normalization_word import normalize_word

def process_word_with_fuzzy(word, jejemon, corpora):
    if not word.strip():
        return word

    norm = normalize_word(word)
    
    # Direct match in corpora
    if norm in corpora:
        return norm

    # Match in jejemon variants
    for normal, variants in jejemon.items():
        if norm in [v.lower() for v in variants]:
            return normal

    # Fuzzy match
    fuzzy = fuzzy_jejemon_matching(norm, jejemon)
    return fuzzy if fuzzy else norm
