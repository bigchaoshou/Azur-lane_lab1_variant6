from __future__ import annotations
from typing import (
    Any, Optional, Callable, List, Tuple,
    Iterator, Iterable, Generic, TypeVar,
    Union, Mapping
)
from typing_extensions import Protocol  # 新增导入


class SupportsRichComparison(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...


KT = TypeVar("KT", bound=SupportsRichComparison)
VT = TypeVar("VT")  # 值类型无约束
AccT = TypeVar("AccT")


class DictDictionary(Generic[KT, VT]):
    def __init__(self) -> None:
        self._dict: dict[KT, VT] = {}

    def size(self) -> int:
        return len(self._dict)

    def add(self, key: KT, value: VT) -> None:
        """Add or update key-value pair"""
        self._dict[key] = value

    def search(self, key: KT) -> Optional[VT]:
        """Search value by key"""
        return self._dict.get(key, None)

    def set(self, key: KT, new_value: VT) -> None:
        """Update existing key's value"""
        if key in self._dict:
            self._dict[key] = new_value

    def remove(self, key: KT) -> None:
        """Remove key from dictionary"""
        if key in self._dict:
            del self._dict[key]

    def member(self, value: VT) -> bool:
        """Check if value exists"""
        return value in self._dict.values()

    def reverse(self) -> List[Tuple[KT, VT]]:
        """Get reversed sorted entries"""
        return sorted(self._dict.items(), key=lambda x: x[0], reverse=True)

    @classmethod
    def from_list(cls, lst: Iterable[Tuple[KT, VT]]) -> DictDictionary[KT, VT]:
        """Build from iterable of (key, value) pairs"""
        new_dict = cls()
        for key, value in lst:
            new_dict.add(key, value)
        return new_dict

    def to_list(self) -> List[Tuple[KT, VT]]:
        """Convert to sorted list"""
        return sorted(self._dict.items(), key=lambda x: x[0])

    def filter(
            self,
            predicate: Callable[[KT, VT], bool]
    ) -> List[Tuple[KT, VT]]:
        """Filter entries by predicate"""
        return sorted(
            [(k, v) for k, v in self._dict.items() if predicate(k, v)],
            key=lambda x: x[0]
        )

    def map(
            self,
            func: Callable[[KT, VT], Tuple[Any, Any]]
    ) -> List[Tuple[Any, Any]]:
        """Apply function to each entry"""
        return [
            func(k, v)
            for k, v in sorted(
                self._dict.items(),
                key=lambda x: x[0]
            )
        ]

    def reduce(
            self,
            func: Callable[[AccT, KT, VT], AccT],
            initial_value: AccT
    ) -> AccT:
        """Fold entries with initial value"""
        acc = initial_value
        for k, v in sorted(self._dict.items(), key=lambda x: x[0]):
            acc = func(acc, k, v)
        return acc

    def __iter__(self) -> Iterator[Tuple[KT, VT]]:
        """Sorted iterator"""
        return iter(sorted(self._dict.items(), key=lambda x: x[0]))

    @staticmethod
    def empty() -> DictDictionary[Any, Any]:
        """Create empty dictionary"""
        return DictDictionary()

    def concat(
            self,
            other: Union[DictDictionary[KT, VT], Mapping[KT, VT]]
    ) -> DictDictionary[KT, VT]:
        """Merge two dictionaries"""
        new_dict = DictDictionary[KT, VT]()
        new_dict._dict = self._dict.copy()
        new_dict._dict.update(
            dict(other.items())
            if isinstance(other, Mapping)
            else other._dict
        )
        return new_dict

    def items(self) -> Iterable[Tuple[KT, VT]]:
        """Get sorted items view"""
        return sorted(
            self._dict.items(),
            key=lambda x: x[0]
        )
