from utils.levenshtein import levenshtein_ratio

def fuzzy_jejemon_matching(text, jejemon_dict, threshold=80, corpora=None):
    text = text.lower()
    best_match = None
    best_score = 0

    # 1. Check jejemon dictionary
    for normal, variants in jejemon_dict.items():
        for variant in variants:
            score = levenshtein_ratio(text, variant.lower())
            if score > best_score:
                best_score = score
                best_match = normal

    # 2. Check corpora if needed
    if best_score < threshold and corpora:
        for word in corpora:
            score = levenshtein_ratio(text, word)
            if score > best_score:
                best_score = score
                best_match = word

    return best_match if best_score > threshold else None

