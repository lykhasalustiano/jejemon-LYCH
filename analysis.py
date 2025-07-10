#     @classmethod
#     def normalize(cls, text):
#         """Convert Jejemon text to standard Filipino"""
#         text = text.lower()
#         for jej, norm in cls.JEJEMON_MAP.items():
#             text = re.sub(rf'\b{jej}\b', norm, text)
#         text = re.sub(r'(.)\1{2,}', r'\1', text)
#         return text.capitalize()

#     @classmethod
#     def analyze(cls, text):
#         """Return translation with statistics"""
#         normalized = cls.normalize(text)
#         return {
#             'original': text,
#             'normalized': normalized,
#             'length_diff': len(text) - len(normalized),
#             'changed': text.lower() != normalized.lower()
# 
#         }

import json
import re

class TextProcessor:
    @staticmethod
    def validate_text(text):
        """Validate input text to ensure it contains only allowed characters."""
        return bool(re.match(r'^[\w\s~!@#$%^&*()_+=\-\[\]{}|\\:;"\',.?/]*$', text))

    @staticmethod
    def string_similarity(a, b):
        """Calculate similarity ratio between two strings using SequenceMatcher."""
        from difflib import SequenceMatcher
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def levenshtein_ratio(s1, s2):
        """Calculate Levenshtein similarity ratio between two strings."""
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
                    dp[i - 1][j] + 1,      # Deletion
                    dp[i][j - 1] + 1,      # Insertion
                    dp[i - 1][j - 1] + cost  # Substitution
                )

        distance = dp[len1][len2]
        max_len = max(len1, len2)
        return (1 - distance / max_len) * 100 if max_len != 0 else 100

    @staticmethod
    def correct_typo(token, lexicon):
        """Correct a token based on similarity to known lexicon entries using Levenshtein ratio."""
        if token in lexicon:
            return lexicon[token]
        
        #----------------------------------------------------------------------------------------------------
        #  Ang Levenshtein ratio ay ginagamit para ikumpara ang token example sa bawat key 
        # sa lexicon para ma compute nya kung gaano sila magkapareho.
        #----------------------------------------------------------------------------------------------------

        similarities = [
            (key, TextProcessor.levenshtein_ratio(token, key)) for key in lexicon.keys()
        ]

        #----------------------------------------------------------------------------------------------------
        # Hanapin nya pinaka close na match
        #----------------------------------------------------------------------------------------------------
        
        best_match = max(similarities, key=lambda x: x[1])

        #----------------------------------------------------------------------------------------------------
        # kapag may similarity 60% pataas mag assume sya na typo sya at tama lang 
        #----------------------------------------------------------------------------------------------------

        if best_match[1] > 60:  
            return lexicon[best_match[0]]
        return token


def load_lexicons():
    with open("lexicon/alphabet.json", "r", encoding="utf-8") as f:
        alphabet = json.load(f)

    with open("lexicon/emoticons.json", "r", encoding="utf-8") as f:
        emoticons = json.load(f)                                                     

    with open("lexicon/special_characters.json", "r", encoding="utf-8") as f:
        special_chars = json.load(f)

    return alphabet, emoticons, special_chars # to here....  

#----------------------------------------------------------------------------------------------------
# itong function na load_lexicon ginawa ko para mabasa yung lexicon file na nasa .json para kapag
# nag tokenize may data na manggagaling dito na kailangan sa tokenization (ready na yung data)
#----------------------------------------------------------------------------------------------------


def build_reverse_lexicon(alphabet): # from here...
    reverse = {}
    for normal, variants in alphabet.items():
        for v in variants:
            reverse[v.lower()] = normal
    return reverse # to here...

#----------------------------------------------------------------------------------------------------
# ito naman ang ginagawa nito nag rereverse lookup lang siya sa alphabet lexicon natin para
# madali ma convert yung jejemon input ni user sa normal text.
# bali halimbawa: kung sa JSON "a": ["4", "@", "a"], gagawin niyang "4": "a", "@": "a", "a": "a".
# ito yung ginagamit para makilala agad ang jejemon letter at ma-convert ito pabalik sa normal na letter.
#----------------------------------------------------------------------------------------------------

def tokenize(text, alphabet, emoticons, special_chars): # from here...
    reverse_lex = build_reverse_lexicon(alphabet)
    text = text.strip()
    lowered = text.lower()
    i = 0
    tokens = []

    while i < len(text):
        found = False

        for length in [3, 2, 1]: # from here...
            if i + length <= len(lowered):
                chunk = lowered[i:i+length]
                if chunk in reverse_lex:
                    tokens.append({
                        "type": "alphabet",
                        "value": reverse_lex[chunk]
                    })
                    i += length
                    found = True
                    break # to here...

        # -------------------------------------------------------------------------------------------------------------
        # sinusubukan neto hulihin yung jejemon input ni user kung mapapansin mo kasi sa 3 lexicon natin yung alphabet 
        # ang may reverse dictionary (jejemon style) 
        # Pinipili muna yung pinakamahabang combination (3 characters) bago mag-fallback sa 2 o 1 character,
        # para ma-detect yung mga multi-letter jejemon words tulad ng "ph" → "f".
        # --------------------------------------------------------------------------------------------------------------

        if not found: # from here...
            char = text[i] # to here...

        #------------------------------------------------------------------------------------------
        # kung walang makitang match sa alphabet, irereview neto yung character sa position "i"
        #------------------------------------------------------------------------------------------
   
            if char in special_chars: #from here...
                tokens.append({
                    "type": "special_char",
                    "value": char
                })
                i += 1
            elif any(char in values for values in emoticons.values()):
                tokens.append({
                    "type": "emoticon",
                    "value": char
                })
                i += 1
            else:
                tokens.append({
                    "type": "unknown",
                    "value": char.lower()
                })
                i += 1 # to here...
            #---------------------------------------------------------------------------------------------------
            # eto yung review checking na nasa position i kung emoticons ba siya, special character, or unknown 
            #---------------------------------------------------------------------------------------------------

    return tokens # to here...
 
    #-----------------------------------------------------------------------------------------------------------------------------
    # ito yung pinaka tokenization part, dito sa function na ito ang ginagawa niyan yan yung nag seseperate ng input text ni user
    # bali kaya niya hinihiwa-hiwalay para ma classify niya kung ano ibig sabihin nung bawat text or bawat laman ng input ni user.
    # sa pamamagitan kasi non magkaka output na ng normal text version.
    #-----------------------------------------------------------------------------------------------------------------------------


def token_area(text): #from here
    alphabet, emoticons, special_chars = load_lexicons()
    tokens = tokenize(text, alphabet, emoticons, special_chars)

    with open("tokenized_output.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)

    token_join = "".join(token["value"] for token in tokens if token["type"] in ["alphabet", "unknown"])
    return token_join # to here...

#------------------------------------------------------------------------
# pang save lang ito sa tokenized_output.json natin, dito napupunta yung 
# type (lexicon) and value (laman ng lexicon na analyze at nagamit)"
# -----------------------------------------------------------------------