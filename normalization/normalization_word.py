def normalize_word(word):
    if not word:
        return word
    word = word.lower()
    result = []
    i = 0
    while i < len(word):
        char = word[i]
        result.append(char)
        j = i + 1
        while j < len(word) and word[j] == char:
            j += 1
        repeat_count = j - i

        if char in 'aeiou' and repeat_count > 1:
            result.pop()
            result.append(char)
        elif char in 'ls' and repeat_count > 2:
            result.pop()
            result.append(char * 2)
        elif repeat_count > 1:
            result.pop()
            result.append(char)
        i = j
    return ''.join(result)