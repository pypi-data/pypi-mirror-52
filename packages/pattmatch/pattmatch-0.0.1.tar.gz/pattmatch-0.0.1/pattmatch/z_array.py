from pattmatch.helpers import longest_prefix


def z_array(text, pattern): # +DOCTEST ELIPSIS
    """
    Finds all occurences of a pattern in a text.

    >>> z_array('AAAB', 'AA')
    [2, 2, 1, 0]
    >>> z_array('AAABAAAAACAAAAAABAAAAAABBBAAA', 'AAAAB')
    [3, 2, 1, 0, 4, 4, 3, 2, 1, 0, 4, 4, 5, 3, 2, 1, 0, 4, 4, 5, 3, 2, 1, 0, 0, 0, 3, 2, 1]
    >>> z_array('ABCDAABBCAAAABBCAAAAABCA', 'AAAA')
    [1, 0, 0, 0, 2, 1, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 4, 4, 3, 2, 1, 0, 0, 1]
    >>> z_array('ABCA', 'DD')
    [0, 0, 0, 0]

    Args:
        text(str) : text for searching in

        pattern(str): pattern for searching in the text

    Returns all occurences of the pattern in the given text.
    """
    lhs, rhs = [0] * 2
    concatenated = '$'.join([pattern, text])
    z_values = [0] * len(concatenated)
    for i in range(1, len(concatenated)):
        if i > rhs:
            lprefix = longest_prefix(concatenated, pattern, i)
            z_values[i] = len(lprefix)

            if z_values[i] > 0:
                lhs = i
                rhs = i + len(lprefix) - 1
        else:
            k = i - lhs

            if z_values[k] < rhs - i + 1:
                z_values[i] = z_values[k]
            else:
                lhs = i
                lprefix = longest_prefix(concatenated, pattern, i)
                rhs = i + len(lprefix) - 1
                z_values[i] = len(lprefix)

    return z_values[len(pattern) + 1:]
