from collections import OrderedDict
import sys
import unicodedata
import unittest

from curl_requests.structures import CaseInsensitiveDict


def xfail_if(cond):
    if cond:
        return unittest.expectedFailure
    return lambda x: x

class TestCaseInsensitiveDict(unittest.TestCase):
    def test_eq(self):
        assert CaseInsensitiveDict(a=1) == CaseInsensitiveDict(a=1)
        assert CaseInsensitiveDict(a=1) == CaseInsensitiveDict(A=1)
        assert CaseInsensitiveDict(A=1) == CaseInsensitiveDict(a=1)
        assert CaseInsensitiveDict(A=1) == CaseInsensitiveDict(A=1)
        assert CaseInsensitiveDict(a=1) == {'A': 1}
        assert {'a': 1} == CaseInsensitiveDict(A=1)

    def test_intl(self):
        assert CaseInsensitiveDict({'ss': 1}) == {'ß': 1}
        assert CaseInsensitiveDict({'sS': 1}) == {'ß': 1}
        assert CaseInsensitiveDict({'Ss': 1}) == {'ß': 1}
        assert CaseInsensitiveDict({'SS': 1}) == {'ß': 1}
        assert CaseInsensitiveDict({'ß': 1}) == {'ss': 1}
        assert CaseInsensitiveDict({'ß': 1}) == {'sS': 1}
        assert CaseInsensitiveDict({'ß': 1}) == {'Ss': 1}
        assert CaseInsensitiveDict({'ß': 1}) == {'SS': 1}

        assert CaseInsensitiveDict({'ς': 1}) == {'σ': 1}
        assert CaseInsensitiveDict({'Σ': 1}) == {'σ': 1}
        assert CaseInsensitiveDict({'Σ': 1}) == {'ς': 1}

    def test_intl_nfd(self):
        # combining iota is nasty if there are also accents
        # insert an accent at *every* position to test
        strings = [
            # E I
            ('\u0389\u0399', True), # Ea I (NFC)
            ('\u0397\u0301\u0399', True), # E a I (NFD)
            ('\u0397\u038a', False), # E Ia (NFC)
            ('\u0397\u0399\u0301', False), # E I a (NFD)

            # E i
            ('\u0389\u03b9', True), # Ea i (NFC)
            ('\u0397\u0301\u03b9', True), # E a i (NFD)
            ('\u0397\u03af', False), # E ia (NFC)
            ('\u0397\u03b9\u0301', False), # E i a (NFD)

            # EP, E P (note P always NFx's to i)
            ('\u0389\u1fbe', True), # Ea P
            ('\u0397\u0301\u1fbe', True), # E a P
            ('\u1fcc\u0301', True), # EP a
            ('\u0397\u1fbe\u0301', False), # E P a

            # E y
            # no triple for uppercase
            ('\u0389\u0345', True), # Ea y (NFC)
            ('\u0397\u0301\u0345', True), # E a y (NFD)
            # there is no Ey a - EP a instead
            ('\u0397\u0345\u0301', True), # E y a

            # e I
            ('\u03ae\u0399', True), # ea I (NFC)
            ('\u03b7\u0301\u0399', True), # e a I (NFD)
            ('\u03b7\u038a', False), # e Ia (NFC)
            ('\u03b7\u0399\u0301', False), # e I a (NFD)

            # e i
            ('\u03ae\u03b9', True), # ea i (NFC)
            ('\u03b7\u0301\u03b9', True), # e a i (NFD)
            ('\u03b7\u03af', False), # e ia (NFC)
            ('\u03b7\u03b9\u0301', False), # e i a (NFD)

            # e P (note P always NFx's to i)
            ('\u03ae\u1fbe', True), # ea P
            ('\u03b7\u0301\u1fbe', True), # e a P
            # there is no eP a - ey a instead
            ('\u03b7\u1fbe\u0301', False), # e P a

            # ey, e y
            ('\u1fc4', True), # eay (NFC)
            ('\u03ae\u0345', True), # ea y
            ('\u03b7\u0301\u0345', True), # e a y (NFD)
            ('\u1fc3\u0301', True), # ey a
            ('\u03b7\u0345\u0301', True), # e y a
        ]
        n = ['ηί', 'ήι']
        assert len(n[0]) == 2
        assert len(n[1]) == 2
        for a, c in strings:
            assert unicodedata.normalize('NFC', unicodedata.normalize('NFD', a).casefold()) == n[c]
            d = CaseInsensitiveDict({a: 1})
            for b, e in strings:
                assert (b in d) == (c == e)

    @xfail_if(sys.version_info[:2] <= (3, 4) or '__pypy__' in sys.modules and sys.pypy_version_info[:2] <= (5, 7))
    def test_cherokee(self):
        assert CaseInsensitiveDict({'ꭰ': 1}) == {'ꭰ': 1}
        assert CaseInsensitiveDict({'ꭰ': 1}) == {'Ꭰ': 1}
        assert CaseInsensitiveDict({'Ꭰ': 1}) == {'ꭰ': 1}
        assert CaseInsensitiveDict({'Ꭰ': 1}) == {'Ꭰ': 1}

    def test_mut(self):
        d = CaseInsensitiveDict()
        assert list(d.items()) == []
        d['A'] = 1
        assert list(d.items()) == [('A', 1)]
        d['B'] = 2
        assert list(d.items()) == [('A', 1), ('B', 2)]
        d['a'] = 3
        assert list(d.items()) == [('A', 3), ('B', 2)]
        del d['b']

    def test_norm(self):
        assert 'à' in CaseInsensitiveDict({'a\u0300': 1})
        assert 'à' in CaseInsensitiveDict({'A\u0300': 1})
        assert 'a\u0301\u0300' not in CaseInsensitiveDict({'a\u0300\u0301': 1})
        assert 'a\u0316\u0300' in CaseInsensitiveDict({'a\u0300\u0316': 1})
        assert 'क़' in CaseInsensitiveDict({'क़': 1})
        assert '⫝̸' in CaseInsensitiveDict({'⫝\u0338': 1})
        assert 'Ω' in CaseInsensitiveDict({'Ω': 1})
        assert '\u0344' in CaseInsensitiveDict({'\u0308\u0301': 1})
        assert 'Å' in CaseInsensitiveDict({'Å': 1})

    def test_ord(self):
        assert CaseInsensitiveDict(a=1) == OrderedDict({'A': 1})
        # This can only work because OrderedDict.__eq__ returns NotImplemented
        assert OrderedDict({'a': 1}) == CaseInsensitiveDict(A=1)
