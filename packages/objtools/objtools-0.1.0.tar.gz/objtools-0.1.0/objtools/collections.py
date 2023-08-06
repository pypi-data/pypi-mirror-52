from typing import (
    Mapping, MutableMapping, Sequence, Set,
    Iterable, Iterator, ByteString, Any,
)


def namespacify(value: Any) -> Any:
    if isinstance(value, Namespace):
        return value
    if isinstance(value, Mapping):
        return Namespace(value)
    if isinstance(value, (str, ByteString)):
        # Do not treat strings and bytestrings as normal sequences
        return value
    if isinstance(value, Sequence):
        return list(map(namespacify, value))
    if isinstance(value, Set):
        return set(map(namespacify, value))
    if isinstance(value, Iterable):
        return map(namespacify, value)
    return value


class Namespace(MutableMapping):

    def __init__(self, *args: Iterable, **kwargs: Any):
        for iterable in (*args, kwargs):
            if isinstance(iterable, Mapping):
                iterable = iterable.items()
            for k, v in iterable:
                setattr(self, k, v)

    def __getitem__(self, name: Any) -> Any:
        try:
            attr = getattr(self, name)
        except AttributeError:
            raise KeyError(repr(name))
        return namespacify(attr)

    def __iter__(self) -> Iterator:
        return iter(self.__dict__)

    def __len__(self) -> int:
        return len(self.__dict__)

    def __repr__(self) -> str:
        return '{}({!r})'.format(self.__class__.__name__, self.__dict__)

    def __str__(self) -> str:
        return str(self.__dict__)

    def copy(self) -> 'Namespace':
        return self.__class__(self.__dict__)

    def __setitem__(self, name: Any, value: Any) -> None:
        setattr(self, name, value)

    def __delitem__(self, name: Any) -> None:
        try:
            delattr(self, name)
        except AttributeError:
            raise KeyError(repr(name))
