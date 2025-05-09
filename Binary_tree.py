from typing import Optional, List, Tuple, Callable, Iterator, TypedDict


class TreeNodeDict(TypedDict, total=False):
    key: int
    value: str
    left: Optional['TreeNodeDict']
    right: Optional['TreeNodeDict']


class BSTDictionary:
    def __init__(self) -> None:
        self.root: Optional[TreeNodeDict] = None
        self._size: int = 0

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BSTDictionary):
            return False

        def inorder_gen(node):
            stack = []
            while stack or node:
                while node:
                    stack.append(node)
                    node = node["left"]
                node = stack.pop()
                yield (node["key"], node["value"])
                node = node["right"]

        gen1 = inorder_gen(self.root)
        gen2 = inorder_gen(other.root)

        for pair1, pair2 in zip(gen1, gen2):
            if pair1 != pair2:
                return False

        # Check if both trees had the same number of nodes
        try:
            next(gen1)
            return False
        except StopIteration:
            pass

        try:
            next(gen2)
            return False
        except StopIteration:
            pass

        return True

    def size(self) -> int:
        return self._size

    def add(self, key: int, value: str) -> None:
        if self.root is None:
            self.root = {
                'key': key,
                'value': value,
                'left': None,
                'right': None
            }
            self._size += 1
        else:
            if self._add_recursive(self.root, key, value):
                self._size += 1

    def _add_recursive(self, node: TreeNodeDict, key: int, value: str) -> bool:
        if key < node['key']:
            if node['left'] is None:
                node['left'] = {
                    'key': key,
                    'value': value,
                    'left': None,
                    'right': None
                }
                return True
            return self._add_recursive(node['left'], key, value)
        elif key > node['key']:
            if node['right'] is None:
                node['right'] = {
                    'key': key,
                    'value': value,
                    'left': None,
                    'right': None
                }
                return True
            return self._add_recursive(node['right'], key, value)
        else:
            node['value'] = value
            return False

    def _find_min(self, node: TreeNodeDict) -> TreeNodeDict:
        while node['left'] is not None:
            node = node['left']
        return node

    def search(self, key: int) -> Optional[str]:
        node = self._search_recursive(self.root, key)
        return node['value'] if node else None

    def _search_recursive(
        self,
        node: Optional[TreeNodeDict],
        key: int
    ) -> Optional[TreeNodeDict]:
        if node is None or node['key'] == key:
            return node
        elif key < node['key']:
            return self._search_recursive(node['left'], key)
        else:
            return self._search_recursive(node['right'], key)

    def set(self, key: int, new_value: str) -> None:
        node = self._search_recursive(self.root, key)
        if node:
            node['value'] = new_value

    def remove(self, key: int) -> None:
        if self.search(key) is not None:
            self.root = self._delete_recursive(self.root, key)
            self._size -= 1

    def _delete_recursive(
        self,
        node: Optional[TreeNodeDict],
        key: int
    ) -> Optional[TreeNodeDict]:
        if node is None:
            return node
        if key < node['key']:
            node['left'] = self._delete_recursive(node['left'], key)
        elif key > node['key']:
            node['right'] = self._delete_recursive(node['right'], key)
        else:
            if node['left'] is None:
                return node['right']
            elif node['right'] is None:
                return node['left']
            temp = self._find_min(node['right'])
            node['key'], node['value'] = temp['key'], temp['value']
            node['right'] = self._delete_recursive(
                node['right'], temp['key']
            )
        return node

    def member(self, value: str) -> bool:
        return self._member_recursive(self.root, value)

    def _member_recursive(
        self,
        node: Optional[TreeNodeDict],
        value: str
    ) -> bool:
        if node is None:
            return False
        if node['value'] == value:
            return True
        return (
            self._member_recursive(node['left'], value)
            or self._member_recursive(node['right'], value)
        )

    def reverse(self) -> List[Tuple[int, str]]:
        result: List[Tuple[int, str]] = []
        self._inorder_traversal(self.root, result)
        return result[::-1]

    @classmethod
    def from_list(cls, lst: List[Tuple[int, str]]) -> 'BSTDictionary':
        bst_dict = cls()
        for key, value in lst:
            bst_dict.add(key, value)
        return bst_dict

    def to_list(self) -> List[Tuple[int, str]]:
        result: List[Tuple[int, str]] = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(
        self,
        node: Optional[TreeNodeDict],
        result: List[Tuple[int, str]]
    ) -> None:
        if node is not None:
            self._inorder_traversal(node['left'], result)
            result.append((node['key'], node['value']))
            self._inorder_traversal(node['right'], result)

    def filter(
        self,
        predicate: Callable[[int, str], bool]
    ) -> List[Tuple[int, str]]:
        result: List[Tuple[int, str]] = []
        self._filter_recursive(self.root, predicate, result)
        return sorted(result, key=lambda x: x[0])

    def _filter_recursive(
        self,
        node: Optional[TreeNodeDict],
        predicate: Callable[[int, str], bool],
        result: List[Tuple[int, str]]
    ) -> None:
        if node:
            if predicate(node['key'], node['value']):
                result.append((node['key'], node['value']))
            self._filter_recursive(node['left'], predicate, result)
            self._filter_recursive(node['right'], predicate, result)

    def map(
        self,
        func: Callable[[int, str], Tuple[int, str]]
    ) -> List[Tuple[int, str]]:
        result: List[Tuple[int, str]] = []
        self._map_recursive(self.root, func, result)
        return BSTDictionary.from_list(result).to_list()

    def _map_recursive(
        self,
        node: Optional[TreeNodeDict],
        func: Callable[[int, str], Tuple[int, str]],
        result: List[Tuple[int, str]]
    ) -> None:
        if node:
            result.append(func(node['key'], node['value']))
            self._map_recursive(node['left'], func, result)
            self._map_recursive(node['right'], func, result)

    def reduce(
        self,
        func: Callable[[str, int, str], str],
        initial_value: str
    ) -> str:
        return self._reduce_recursive(self.root, func, initial_value)

    def _reduce_recursive(
        self,
        node: Optional[TreeNodeDict],
        func: Callable[[str, int, str], str],
        value: str
    ) -> str:
        if node is None:
            return value
        value = self._reduce_recursive(node['left'], func, value)
        value = func(value, node['key'], node['value'])
        value = self._reduce_recursive(node['right'], func, value)
        return value

    def __iter__(self) -> Iterator[Tuple[int, str]]:
        self._iter_stack: List[TreeNodeDict] = []
        self._push_left(self.root)
        return self

    def __next__(self) -> Tuple[int, str]:
        if not self._iter_stack:
            raise StopIteration
        node = self._iter_stack.pop()
        self._push_left(node['right'])
        return node['key'], node['value']

    def _push_left(self, node: Optional[TreeNodeDict]) -> None:
        while node:
            self._iter_stack.append(node)
            node = node['left']

    @staticmethod
    def empty() -> 'BSTDictionary':
        return BSTDictionary()

    def concat(
        self,
        other: 'BSTDictionary'
    ) -> 'BSTDictionary':
        if (not isinstance(other, BSTDictionary) or other.root is None):
            return self

        def add_other_tree(node: Optional[TreeNodeDict]) -> None:
            if node is not None:
                self.add(node['key'], node['value'])
                add_other_tree(node['left'])
                add_other_tree(node['right'])

        add_other_tree(other.root)
        return self
