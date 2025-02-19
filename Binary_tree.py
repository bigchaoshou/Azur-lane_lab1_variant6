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

    # size
    def size(self):
        return self._size

    def add(self, key, value):
        """插入键值对，仅在键不存在时增加大小"""
        if self.root is None:
            self.root = BSTNode(key, value)
            self._size += 1
            return
        # 递归插入，返回是否插入了新节点
        if self._add_recursive(self.root, key, value):
            self._size += 1

    def _add_recursive(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, value)
                return True  # 新节点插入成功
            else:
                return self._add_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, value)
                return True  # 新节点插入成功
            else:
                return self._add_recursive(node.right, key, value)
        else:
            node.value = value  # 更新现有键的值
            return False  # 未插入新节点

    # search
    def search(self, key):
        """查找 key，返回对应的 value"""
        node = self._search_recursive(self.root, key)
        return node.value if node else None

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)


    # set
    def set(self, key, new_value):
        """更新 key 的 value"""
        node = self._search_recursive(self.root, key)
        if node:
            node.value = new_value

    # remove
    def remove(self, key):

        self.root, deleted = self._delete_recursive(self.root, key)
        if deleted:
            self._size -= 1

    def _delete_recursive(self, node, key):
        if node is None:
            return node, False  # 未找到 key，返回 False

        deleted = False
        if key < node.key:
            node.left, deleted = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right, deleted = self._delete_recursive(node.right, key)
        else:
            # 找到 key，删除节点
            if node.left is None:
                return node.right, True  # 删除成功
            elif node.right is None:
                return node.left, True
            # 找到右子树的最小节点替换
            temp = self._find_min(node.right)
            node.key, node.value = temp.key, temp.value
            # 删除右子树中的原最小节点
            node.right, _ = self._delete_recursive(node.right, temp.key)
            deleted = True
        return node, deleted

    def _find_min(self, node):
        """找到子树的最小节点"""
        while node.left is not None:
            node = node.left
        return node

    # member
    def is_member(self, value):
        """检查是否有节点的值等于给定值"""
        return self._member_recursive(self.root, value)

    def _member_recursive(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        return self._member_recursive(node.left, value) or self._member_recursive(node.right, value)

    # reverse
    def reverse(self):
        """反转字典的顺序"""
        result = []
        self._inorder_traversal(self.root, result)
        return result[::-1]  # 反转列表

    # from_list
    @classmethod
    def from_list(cls, lst):
        """根据给定的 (key, value) 元组列表，创建一个 BSTDictionary"""
        bst_dict = cls()
        for key, value in lst:
            bst_dict.add(key, value)
        return bst_dict

    # to_list
    def to_list(self):
        """按序遍历返回 (key, value) 列表"""
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node is not None:
            self._inorder_traversal(node.left, result)
            result.append((node.key, node.value))
            self._inorder_traversal(node.right, result)

    # filter
    def filter(self, predicate):
        """根据给定的条件过滤元素"""
        result = []
        self._filter_recursive(self.root, predicate, result)
        return result

    def _filter_recursive(self, node, predicate, result):
        if node:

            self._filter_recursive(node.left, predicate, result)
            if predicate(node.key, node.value):
                result.append((node.key, node.value))
            self._filter_recursive(node.right, predicate, result)

    # map
    def map(self, func):
        """对字典中的每个元素应用指定的函数"""
        result = []
        self._map_recursive(self.root, func, result)
        return result

    def _map_recursive(self, node, func, result):
        if node:
            self._map_recursive(node.left, func, result)
            result.append(func(node.key, node.value))
            self._map_recursive(node.right, func, result)

    # reduce
    def reduce(self, func, initial_value):
        """通过指定的函数对字典中的元素进行归约"""
        return self._reduce_recursive(self.root, func, initial_value)

    def _reduce_recursive(self, node, func, value):
        if node is None:
            return value
        value = self._reduce_recursive(node.left, func, value)
        value = func(value, node.key, node.value)
        value = self._reduce_recursive(node.right, func, value)
        return value

    # iterator
    def __iter__(self):
        """返回一个迭代器，支持 `for key, value in d:`"""
        self._iter_stack = []
        self._push_left(self.root)
        return self

    def __next__(self):
        """返回下一个 (key, value)"""
        if not self._iter_stack:
            raise StopIteration
        node = self._iter_stack.pop()
        self._push_left(node.right)
        return node.key, node.value

    def _push_left(self, node):
        """辅助方法：将左子树压入栈"""
        while node:
            self._iter_stack.append(node)
            node = node.left

    # empty
    @classmethod
    def empty(cls):
        """返回一个空的 BSTDictionary"""
        return cls()

    # concat
    def concat(self, other):
        """将另一个 BSTDictionary 合并到当前字典，覆盖重复的键"""
        if not isinstance(other, BSTDictionary) or other.root is None:
            return
        def add_or_update(node):
            if node is not None:
                # 无论键是否存在，直接调用 add 方法（已存在的键会更新值）
                self.add(node.key, node.value)
                add_or_update(node.left)
                add_or_update(node.right)
        add_or_update(other.root)