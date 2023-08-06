PATTMATCH
---------

.. image:: https://github.com/monzita/pattmatch/blob/master/pmatch.png

`More algorithms can be found here <https://www.quora.com/What-are-the-most-common-pattern-matching-algorithms>`_

Documentation
-------------

`It's here <https://pattmatch.readthedocs.io>`_

Example
-------

>>> from pattmatch import *
>>>
>>> kmp('ABCABC', 'ABC')
[[0, 3], [3, 6]]
>>> rabin_karb('ABCDAABC', 'ABC')
[[0, 3], [5, 8]]
>>> boyer_moore('AAABAAACAAD', 'AA')
[[0, 2], [1, 3], [4, 6], [5, 7], [8, 10]]
>>> z_array('ABCDAABBCAAAABBCAAAAABCA', 'AAAA')
[1, 0, 0, 0, 2, 1, 0, 0, 0, 4, 3, 2, 1, 0, 0, 0, 4, 4, 3, 2, 1, 0, 0, 1]

LICENCE
-------

`MIT <https://github.com/monzita/pattmatch/blob/master/LICENSE>`_