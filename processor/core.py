import json
import re

from utils.lexicon_loader import load_lexicons
from normalization.normalization_word import normalize_word
from normalization.fuzzy_matching import fuzzy_jejemon_matching
from tokenizer.tokenizer import tokenize_text
from tokenizer.reconstruct import reconstruct_from_tokens

def token_area(text):
    
    alphabet, emoticons, special_chars, jejemon, corpora = load_lexicons()
    normalized_text = normalize_word(text)
    fuzzy_result = fuzzy_jejemon_matching(normalized_text, jejemon)

    if fuzzy_result:
        return fuzzy_result.capitalize()
    tokens = tokenize_text(text, alphabet, emoticons, special_chars, jejemon)

    with open("tokenized_output.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)
    result = reconstruct_from_tokens(tokens, jejemon, corpora)

    return result.strip().capitalize() if result.strip() else text

def preprocess_mixed_content(text):

    emoticon_patterns = [':)', ':(', ':D', ';)', '<3', ':/']

    for emo in emoticon_patterns:
        text = text.replace(emo, f' {emo} ')
        
    return re.sub(r'\s+', ' ', text).strip()

def enhanced_token_area(text):
    return token_area(preprocess_mixed_content(text))