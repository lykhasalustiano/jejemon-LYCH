import json
import re
import string

def validate_text(text):
    return bool(re.match(r'^[\w\s~!@#$%^&*()_+=\-\[\]{}|\\:;"\',.?/]*$', text))

def levenshtein_ratio(s1, s2):
    len1, len2 = len(s1), len(s2)
    dp = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        dp[i][0] = i
    for j in range(len2 + 1):
        dp[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )

    distance = dp[len1][len2]
    max_len = max(len1, len2)
    return (1 - distance / max_len) * 100 if max_len != 0 else 100

def correct_typo(token, lexicon):
    lowered = token.lower()
    for key, variants in lexicon.items():
        if lowered in variants:
            return key

    similarities = []
    for key, variants in lexicon.items():
        for variant in variants:
            ratio = levenshtein_ratio(lowered, variant)
            similarities.append((key, ratio))

    best_match = max(similarities, key=lambda x: x[1])
    if best_match[1] > 60:
        return best_match[0]
    return token

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

def normalize_text(text, alphabet):
    reverse_lex = build_reverse_lexicon(alphabet)
    lowered = text.lower()
    for jej, norm in reverse_lex.items():
        lowered = re.sub(rf"{re.escape(jej)}", norm, lowered)
    lowered = re.sub(r'(.)\1+', r'\1', lowered)  # compress repeated chars
    return lowered

def tokenize(text, alphabet, emoticons, special_chars):
    reverse_lex = build_reverse_lexicon(alphabet)
    text = text.strip()
    lowered = text.lower()
    i = 0
    tokens = []

    max_len = max(
        max((len(k) for k in reverse_lex), default=0),
        max((len(k) for k in emoticons), default=0)
    )

    while i < len(text):
        found = False
        for length in range(max_len, 0, -1):
            if i + length <= len(text):
                chunk = text[i:i+length].lower()

                if chunk in reverse_lex:
                    tokens.append({
                        "type": "alphabet",
                        "value": reverse_lex[chunk]
                    })
                    i += length
                    found = True
                    break
                elif chunk in emoticons:
                    tokens.append({
                        "type": "emoticon",
                        "value": emoticons[chunk]
                    })
                    i += length
                    found = True
                    break

        if not found:
            char = text[i]
            if char in special_chars:
                tokens.append({
                    "type": "special_char",
                    "value": char
                })
            else:
                tokens.append({
                    "type": "unknown",
                    "value": char.lower()
                })
            i += 1

    return tokens

def apply_jejemon(words, jejemon):
    transformed = []
    for word in words:
        word_lower = word.lower()
        found = False
        for key, variants in jejemon.items():
            if word_lower in variants:
                transformed.append(key)
                found = True
                break
        if not found:
            transformed.append(word)
    return transformed

def fuzzy_matching(text, jejemon):
    text_lower = text.lower()
    best_match = None
    best_score = 0

    for normal, variants in jejemon.items():
        for variant in variants:
            score = levenshtein_ratio(text_lower, variant.lower())
            if score > best_score:
                best_score = score
                best_match = normal

    if best_score > 80:
        return best_match.capitalize()
    return None

def token_area(text):
    alphabet, emoticons, special_chars, jejemon = load_lexicons()

    fuzzy_result = fuzzy_matching(text, jejemon)
    if fuzzy_result:
        return fuzzy_result

    normalized_text = normalize_text(text, alphabet)
    tokens = tokenize(normalized_text, alphabet, emoticons, special_chars)

    with open("tokenized_output.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)

    token_join = "".join(token["value"] for token in tokens if token["type"] in ["alphabet", "unknown", "special_char", "emoticon"])
    words = token_join.split()

    jejemon_transformed = []

    for word in words:
        punct = ''
        if word and word[-1] in string.punctuation:
            punct = word[-1]
            word = word[:-1]

        transformed = None
        for key, variants in jejemon.items():
            if word.lower() in variants:
                transformed = key
                break
        if not transformed:
            fuzzy = fuzzy_matching(word, jejemon)
            transformed = fuzzy if fuzzy else word

        jejemon_transformed.append(transformed + punct)

    response = " ".join(jejemon_transformed)
    return response.capitalize()

#---------------------------------------------------------------------------------
#1 FIX NA DOUBLE CHECK MO NA LANG
# need pa ifix yung sa multiple character kapag marami inenter si user na character 
# dapat ang maging output ay yung normal text nung ininput ni user example
# user: h3Ll0ooOooooo
# dapat ganito output: Hello
# Napansin ko kasi sa output natin ganito ang lumalabas output: Helloo 
# may sumosobrang isa sa dulo
#-----------------------------------------------------------------------------

#------------------------------------------------------------------------------------
#2 FIX NA DOUBLE CHECK MO NA LANG
# next don yung special character need din ifix if hindi naman need inormamlize 
# dapat sa output nandon pa rin siya pero kung need inormalize kailangan wala 
# siya sa output kung ginamit siya as a jejemon text.
# example: user input: @No? output: Ano?
# ang lumalabas kasi sa output natin ganito:
# user input: @no? output Ano
# kumbaga tinanggal niya special character kahit hindi naman dapat
# tanggalin kase normal sa text na nagtatanong na may question mark
#---------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------
#3 FIX NA DOUBLE CHECK MO NA LANG
# lastly yung emoticons pag chineck mo yung emoticons.json natin 
# makikita mo may mga ganito " :), :(, :P, at iba pa" tapos may equivalent siyang emoji
# parang ganito: ":)": "😊"
# problem? hindi pa siya na nonormalized sa ngayon ang nagiging output ay ganito
# user input: :) output: 
# wala siyang output pero dapat ganito
# user input: s0br@n9 s4Y@ k0! :) output: Sobrang saya ko! 😊
#--------------------------------------------------------------------------------------------