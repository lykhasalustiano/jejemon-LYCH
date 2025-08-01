from utils.levenshtein import levenshtein_ratio
#this code implements fuzzy matching for jejemon text normalization.
def fuzzy_jejemon_matching(text, jejemon_dict, threshold=80):
    text = text.lower()
    best_match = None
    best_score = 0

    # Check jejemon dictionary for best fuzzy match
    for normal, variants in jejemon_dict.items():
        for variant in variants:
            score = levenshtein_ratio(text, variant.lower())
            if score > best_score:
                best_score = score
                best_match = normal

    return best_match if best_score > threshold else None
