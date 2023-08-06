import random
import math

from pattmatch.helpers import random_prime, init_hash

CHAR_SIZE = 256

def rabin_karp(text, pattern): # +DOCTEST ELIPSIS
    """
    Finds all start-end position of searched pattern in the given text.

    >>> rabin_karp('ABCD', 'ABC')
    [[0, 3]]
    >>> rabin_karp('ABC', 'ABC')
    [[0, 3]]
    >>> rabin_karp('ABABC', 'ABC')
    [[2, 5]]
    >>> rabin_karp('ABDBABCDCABC', 'ABC')
    [[4, 7], [9, 12]]

    Args:
        text(str) : text for searching in

        pattern(str): pattern for searching in the text

    Returns all start-end positions of the pattern in the given text.
    """
    global CHAR_SIZE

    prime = random_prime()
    power = CHAR_SIZE ** (len(pattern) - 1)

    text_hash = init_hash(0, len(pattern), text, prime)
    patt_hash = init_hash(0, len(pattern), pattern, prime)

    if text_hash == patt_hash and len(text) == len(pattern):
        return [[0, len(text)]]

    start_end_positions = []

    n, m = len(text), len(pattern)

    for i in range(n - m + 1):
        if text_hash == patt_hash and text[i:i+m] == pattern:
            start_end_positions.append([i, i+m])
        if i < n - m:
            text_hash = (CHAR_SIZE * (text_hash - ord(text[i]) * power) + ord(text[i + m])) % prime
    
    return start_end_positions
