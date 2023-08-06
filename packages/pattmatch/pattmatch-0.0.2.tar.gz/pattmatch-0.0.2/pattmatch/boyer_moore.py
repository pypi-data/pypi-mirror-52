from pattmatch.helpers import difference

def boyer_moore(text, pattern):
    """
    Finds all start-end positions, containing every start and end of the given pattern in the text.

    >>> boyer_moore('AAA', 'A')
    [[0, 1], [1, 2], [2, 3]]
    >>> boyer_moore('ABAACD', 'AC')
    [[3, 5]]
    >>> boyer_moore('AABAACAADAABAABA', 'AABA')
    [[0, 4], [9, 13], [12, 16]]
    >>> boyer_moore('AAABACAAABCAADCVABCDABCFGABC', 'ABC')
    [[8, 11], [16, 19], [20, 23], [25, 28]]

    Args:
        text(str) : text for searching in
        
        pattern(str): pattern for searching in the text

    Returns all start-end positions of the pattern in the given text.
    """
    start_end_positions = []
    if text == pattern:
        start_end_positions.append([0, len(pattern)])

    i = len(pattern)
    while i < len(text) + 1:
        if text[i-len(pattern):i] == pattern:
            start_end_positions.append([i-len(pattern), i])
        i += difference(text, pattern, i) or 1
    return start_end_positions
