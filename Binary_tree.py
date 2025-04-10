from typing import (
    Optional, List, Tuple, Callable, TypeVar, Iterator, Protocol, Generic,
    TypedDict, cast, overload
)
from typing_extensions import Self


# 定义支持比较操作的泛型协议
class SupportsRichComparison(Protocol[K]):
    def __lt__(self: K, other: K) -> bool: ...

    def __le__(self: K, other: K) -> bool: ...

    def __gt__(self: K, other: K) -> bool: ...

    def __ge__(self: K, other: K) -> bool: ...


KT = TypeVar('KT', bound=SupportsRichComparison)  # Key类型必须支持比较操作
VT = TypeVar('VT')  # 值类型
AccT = TypeVar('AccT')  # 累加器类型


# 使用更严格的TypedDict定义树节点
class TreeNode(TypedDict, Generic[KT, VT]):
    key: KT
    value: VT
    left: Optional['TreeNode[KT, VT]']
    right: Optional['TreeNode[KT, VT]']


class BSTDictionary(Generic[KT, VT]):
    def __init__(self) -> None:
        self.root: Optional[TreeNode[KT, VT]] = None
        self._size: int = 0

    def size(self) -> int:
        return self._size

    def add(self, key: KT, value: VT) -> None:
        if self.root is None:
            self.root = TreeNode(key=key, value=value, left=None, right=None)
            self._size += 1
        else:
            if self._add_recursive(self.root, key, value):
                self._size += 1

    def _add_recursive(self, node: TreeNode[KT, VT], key: KT, value: VT) -> bool:
        if key < node['key']:  # 类型安全：已知KT支持比较操作
            left = node['left']
            if left is None:
                node['left'] = TreeNode(key=key, value=value, left=None, right=None)
                return True
            return self._add_recursive(left, key, value)
        elif key > node['key']:
            right = node['right']
            if right is None:
                node['right'] = TreeNode(key=key, value=value, left=None, right=None)
                return True
            return self._add_recursive(right, key, value)
        else:
            node['value'] = value
            return False

    def _find_min(self, node: TreeNode[KT, VT]) -> TreeNode[KT, VT]:
        while node['left'] is not None:
            node = node['left']
        return node

    @overload
    def search(self, key: KT) -> Optional[VT]:
        ...

    def search(self, key: KT) -> Optional[VT]:
        node = self._search_recursive(self.root, key)
        return node['value'] if node else None

    def _search_recursive(
            self,
            node: Optional[TreeNode[KT, VT]],
            key: KT
    ) -> Optional[TreeNode[KT, VT]]:
        if node is None or node['key'] == key:
            return node
        return self._search_recursive(
            node['left'] if key < node['key'] else node['right'],
            key
        )

    def set(self, key: KT, new_value: VT) -> None:
        node = self._search_recursive(self.root, key)
        if node:
            node['value'] = new_value

    def remove(self, key: KT) -> None:
        if self.search(key) is not None:
            self.root = self._delete_recursive(self.root, key)
            self._size -= 1

    def _delete_recursive(
            self,
            node: Optional[TreeNode[KT, VT]],
            key: KT
    ) -> Optional[TreeNode[KT, VT]]:
        if node is None:
            return None

        if key < node['key']:
            node['left'] = self._delete_recursive(node['left'], key)
        elif key > node['key']:
            node['right'] = self._delete_recursive(node['right'], key)
        else:
            if node['left'] is None:
                return node['right']
            if node['right'] is None:
                return node['left']

            temp = self._find_min(cast(TreeNode[KT, VT], node['right']))
            node['key'], node['value'] = temp['key'], temp['value']
            node['right'] = self._delete_recursive(node['right'], temp['key'])

        return node

    def member(self, value: VT) -> bool:
        return self._member_recursive(self.root, value)

    def _member_recursive(
            self,
            node: Optional[TreeNode[KT, VT]],
            value: VT
    ) -> bool:
        if node is None:
            return False
        return (
                node['value'] == value
                or self._member_recursive(node['left'], value)
                or self._member_recursive(node['right'], value)
        )

    def reverse(self) -> List[Tuple[KT, VT]]:
        return self.to_list()[::-1]

    @classmethod
    def from_list(cls, lst: List[Tuple[KT, VT]]) -> Self:
        bst_dict = cls()
        for key, value in lst:
            bst_dict.add(key, value)
        return bst_dict

    def to_list(self) -> List[Tuple[KT, VT]]:
        result: List[Tuple[KT, VT]] = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(
            self,
            node: Optional[TreeNode[KT, VT]],
            result: List[Tuple[KT, VT]]
    ) -> None:
        if node is not None:
            self._inorder_traversal(node['left'], result)
            result.append((node['key'], node['value']))
            self._inorder_traversal(node['right'], result)

    def filter(
            self,
            predicate: Callable[[KT, VT], bool]
    ) -> List[Tuple[KT, VT]]:
        result: List[Tuple[KT, VT]] = []
        self._filter_recursive(self.root, predicate, result)
        return sorted(result, key=lambda x: x[0])

    def _filter_recursive(
            self,
            node: Optional[TreeNode[KT, VT]],
            predicate: Callable[[KT, VT], bool],
            result: List[Tuple[KT, VT]]
    ) -> None:
        if node:
            if predicate(node['key'], node['value']):
                result.append((node['key'], node['value']))
            self._filter_recursive(node['left'], predicate, result)
            self._filter_recursive(node['right'], predicate, result)

    def map(
            self,
            func: Callable[[KT, VT], Tuple[KT, VT]]
    ) -> List[Tuple[KT, VT]]:
        result: List[Tuple[KT, VT]] = []
        self._map_recursive(self.root, func, result)
        return BSTDictionary.from_list(result).to_list()

    def _map_recursive(
            self,
            node: Optional[TreeNode[KT, VT]],
            func: Callable[[KT, VT], Tuple[KT, VT]],
            result: List[Tuple[KT, VT]]
    ) -> None:
        if node:
            result.append(func(node['key'], node['value']))
            self._map_recursive(node['left'], func, result)
            self._map_recursive(node['right'], func, result)

    def reduce(
            self,
            func: Callable[[AccT, KT, VT], AccT],
            initial_value: AccT
    ) -> AccT:
        return self._reduce_recursive(self.root, func, initial_value)

    def _reduce_recursive(
            self,
            node: Optional[TreeNode[KT, VT]],
            func: Callable[[AccT, KT, VT], AccT],
            value: AccT
    ) -> AccT:
        if node is None:
            return value
        value = self._reduce_recursive(node['left'], func, value)
        value = func(value, node['key'], node['value'])
        return self._reduce_recursive(node['right'], func, value)

    def __iter__(self) -> Iterator[Tuple[KT, VT]]:
        self._iter_stack: List[TreeNode[KT, VT]] = []
        self._push_left(self.root)
        return self

    def __next__(self) -> Tuple[KT, VT]:
        if not self._iter_stack:
            raise StopIteration
        node = self._iter_stack.pop()
        self._push_left(node['right'])
        return node['key'], node['value']

    def _push_left(self, node: Optional[TreeNode[KT, VT]]) -> None:
        while node:
            self._iter_stack.append(node)
            node = node['left']

    @staticmethod
    def empty() -> Self:
        return BSTDictionary()

    def concat(self, other: Self) -> Self:
        if not isinstance(other, BSTDictionary) or other.root is None:
            return self

        def add_other_tree(node: Optional[TreeNode[KT, VT]]) -> None:
            if node:
                self.add(node['key'], node['value'])
                add_other_tree(node['left'])
                add_other_tree(node['right'])

        add_other_tree(other.root)
        return self