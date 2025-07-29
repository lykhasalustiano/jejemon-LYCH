# take note: paki linis na din whole code after magawa and paki check other folder 
# kung may need din idagdag sa mga bawat file para smooth ang program also paki accurate lahat ng name ng function.

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
        #here to...
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
        #here...
    return ''.join(result)

# Paki-fix ito.

# pwede din na if else tapos magkasama na lang si vowels at consonant tapos if na notify ng system 
# or recognized ni sys na need bawasan yung multiple character babawasan pero kung hindi else irereturn niya yung normal text 
# sa ininput example: input: "H3ll0oOo" may multiple char yan so ang mangyayari sa condition if yung 
# char ay multiple babawasan niya yon mapa vowels or consonant tapos else kung hindi naman need bawasan char dahil normal
# lang yung bilang ng letter rereturn niya lang and ang output ay: "Hello" 