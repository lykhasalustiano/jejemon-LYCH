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

def normalize_word(word):
    if not word:
        return word
    
    word_lower = word.lower()
    normalized = []
    i = 0
    
    while i < len(word_lower):
        current_char = word_lower[i]
        normalized.append(current_char)
        
        # Check if current character is repeated
        j = i + 1
        while j < len(word_lower) and word_lower[j] == current_char:
            j += 1
        
        repeat_count = j - i
        
        # Handle vowel repetitions (always reduce to one)
        if current_char in 'aeiou':
            if repeat_count > 1:
                # Remove the extra added character (since we already added one)
                if len(normalized) > 0 and normalized[-1] == current_char:
                    normalized = normalized[:-1]
                normalized.append(current_char)
        
        # Handle consonant repetitions
        else:
            # For consonants that are commonly doubled in English (l, s, etc.)
            if current_char in 'ls' and repeat_count >= 2:
                # Keep two characters
                if repeat_count > 2:
                    if len(normalized) > 0 and normalized[-1] == current_char:
                        normalized = normalized[:-1]
                    normalized.append(current_char)
                normalized.append(current_char)
            else:
                # For other consonants, just keep one
                if repeat_count > 1:
                    if len(normalized) > 0 and normalized[-1] == current_char:
                        normalized = normalized[:-1]
                    normalized.append(current_char)
        
        i = j
    
    return ''.join(normalized)

def unified_tokenize(text, alphabet, emoticons, special_chars, jejemon):
    reverse_lex = build_reverse_lexicon(alphabet)  
    text = text.strip()  
    i = 0
    tokens = []  

    max_len = max(
        max((len(k) for k in reverse_lex), default=0),
        max((len(k) for k in emoticons), default=0),
        max((len(variant) for variants in jejemon.values() for variant in variants), default=0)
    )

    while i < len(text):
        found = False
        for length in range(max_len, 0, -1):
            if i + length <= len(text):
                chunk = text[i:i+length].lower()  
                original_chunk = text[i:i+length] 
                clean_chunk = normalize_word(chunk)  

                if chunk in emoticons:
                    tokens.append({
                        "type": "emoticon",
                        "value": emoticons[chunk],
                        "original": original_chunk   
                    })
                    i += length  
                    found = True
                    break

               
                for normal_word, variants in jejemon.items():
                    if chunk in [v.lower() for v in variants] or clean_chunk in [v.lower() for v in variants]:
                        tokens.append({
                            "type": "jejemon",
                            "value": normal_word, 
                            "original": original_chunk
                        })
                        i += length
                        found = True
                        break
                if found:
                    break

                if clean_chunk in reverse_lex:
                    tokens.append({
                        "type": "alphabet",
                        "value": reverse_lex[clean_chunk],  
                        "original": original_chunk
                    })
                    i += length
                    found = True
                    break

        if not found:
            char = text[i]
            if char in special_chars: 
                tokens.append({
                    "type": "special_char",
                    "value": char,
                    "original": char
                })
            elif char.isspace(): 
                tokens.append({
                    "type": "space",
                    "value": char,
                    "original": char
                })
            else:  
                tokens.append({
                    "type": "unknown",
                    "value": char.lower(),
                    "original": char
                })
            i += 1

    return tokens  

def fuzzy_jejemon_matching(text, jejemon, threshold=80):
    text_lower = text.lower()
    best_match = None
    best_score = 0

    for normal, variants in jejemon.items():
        for variant in variants:
            score = levenshtein_ratio(text_lower, variant.lower())  
            if score > best_score:
                best_score = score
                best_match = normal
    return best_match if best_score > threshold else None 


def reconstruct_from_tokens(tokens, jejemon):
    result_parts = []
    current_word = []  

    for token in tokens:
        if token["type"] == "space":
            if current_word:  
                processed_word = process_word_with_fuzzy("".join(current_word), jejemon)
                result_parts.append(processed_word)
                current_word = []
            result_parts.append(token["value"]) 
        elif token["type"] in ["alphabet", "unknown"]:
            current_word.append(token["value"]) 
        elif token["type"] in ["jejemon", "emoticon"]:
            if current_word: 
                processed_word = process_word_with_fuzzy("".join(current_word), jejemon)
                result_parts.append(processed_word)
                current_word = []
            result_parts.append(token["value"]) 
        elif token["type"] == "special_char":
            if current_word:
                processed_word = process_word_with_fuzzy("".join(current_word), jejemon)
                result_parts.append(processed_word + token["value"])
                current_word = []
            else:
                result_parts.append(token["value"])

   
    if current_word:
        processed_word = process_word_with_fuzzy("".join(current_word), jejemon)
        result_parts.append(processed_word)

    return "".join(result_parts) 


def process_word_with_fuzzy(word, jejemon):
    if not word.strip():
        return word
    
    word_normalized = normalize_word(word)  
    
    for normal, variants in jejemon.items():
        if word_normalized in [v.lower() for v in variants]:
            return normal
    
 
    fuzzy_result = fuzzy_jejemon_matching(word_normalized, jejemon)
    if fuzzy_result:
        return fuzzy_result
    
    return word_normalized


def token_area(text):
    alphabet, emoticons, special_chars, jejemon = load_lexicons()
    fuzzy_result = fuzzy_jejemon_matching(text, jejemon)
    if fuzzy_result:
        return fuzzy_result.capitalize()
    
    tokens = unified_tokenize(text, alphabet, emoticons, special_chars, jejemon)
    with open("tokenized_output.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)
    
    result = reconstruct_from_tokens(tokens, jejemon)
    return result.strip().capitalize() if result.strip() else text


def preprocess_mixed_content(text):
    emoticon_patterns = [':)', ':(', ':D', ':P', ';)', '<3', ':/']
    for pattern in emoticon_patterns:
        text = text.replace(pattern, f' {pattern} ')  
    text = re.sub(r'\s+', ' ', text) 
    return text.strip()


def enhanced_token_area(text):
    preprocessed_text = preprocess_mixed_content(text)
    return token_area(preprocessed_text)
#---------------------------------------------------------------------------------
#1 FIX NA DOUBLE CHECK MO NA LANG(ETO NALANG HINDI KO MA FIX)
# need pa ifix yung sa multiple character kapag marami inenter si user na character 
# dapat ang maging output ay yung normal text nung ininput ni user example
# user: h3Ll0ooOooooo
# dapat ganito output: Hello
# Napansin ko kasi sa output natin ganito ang lumalabas output: Helloo 
# may sumosobrang isa sa dulo
#-----------------------------------------------------------------------------

#------------------------------------------------------------------------------------
#2 FIX NA DOUBLE CHECK MO NA LANG(DONE)
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
#3 FIX NA DOUBLE CHECK MO NA LANG(DONE)
# lastly yung emoticons pag chineck mo yung emoticons.json natin 
# makikita mo may mga ganito " :), :(, :P, at iba pa" tapos may equivalent siyang emoji
# parang ganito: ":)": "😊"
# problem? hindi pa siya na nonormalized sa ngayon ang nagiging output ay ganito
# user input: :) output: 
# wala siyang output pero dapat ganito
# user input: s0br@n9 s4Y@ k0! :) output: Sobrang saya ko! 😊  
#--------------------------------------------------------------------------------------------