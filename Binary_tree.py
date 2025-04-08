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
    def __init__(self, node: Optional[dict] = None):
        if node is None:
            node = {'key': None, 'value': None, 'left': None, 'right': None}
        self.node = node

    def is_empty(self) -> bool:
        return self.node['key'] is None

    def add(self, key: KT, value: VT) -> None:
        """Add a new key-value pair to the tree (mutable operation)"""
        if self.is_empty():
            self.node = {'key': key, 'value': value, 'left': None, 'right': None}
        elif key == self.node['key']:
            self.node['value'] = value
        elif key < self.node['key']:
            if self.node['left'] is None:
                self.node['left'] = BinaryTreeDict({'key': key, 'value': value, 'left': None, 'right': None})
            else:
                self.node['left'].add(key, value)
        else:
            if self.node['right'] is None:
                self.node['right'] = BinaryTreeDict({'key': key, 'value': value, 'left': None, 'right': None})
            else:
                self.node['right'].add(key, value)

    def search(self, key: KT) -> Optional[VT]:
        """Search for the value corresponding to the key (mutable)"""
        if self.is_empty():
            return None
        if key == self.node['key']:
            return self.node['value']
        elif key < self.node['key']:
            return self.node['left'].search(key) if self.node['left'] else None
        else:
            return self.node['right'].search(key) if self.node['right'] else None

    def member(self, key: KT) -> bool:
        """Check if the key is in the tree"""
        return self.search(key) is not None

    def remove(self, key: KT) -> None:
        """Remove a key-value pair (mutable operation)"""
        if self.is_empty():
            return
        if key < self.node['key']:
            if self.node['left']:
                self.node['left'].remove(key)
        elif key > self.node['key']:
            if self.node['right']:
                self.node['right'].remove(key)
        else:
            if self.node['left'] is None and self.node['right'] is None:
                self.node = {'key': None, 'value': None, 'left': None, 'right': None}
            elif self.node['left'] is None:
                self.node = self.node['right'].node
            elif self.node['right'] is None:
                self.node = self.node['left'].node
            else:
                min_key, min_value = self.node['right']._find_min()
                self.node['key'] = min_key
                self.node['value'] = min_value
                self.node['right'].remove(min_key)

    def _find_min(self) -> Tuple[KT, VT]:
        """Find the minimum key-value pair in the tree"""
        if self.node['left'] is None:
            return self.node['key'], self.node['value']
        return self.node['left']._find_min()

    def to_list(self) -> list[Tuple[KT, VT]]:
        """Convert the tree to a sorted list of key-value pairs"""
        if self.is_empty():
            return []
        result = []
        if self.node['left']:
            result.extend(self.node['left'].to_list())
        result.append((self.node['key'], self.node['value']))
        if self.node['right']:
            result.extend(self.node['right'].to_list())
        return result

    @staticmethod
    def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
        """Create a tree from a list of key-value pairs"""
        tree = BinaryTreeDict()
        for k, v in items:
            tree.add(k, v)
        return tree

    def __eq__(self, other: Any) -> bool:
        """Check if two trees are equal"""
        return isinstance(other, BinaryTreeDict) and self.to_list() == other.to_list()

    def __str__(self) -> str:
        """String representation of the tree"""
        return "{" + ", ".join(f"{repr(k)}: {repr(v)}" for k, v in self.to_list()) + "}"

    def __iter__(self) -> Iterator[KT]:
        """Iterator for the keys in the tree"""
        for k, _ in self.to_list():
            yield k

    def map(self, f: Callable[[KT, VT], Tuple[KT, VT]]) -> None:
        """Apply a function to each key-value pair (mutable operation)"""
        for k, v in self.to_list():
            new_key, new_value = f(k, v)
            self.remove(k)
            self.add(new_key, new_value)

    def filter(self, f: Callable[[KT, VT], bool]) -> None:
        """Filter the tree by a predicate (mutable operation)"""
        keys_to_remove = [k for k, v in self.to_list() if not f(k, v)]
        for key in keys_to_remove:
            self.remove(key)

    def reduce(self, f: Callable[[AccT, KT, VT], AccT], acc: AccT) -> AccT:
        """Fold the tree with an accumulator (mutable operation)"""
        for k, v in self.to_list():
            acc = f(acc, k, v)
        return acc


def empty() -> BinaryTreeDict[Any, Any]:
    """Create an empty tree"""
    return BinaryTreeDict()


def cons(key: KT, value: VT, tree: BinaryTreeDict[KT, VT]) -> None:
    """Add a key-value pair to the tree (mutable)"""
    tree.add(key, value)


def concat(t1: BinaryTreeDict[KT, VT], t2: BinaryTreeDict[KT, VT]) -> None:
    """Concatenate two trees into a new one (mutable)"""
    for k, v in t2.to_list():
        t1.add(k, v)


def length(tree: BinaryTreeDict[KT, VT]) -> int:
    """Get the length of the tree (mutable)"""
    return len(tree.to_list())


def member(key: KT, tree: BinaryTreeDict[KT, VT]) -> bool:
    """Check if a key is in the tree (mutable)"""
    return tree.member(key)


def remove(tree: BinaryTreeDict[KT, VT], key: KT) -> None:
    """Remove a key-value pair from the tree (mutable)"""
    tree.remove(key)


def from_list(items: list[Tuple[KT, VT]]) -> BinaryTreeDict[KT, VT]:
    """Create a tree from a list of key-value pairs (mutable)"""
    tree = BinaryTreeDict()
    for k, v in items:
        tree.add(k, v)
    return tree


def to_list(tree: BinaryTreeDict[KT, VT]) -> list[Tuple[KT, VT]]:
    """Convert the tree to a list of key-value pairs (mutable)"""
    return tree.to_list()
