# take note: paki linis na din whole code after magawa and paki check other folder 
# kung may need din idagdag sa mga bawat file para smooth ang program also paki accurate lahat ng name ng function.

from tokenizer.process_word import process_word_with_fuzzy
# from here...
def reconstruct_from_tokens(tokens, jejemon, corpora):
    result = []
    current_word = []
    for token in tokens:
        if token["type"] == "space":
            if current_word:
                result.append(process_word_with_fuzzy("".join(current_word), jejemon, corpora))
                current_word = []
            result.append(" ")
        elif token["type"] in ["alphabet", "unknown"]:
            current_word.append(token["value"])
        elif token["type"] in ["jejemon", "emoticon"]:
            if current_word:
                result.append(process_word_with_fuzzy("".join(current_word), jejemon, corpora))
                current_word = []
            result.append(token["value"])
        elif token["type"] == "special_char":
            if current_word:
                result.append(process_word_with_fuzzy("".join(current_word), jejemon, corpora))
                current_word = []
            result.append(token["value"])

    if current_word:
        result.append(process_word_with_fuzzy("".join(current_word), jejemon, corpora))
# to here...
    return "".join(result)

# paki dagdag ang corpora para ma tokenize din.
