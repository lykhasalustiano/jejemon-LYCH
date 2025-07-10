# import re

# class JejemonTranslator:
#     JEJEMON_MAP = {
#         "7h": "cityh", "0": "o", "4q": "ako", 
#         "aq": "ako", "p": "pa", "l": "ll",
#         "3": "e", "1": "i", "2": "to", "4": "for",
#         "u": "you", "r": "are", "y": "why",
#         "pls": "please", "kc": "kasi", "prn": "pero"
#     }

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
from difflib import SequenceMatcher

class TextProcessor:
    @staticmethod
    def validate_text(text):
        """Validate input text to ensure it contains only allowed characters."""
        return bool(re.match(r'^[\w\s~!@#$%^&*()_+=\-\[\]{}|\\:;"\',.?/]*$', text))

    @staticmethod
    def string_similarity(a, b):
        """Calculate similarity ratio between two strings."""
        return SequenceMatcher(None, a, b).ratio()

    @staticmethod
    def correct_typo(token, lexicon):
        """Correct a token based on similarity to known lexicon entries."""
        if token in lexicon:
            return lexicon[token]
        similarities = [(key, TextProcessor.string_similarity(token, key)) 
                       for key in lexicon.keys()]
        best_match = max(similarities, key=lambda x: x[1])
        if best_match[1] > 0.6:  
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