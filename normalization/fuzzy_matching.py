# take note: paki linis na din whole code after magawa and paki check other folder 
# kung may need din idagdag sa mga bawat file para smooth ang program also paki accurate lahat ng name ng function.

from utils.levenshtein import levenshtein_ratio

def fuzzy_jejemon_matching(text, jejemon_dict, threshold=80, corpora=None):
    text = text.lower()
    best_match = None
    best_score = 0
#here to...
    # 1. Check jejemon dictionary
    for normal, variants in jejemon_dict.items():
        for variant in variants:
            score = levenshtein_ratio(text, variant.lower())
            if score > best_score:
                best_score = score
                best_match = normal

    # 2. Check corpora if needed (not functional)
    if best_score < threshold and corpora:
        for word in corpora:
            score = levenshtein_ratio(text, word)
            if score > best_score:
                best_score = score
                best_match = word
#here...
    return best_match if best_score > threshold else None

# Dito connected si levenshtein sa loob ng fuzzy_matching.py 
# ang ginagawa niyang basis lang ay yung jejemon.json(jejemon) pero nandyan na yan si corpora 
# kaso hindi pa proper na nababasa talaga or nagiging basis ng fuzzy_matching. Ang need diyan 
# ay kung walang makikitang match na mas malapit na word si system natin na mula kay jejemon.json 
# saka siya hahanap or mag checheck ngayon sa corpora_words.txt tapos kunyari naka hanap na 

# example na input: "$cho0l nAh @kO0h" sa corpora meron niyan 
# 1. school
# 2. na
# 3. ako
# so dapat output: "School na ako"


