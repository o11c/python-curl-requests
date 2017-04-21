# Ick, python2 compatibility

class ExtensibleEnumMeta(type):
    def __new__(mcls, name, bases, dct):
        dct.setdefault('__slots__', ())
        cls = type.__new__(mcls, name, bases, dct)
        cls._by_value = {}
        cls._by_name = {}
        return cls

    def __contains__(cls, idx):
        return idx in cls._by_value

    def __call__(cls, idx, name=None):
        assert isinstance(idx, int)
        assert name is None or isinstance(name, str)
        try:
            self = cls._by_value[idx]
        except KeyError:
            # Set self._name only on the first instance.
            assert name not in cls._by_name
            self = type.__call__(cls, idx, name)
            cls._by_value[idx] = self
        if name is not None:
            self._names.add(name)
            name = name.casefold()
            name = name.replace(' ', '_').replace('-', '_').replace('\'', '')
            if name not in cls._by_name:
                cls._by_name[name] = self
                setattr(cls, name.lower(), self)
                setattr(cls, name.upper(), self)
        return self


class ExtensibleEnum(object):
    def __init__(self, idx, name):
        self._idx = idx
        self._name = name
        self._names = set()

    def __repr__(self):
        cls = self.__class__
        cls_name = '%s.%s' % (cls.__module__, getattr(cls, '__qualname__', cls.__name__))
        if self._name is None:
            return '<%s %d>' % (cls_name, self._idx)
        return '<%s %d %s>' % (cls_name, self._idx, self._name)

    def __eq__(self, other):
        if isinstance(other, ExtensibleEnum):
            other = other._idx
        return self._idx == other
ExtensibleEnum = ExtensibleEnumMeta(ExtensibleEnum.__name__, ExtensibleEnum.__bases__, dict(ExtensibleEnum.__dict__, __slots__ = ('_idx', '_name', '_names')))
