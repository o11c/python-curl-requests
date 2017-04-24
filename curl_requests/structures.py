from collections import OrderedDict
from collections.abc import Mapping, MutableMapping
import unicodedata


def _nfc(s):
    return unicodedata.normalize('NFC', s)

def _nfd(s):
    return unicodedata.normalize('NFD', s)

def _nfkc(s):
    return unicodedata.normalize('NFKC', s)

def _nfkd(s):
    return unicodedata.normalize('NFKD', s)

def _canonical_fold(s):
    return _nfd(str.casefold(_nfd(s)))

def _identifier_fold(s):
    return _nfkd(str.casefold(_nfkd(str.casefold(_nfd(s)))))


class CaseInsensitiveDict(MutableMapping):
    ''' General-purpose case-insensitive dict.

        Most implementations are flawed. See the tests.
    '''
    def __init__(*args, **kwargs):
        self, *args = args
        self._dict = OrderedDict()
        self.update(*args, **kwargs)

    def __repr__(self):
        return '%s%r' % (self.__class__.__name__, dict(self))

    def __getitem__(self, key):
        fold_key = _canonical_fold(key)
        orig_key, value = self._dict[fold_key]
        return value

    def __setitem__(self, key, value):
        fold_key = _canonical_fold(key)
        orig_key, orig_value = self._dict.get(fold_key, (None, None))
        if orig_key is not None:
            key = orig_key
        self._dict[fold_key] = (key, value)

    def __delitem__(self, key):
        fold_key = _canonical_fold(key)
        del self._dict[fold_key]

    def __iter__(self):
        for orig_key, value in self._dict.values():
            yield orig_key

    def __len__(self):
        return len(self._dict)

    def __eq__(self, other):
        absent = object()
        if not isinstance(other, Mapping):
            return NotImplemented
        if len(self) != len(other):
            return False
        for k, v in other.items():
            v2 = self.get(k, absent)
            if v2 is absent or v != v2:
                return False
        return True
