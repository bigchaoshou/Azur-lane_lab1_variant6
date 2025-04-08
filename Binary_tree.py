from __future__ import annotations
from typing import Any, Callable, Generic, Iterator, Optional, Tuple, TypeVar, Union
from typing_extensions import Protocol

class SupportsRichComparison(Protocol):
    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

KT = TypeVar("KT", bound=SupportsRichComparison)
VT = TypeVar("VT")
AccT = TypeVar("AccT")

class BinaryTreeDict(Generic[KT, VT]):
    def __init__(self, key: Optional[KT] = None, value: Optional[VT] = None,
                 left: Optional[BinaryTreeDict[KT, VT]] = None,
                 right: Optional[BinaryTreeDict[KT, VT]] = None):
        self.tree = {
            'key': key,
            'value': value,
            'left': left,
            'right': right
        }

    def is_empty(self) -> bool:
        return self.tree['key'] is None

    def add(self, key: KT, value: VT) -> BinaryTreeDict[KT, VT]:
        if self.is_empty():
            return BinaryTreeDict(key, value, empty(), empty())
        if key == self.tree['key']:
            return BinaryTreeDict(key, value, self.tree['left'], self.tree['right'])
        elif key < self.tree['key']:
            return BinaryTreeDict(self.tree['key'], self.tree['value'], self.tree['left'].add(key, value), self.tree['right'])
        else:
            return BinaryTreeDict(self.tree['key'], self.tree['value'], self.tree['left'], self.tree['right'].add(key, value))

    def search(self, key: KT) -> Optional[VT]:
        if self.is_empty():
            return None
        if key == self.tree['key']:
            return self.tree['value']
        elif key < self.tree['key']:
            return self.tree['left'].search(key)
        else:
            return self.tree['right'].search(key)

    def member(self, key: KT) -> bool:
        return self.search(key) is not None

    def remove(self, key: KT) -> BinaryTreeDict[KT, VT]:
        if self.is_empty():
            return self
        if key < self.tree['key']:
            return BinaryTreeDict(self.tree['key'], self.tree['value'], self.tree['left'].remove(key), self.tree['right'])
        elif key > self.tree['key']:
            return BinaryTreeDict(self.tree['key'], self.tree['value'], self.tree['left'], self.tree['right'].remove(key))
        else:
            if self.tree['left'].is_empty():
                return self.tree['right']
            if self.tree['right'].is_empty():
                return self.tree['left']
            min_key, min_value = self.tree['right']._find_min()
            return BinaryTreeDict(min_key, min_value, self.tree['left'], self.tree['right'].remove(min_key))

    def _find_min(self) -> Tuple[KT, VT]:
        if self.tree['left'].is_empty():
            return (self.tree['key'], self.tree['value'])
        return self.tree['left']._find_min()

    def to_list(self) -> list[Tuple[KT, VT]]:
        if self.is_empty():
            return []
        return self.tree['left'].to_list() + [(self.tree['key'], self.tree['value'])] + self.tree['right'].to_list()

    @staticmethod
    def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
        tree = empty()
        for k, v in items:
            tree = tree.add(k, v)
        return tree

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, BinaryTreeDict) and self.to_list() == other.to_list()

    def __str__(self) -> str:
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in self.to_list()) + "}"

    def __iter__(self) -> Iterator[KT]:
        for k, _ in self.to_list():
            yield k

    def map(self, f: Callable[[KT, VT], Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
        return BinaryTreeDict.from_list([f(k, v) for k, v in self.to_list()])

    def filter(self, f: Callable[[KT, VT], bool]) -> BinaryTreeDict[KT, VT]:
        return BinaryTreeDict.from_list([(k, v) for k, v in self.to_list() if f(k, v)])

    def reduce(self, f: Callable[[AccT, KT, VT], AccT], acc: AccT) -> AccT:
        for k, v in self.to_list():
            acc = f(acc, k, v)
        return acc

def empty() -> BinaryTreeDict[Any, Any]:
    return BinaryTreeDict()

def cons(key: KT, value: VT, tree: BinaryTreeDict[KT, VT]) -> BinaryTreeDict[KT, VT]:
    return tree.add(key, value)

def concat(t1: BinaryTreeDict[KT, VT], t2: BinaryTreeDict[KT, VT]) -> BinaryTreeDict[KT, VT]:
    return BinaryTreeDict.from_list(t1.to_list() + t2.to_list())

def length(tree: BinaryTreeDict[KT, VT]) -> int:
    return len(tree.to_list())

def member(key: KT, tree: BinaryTreeDict[KT, VT]) -> bool:
    return tree.member(key)

def remove(tree: BinaryTreeDict[KT, VT], key: KT) -> BinaryTreeDict[KT, VT]:
    return tree.remove(key)

def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
    return BinaryTreeDict.from_list(items)

def to_list(tree: BinaryTreeDict[KT, VT]) -> list[Tuple[KT, VT]]:
    return tree.to_list()
