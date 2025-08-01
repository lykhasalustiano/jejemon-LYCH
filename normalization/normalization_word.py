# This code is part of a text normalization module that processes words
# to handle various forms of text input, including jejemon variants, emoticons,
# and special characters. It includes functions for repeated character handling,
# and normalizing words based on predefined lexicons.

def normalize_word(word, alphabet=None, word_special_chars=None):
    if not word:
        return word

    substitutions = {}
    if alphabet:
        for standard, variants in alphabet.items():
            for variant in variants:
                substitutions[str(variant)] = standard
    if word_special_chars:
        substitutions.update(word_special_chars)

    word = ''.join([substitutions.get(char, char) for char in word.lower()])

    result = []
    i = 0
    # Process the word to handle repeated characters and vowels
    while i < len(word):
        char = word[i]
        j = i + 1
        while j < len(word) and word[j] == char:
            j += 1
            
        if char in 'aeiou':
            result.append(char)
        elif char in 'ls' and (j - i) > 2:
            result.append(char * 2)
        else:
            result.append(char)
        i = j
    
    return ''.join(result)