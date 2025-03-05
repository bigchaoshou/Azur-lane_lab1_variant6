class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BSTDictionary:
    def __init__(self):
        self.root = None
        self._size = 0

    def size(self):
        return self._size

    def add(self, key, value):
        if self.root is None:
            self.root = BSTNode(key, value)
            self._size += 1
        else:
            if self._add_recursive(self.root, key, value):
                self._size += 1

    def _add_recursive(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, value)
                return True
            else:
                return self._add_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, value)
                return True
            else:
                return self._add_recursive(node.right, key, value)
        else:
            node.value = value
            return False

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def search(self, key):
        node = self._search_recursive(self.root, key)
        return node.value if node else None

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def set(self, key, new_value):
        node = self._search_recursive(self.root, key)
        if node:
            node.value = new_value

    def remove(self, key):
        if self.search(key) is not None:
            self.root = self._delete_recursive(self.root, key)
            self._size -= 1

    def _delete_recursive(self, node, key):
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_min(node.right)
            node.key, node.value = temp.key, temp.value
            node.right = self._delete_recursive(node.right, temp.key)
        return node

    def member(self, value):
        return self._member_recursive(self.root, value)

    def _member_recursive(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        return (self._member_recursive(node.left, value) or
                self._member_recursive(node.right, value))

    def reverse(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result[::-1]

    @classmethod
    def from_list(cls, lst):
        bst_dict = cls()
        for key, value in lst:
            bst_dict.add(key, value)
        return bst_dict

    def to_list(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node is not None:
            self._inorder_traversal(node.left, result)
            result.append((node.key, node.value))
            self._inorder_traversal(node.right, result)

    def filter(self, predicate):
        result = []
        self._filter_recursive(self.root, predicate, result)
        return sorted(result, key=lambda x: x[0])

    def _filter_recursive(self, node, predicate, result):
        if node:
            if predicate(node.key, node.value):
                result.append((node.key, node.value))
            self._filter_recursive(node.left, predicate, result)
            self._filter_recursive(node.right, predicate, result)

    def map(self, func):
        result = []
        self._map_recursive(self.root, func, result)
        return BSTDictionary.from_list(result).to_list()

    def _map_recursive(self, node, func, result):
        if node:
            result.append(func(node.key, node.value))
            self._map_recursive(node.left, func, result)
            self._map_recursive(node.right, func, result)

    def reduce(self, func, initial_value):
        return self._reduce_recursive(self.root, func, initial_value)

    def _reduce_recursive(self, node, func, value):
        if node is None:
            return value
        value = self._reduce_recursive(node.left, func, value)
        value = func(value, node.key, node.value)
        value = self._reduce_recursive(node.right, func, value)
        return value

    def __iter__(self):
        self._iter_stack = []
        self._push_left(self.root)
        return self

    def __next__(self):
        if not self._iter_stack:
            raise StopIteration
        node = self._iter_stack.pop()
        self._push_left(node.right)
        return node.key, node.value

    def _push_left(self, node):
        while node:
            self._iter_stack.append(node)
            node = node.left

    @classmethod
    def empty(cls):
        return cls()

    def concat(self, other):
        if not isinstance(other, BSTDictionary) or other.root is None:
            return self

        def add_or_update(node):
            if node is not None:
                self.add(node.key, node.value)
                add_or_update(node.left)
                add_or_update(node.right)
        add_or_update(other.root)
        return self
