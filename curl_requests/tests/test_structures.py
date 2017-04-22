from collections import OrderedDict
import sys
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
