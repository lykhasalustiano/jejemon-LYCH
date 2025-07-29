# take note: paki linis na din whole code after magawa and paki check other folder 
# kung may need din idagdag sa mga bawat file para smooth ang program also paki accurate lahat ng name ng function.

def levenshtein_ratio(s1, s2):
    len1, len2 = len(s1), len(s2)
    if len1 == 0 or len2 == 0:
        return 0

    matrix = [[0 for _ in range(len2 + 1)] for _ in range(len1 + 1)]

    for i in range(len1 + 1):
        matrix[i][0] = i
    for j in range(len2 + 1):
        matrix[0][j] = j

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            matrix[i][j] = min(
                matrix[i - 1][j] + 1,     # deletion
                matrix[i][j - 1] + 1,     # insertion
                matrix[i - 1][j - 1] + cost  # substitution
            )

    distance = matrix[len1][len2]
    max_len = max(len1, len2)
    return round((1 - distance / max_len) * 100)