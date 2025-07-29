# take note: paki linis na din whole code after magawa and paki check other folder 
# kung may need din idagdag sa mga bawat file para smooth ang program also paki accurate lahat ng name ng function.

from normalization.normalization_word import normalize_word
from utils.lexicon_loader import build_reverse_lexicon

# from here...
def tokenize_text(text, alphabet, emoticons, special_chars, jejemon):
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
# to here...
    return tokens

# paki dagdag ang corpora para ma tokenize din.
