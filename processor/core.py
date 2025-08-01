import json
import re

from utils.lexicon_loader import load_lexicons
from normalization.normalization_word import normalize_word
from normalization.fuzzy_matching import fuzzy_jejemon_matching
from tokenizer.tokenizer import tokenize_text
from tokenizer.reconstruct import reconstruct_from_tokens

# main function to handle all

def token_area(text):
    # Load lexicons, excluding corpora entirely
    alphabet, emoticons, special_chars, jejemon = load_lexicons()
    
    # Try fuzzy matching against jejemon dictionary
    normalized_text = normalize_word(text)
    fuzzy_result = fuzzy_jejemon_matching(normalized_text, jejemon)

    if fuzzy_result:
        return fuzzy_result.capitalize()

    # Tokenize and reconstruct if no fuzzy match found
    tokens = tokenize_text(text, alphabet, emoticons, special_chars, jejemon)

    # Save tokens for debugging
    with open("tokenized_output.json", "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4, ensure_ascii=False)
    # Reconstruct the tokens into a readable format
    result = reconstruct_from_tokens(tokens, jejemon)

    return result.strip().capitalize() if result.strip() else text

# Preprocess mixed content to handle emoticons
def preprocess_mixed_content(text):
    emoticon_patterns = [":)", ":-)", ":-D", ":(", ":-(", ":'(", ":')", ";)", ";-)", ":o", ":p", ":-O", ":/", ":-/", ":|", ":-|", ":3", "<3", "</3", "^_^", "(╥﹏╥)", ">_<", "-_-", "x_x", ":'')", ">:(", ">:)", ":*", ":-*", "8)", "8-)", "o_o", "O_O", "owo", "uwu", "xd"]
    for emo in emoticon_patterns:
        text = text.replace(emo, f' {emo} ')
    return re.sub(r'\s+', ' ', text).strip()

def enhanced_token_area(text):
    return token_area(preprocess_mixed_content(text))


