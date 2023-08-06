from pattmatch.helpers import longest_proper_prefixes


def kmp(text, pattern): # +DOCTEST ELIPSIS
    """
    Finds all start-end of searched pattern in the given text.

    >>> kmp('ABACD', 'ACD')
    [[2, 5]]
    >>> kmp('ABCDABC', 'ABC')
    [[0, 3], [4, 7]]
    >>> kmp('AAAAABAAABA', 'AAAA')
    [[0, 4], [1, 5]]
    >>> kmp('ABC', 'D')
    []

    Args:
        text(str) : text for searching in
        
        pattern(str): pattern for searching in the text

    Returns all start-end positions of the pattern in the given text.
    """
    lps = longest_proper_prefixes(pattern)
    start_end_positions = []

    i, j = [0] * 2

    while i < len(text):
        if text[i] == pattern[j]:
            i = i + 1
            j = j + 1
        else:
            if j is 0:
                i = i + 1
            else:
                j = lps[j - 1]

        if j == len(pattern):
            start_end_positions.append([i - j, i])
            j = lps[j - 1]

    return start_end_positions
