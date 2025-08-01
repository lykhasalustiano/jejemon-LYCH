from tokenizer.process_word import process_word_with_fuzzy
# Reconstructs a list of tokens into a string, applying fuzzy matching for jejemon words
def reconstruct_from_tokens(tokens, jejemon_dict):

    result = []
    current_word = []

    for token in tokens:
        token_type = token["type"]
        token_value = token["value"]

        if token_type == "space":
            if current_word:
                word = "".join(current_word)
                result.append(process_word_with_fuzzy(word, jejemon_dict))
                current_word = []
            result.append(" ")

        elif token_type in ["alphabet", "unknown"]:
            current_word.append(token_value)

        elif token_type in ["jejemon", "emoticon", "special_char"]:
            if current_word:
                word = "".join(current_word)
                result.append(process_word_with_fuzzy(word, jejemon_dict))
                current_word = []
            result.append(token_value)

    if current_word:
        word = "".join(current_word)
        result.append(process_word_with_fuzzy(word, jejemon_dict))

    return "".join(result)
