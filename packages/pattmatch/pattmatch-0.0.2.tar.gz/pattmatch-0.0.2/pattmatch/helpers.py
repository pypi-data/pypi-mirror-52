import random
import math

"""
Helper methods used from implemented algorithms.
"""

def difference(text, pattern, index): # +DOCTEST ELIPSIS
    """
    Method used by boyer moore's algorithm.
    """
    j = index - 1
    from_index = 0
    for i in range(len(pattern) - 1, -1, -1):
        if pattern[i] != text[j]:
            if not text[j] in pattern:
                return len(pattern) - from_index
            else:
                return i - pattern[:i].rindex(text[j])
            break
        from_index = from_index + 1
        j = j - 1
    return 0


def longest_proper_prefixes(pattern):
    """
    Returns longest common prefices of the given pattern.
    Method used by kmp's algorithm.

    >>> longest_proper_prefixes('ABCDABD')
    [0, 0, 0, 0, 1, 2, 0]
    >>> longest_proper_prefixes('AABAACAABAA')
    [0, 1, 0, 1, 2, 0, 1, 2, 3, 4, 5]
    >>> longest_proper_prefixes('AAAA')
    [0, 1, 2, 3]
    >>> longest_proper_prefixes('AAACAAAAAC')
    [0, 1, 2, 0, 1, 2, 3, 3, 3, 4]
    """
    longest_proper_prefix = [0] * (len(pattern))
    for current_index in range(len(pattern) + 1):
        longest_prefix = [pattern[:current_index - i] for i in range(1, current_index)
                           if pattern[:current_index - i] == pattern[i:current_index]]
        longest_proper_prefix[current_index - 1] = len(longest_prefix[0]) if len(longest_prefix) else 0

    return longest_proper_prefix

CHAR_SIZE = 256

def init_hash(i, j, text, prime):
    """
    Returns a hash of the text[i:j].
    Method used by rabin karp's algorithm.
    """
    global CHAR_SIZE
    text_hash = 0

    for l in range(i, j):
        text_hash = (CHAR_SIZE * text_hash + ord(text[l])) % prime
    return text_hash
 
def random_prime():
    """
    Returns random prime.
    Method used by rabin karp's algorithm.
    """
    random.seed()
    global CHAR_SIZE

    prime = None
    start_from = random.randint(CHAR_SIZE ** 2, CHAR_SIZE ** 3)
    for i in range(start_from, CHAR_SIZE ** 3):
        is_not_prime = sum([j for j in range(2, math.ceil(math.sqrt(i))) if i % j == 0])
        if is_not_prime:
            next
        else:
            prime = i
            break

    return prime


def longest_prefix(text, pattern, start):
    """
    Finds the longest prefix of text and pattern.
    """
    end = len(pattern)
    while text[start:start + end] != pattern[:end]:
        end -= 1

    return text[start:start + end]
