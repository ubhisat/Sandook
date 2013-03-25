__author__ = 'satmeet'
'''
Inspired from http://stackoverflow.com/a/2510816
'''

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def _enbase(x):
    n = len(alphabet)
    if x < n:
        return alphabet[x]
    return _enbase(x / n) + alphabet[x % n]


def _debase(x):
    n = len(alphabet)
    result = 0
    for i, c in enumerate(reversed(x)):
        result += alphabet.index(c) * (n ** i)
    return result


def _pad(x, n):
    p = alphabet[0] * (n - len(x))
    return '%s%s' % (x, p)


def mid(a='a' * 26, b='z' * 26):
    n = max(len(a), len(b))
    a = _debase(_pad(a, n))
    b = _debase(_pad(b, n))
    return _enbase((a + b) / 2)
