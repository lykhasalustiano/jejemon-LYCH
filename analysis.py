import json
import re

# ------------------- Utility Functions -------------------

def validate_text(text):
    return bool(re.match(r'^[\w\s~!@#$%^&*()_+=\-\[\]{}|\\:;"\',.?/]*$', text))

def levenshtein_ratio(s1, s2):
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)

    distance = dp[len1][len2]
    return (1 - distance / max(len1, len2)) * 100

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

def build_reverse_lexicon(alphabet):
    reverse = {}
    for normal, variants in alphabet.items():
        for v in variants:
            reverse[v.lower()] = normal
    return reverse

# ------------------- Core Normalization Logic -------------------

def normalize_word(word):
    if not word:
        return word
    word = word.lower()
    result = []
    i = 0

    while i < len(word):
        char = word[i]
        result.append(char)

        j = i + 1
        while j < len(word) and word[j] == char:
            j += 1
        repeat_count = j - i

        if char in 'aeiou' and repeat_count > 1:
            result.pop()
            result.append(char)
        elif char in 'ls' and repeat_count > 2:
            result.pop()
            result.append(char * 2)
        elif repeat_count > 1:
            result.pop()
            result.append(char)

        i = j
    return ''.join(result)

# ------------------- Fuzzy Matching -------------------

def fuzzy_jejemon_matching(text, jejemon, threshold=80):
    text = text.lower()
    best_match = None
    best_score = 0
    for normal, variants in jejemon.items():
        for variant in variants:
            score = levenshtein_ratio(text, variant.lower())
            if score > best_score:
                best_score = score
                best_match = normal
    return best_match if best_score > threshold else None

# ------------------- Tokenization -------------------

def unified_tokenize(text, alphabet, emoticons, special_chars, jejemon):
    reverse_lex = build_reverse_lexicon(alphabet)
    tokens = []
    i = 0
    text = text.strip()

    max_len = max(
        max((len(k) for k in reverse_lex), default=0),
        max((len(k) for k in emoticons), default=0),
        max((len(v) for variants in jejemon.values() for v in variants), default=0)
    )

    while i < len(text):
        found = False
        for length in range(max_len, 0, -1):
            if i + length > len(text):
                continue
            chunk = text[i:i+length]
            clean_chunk = normalize_word(chunk.lower())

            if chunk.lower() in emoticons:
                tokens.append({"type": "emoticon", "value": emoticons[chunk.lower()], "original": chunk})
                i += length
                found = True
                break

            for normal, variants in jejemon.items():
                if chunk.lower() in [v.lower() for v in variants] or clean_chunk in [v.lower() for v in variants]:
                    tokens.append({"type": "jejemon", "value": normal, "original": chunk})
                    i += length
                    found = True
                    break
            if found:
                break

            if clean_chunk in reverse_lex:
                tokens.append({"type": "alphabet", "value": reverse_lex[clean_chunk], "original": chunk})
                i += length
                found = True
                break

        if not found:
            char = text[i]
            if char in special_chars:
                tokens.append({"type": "special_char", "value": char, "original": char})
            elif char.isspace():
                tokens.append({"type": "space", "value": " ", "original": char})
            else:
                tokens.append({"type": "unknown", "value": char.lower(), "original": char})
            i += 1
    return tokens

# ------------------- Post-processing & Reconstruction -------------------

def process_word_with_fuzzy(word, jejemon):
    if not word.strip():
        return word
    norm = normalize_word(word)
    for normal, variants in jejemon.items():
        if norm in [v.lower() for v in variants]:
            return normal
    fuzzy = fuzzy_jejemon_matching(norm, jejemon)
    return fuzzy if fuzzy else norm

def reconstruct_from_tokens(tokens, jejemon):
    result = []
    current_word = []
    for token in tokens:
        if token["type"] == "space":
            if current_word:
                result.append(process_word_with_fuzzy("".join(current_word), jejemon))
                current_word = []
            result.append(" ")
        elif token["type"] in ["alphabet", "unknown"]:
            current_word.append(token["value"])
        elif token["type"] in ["jejemon", "emoticon"]:
            if current_word:
                result.append(process_word_with_fuzzy("".join(current_word), jejemon))
                current_word = []
            result.append(token["value"])
        elif token["type"] == "special_char":
            if current_word:
                result.append(process_word_with_fuzzy("".join(current_word), jejemon))
                current_word = []
            result.append(token["value"])

    if current_word:
        result.append(process_word_with_fuzzy("".join(current_word), jejemon))

    return "".join(result)

# ------------------- Public Functions -------------------

def token_area(text):
    alphabet, emoticons, special_chars, jejemon = load_lexicons()
    normalized_text = normalize_word(text)
    fuzzy_result = fuzzy_jejemon_matching(normalized_text, jejemon)
    if fuzzy_result:
        return fuzzy_result.capitalize()
    tokens = unified_tokenize(text, alphabet, emoticons, special_chars, jejemon)
    with open("tokenized_output.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)
    result = reconstruct_from_tokens(tokens, jejemon)
    return result.strip().capitalize() if result.strip() else text

def preprocess_mixed_content(text):
    emoticon_patterns = [':)', ':(', ':D', ':P', ';)', '<3', ':/']
    for emo in emoticon_patterns:
        text = text.replace(emo, f' {emo} ')
    return re.sub(r'\s+', ' ', text).strip()

def enhanced_token_area(text):
    return token_area(preprocess_mixed_content(text))
