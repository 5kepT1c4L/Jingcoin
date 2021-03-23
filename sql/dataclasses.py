from collections.abc import MutableMapping as MM
from dataclasses import dataclass, field
from typing import MutableMapping


@dataclass(order=True)
class User:
    user_id: int = field(compare=False)
    stock: int = field(compare=True)
    balance: int = field(compare=True)
    _changed: bool = field(default=False, init=False, repr=False, hash=False, compare=False)
    _new: bool = field(default=True, init=False, repr=False, hash=False, compare=False)

    def __setattr__(self, key: str, value):
        if not key.startswith("_"):
            self._changed = True


class ChangeDict(MM, MutableMapping[str, str]):
    __slots__ = ("dict", "changed")

    def __init__(self, iterable=None):
        self.dict = dict(iterable) if iterable else {}
        self.changed = False

    def __setitem__(self, k, v):
        self.dict[k] = v
        self.changed = True

    def __delitem__(self, v):
        del self.dict[v]
        self.changed = True

    def __getitem__(self, k):
        return self.dict[k]

    def __len__(self) -> int:
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)

    def __repr__(self):
        return repr(self.dict)
