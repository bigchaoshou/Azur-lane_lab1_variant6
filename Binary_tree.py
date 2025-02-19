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

    # add
    def add(self, key, value):
        """在字典中插入键值对"""
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self._add_recursive(self.root, key, value)
        self._size += 1

    def _add_recursive(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(key, value)
            else:
                self._add_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(key, value)
            else:
                self._add_recursive(node.right, key, value)
        else:
            node.value = value  # 如果 key 已存在，更新 value

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
        """删除 key 并维护 BST 结构"""
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

    # member
    def member(self, value):
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
            if predicate(node.key, node.value):
                result.append((node.key, node.value))
            self._filter_recursive(node.left, predicate, result)
            self._filter_recursive(node.right, predicate, result)

    # map
    def map(self, func):
        """对字典中的每个元素应用指定的函数"""
        result = []
        self._map_recursive(self.root, func, result)
        return result

    def _map_recursive(self, node, func, result):
        if node:
            result.append(func(node.key, node.value))
            self._map_recursive(node.left, func, result)
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
        """将另一个 BSTDictionary 合并到当前字典中，保留已有 key"""
        if not isinstance(other, BSTDictionary) or other.root is None:
            return
        def add_if_absent(node):
            if node is not None:
                if self.search(node.key) is None:
                    self.add(node.key, node.value)
                add_if_absent(node.left)
                add_if_absent(node.right)
        add_if_absent(other.root)

# 测试代码
if __name__ == "__main__":
    lst = BSTDictionary()
    lst.add(1, "A")
    lst.add(2, "B")
    lst.add(3, "C")

    # 删除元素
    print("Before remove:")
    print(lst.to_list())
    lst.remove(2)
    print("After remove:")
    print(lst.to_list())

    # 过滤
    print("\nFiltered (even keys):")
    even = lst.filter(lambda k, v: k % 2 == 0)
    print(even)

    # 映射
    print("\nMapped (increment keys by 1):")
    incremented = lst.map(lambda k, v: (k + 1, v))
    print(incremented)

    # 归约
    print("\nReduced (sum of keys):")
    total = lst.reduce(lambda acc, k, v: acc + k, 0)
    print(total)

    # 反转
    print("\nReversed List:")
    reversed_lst = lst.reverse()
    print(reversed_lst)

    # 转换为列表
    print("\nList form:")
    lst_list = lst.to_list()
    print(lst_list)

    # 创建空字典
    empty_dict = BSTDictionary.empty()
    print("\nEmpty dictionary:")
    print(empty_dict.to_list())

    # 合并字典
    print("\nConcatenate with another dictionary:")
    lst2 = BSTDictionary()
    lst2.add(4, "D")
    lst2.add(5, "E")
    lst.concat(lst2)
    print(lst.to_list())
