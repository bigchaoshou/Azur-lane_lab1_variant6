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

    # toList
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

    # map
    def map(self, func):
        """对所有值应用函数"""
        self._map_recursive(self.root, func)

    def _map_recursive(self, node, func):
        if node is not None:
            node.value = func(node.value)
            self._map_recursive(node.left, func)
            self._map_recursive(node.right, func)

    # reduce
    def reduce(self, func, initial_state):
        """对所有 (key, value) 进行 reduce 计算"""
        return self._reduce_recursive(self.root, func, initial_state)

    def _reduce_recursive(self, node, func, state):
        if node is not None:
            state = self._reduce_recursive(node.left, func, state)
            state = func(state, node.value)
            state = self._reduce_recursive(node.right, func, state)
        return state

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

    # delete
    def delete(self, key):
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

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    # set (update)
    def set(self, key, new_value):
        """更新 key 的 value"""
        node = self._search_recursive(self.root, key)
        if node:
            node.value = new_value

    # is a member
    def member(self, value):
        """检查是否有节点的值等于给定值"""
        return self._member_recursive(self.root, value)

    def _member_recursive(self, node, value):
        if node is None:
            return False
        if node.value == value:
            return True
        return self._member_recursive(node.left, value) or self._member_recursive(node.right, value)

    # inorder traversal
    def inorder_traversal(self):
        """中序遍历（升序输出所有键值对）"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is not None:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)

    # concat (合并 BST，但不覆盖已有的 key)
    def concat(self, other):
        """将另一个 BSTDictionary 合并到当前字典中，保留已有 key"""
        def add_if_absent(node):
            if node is not None:
                if self.search(node.key) is None:  # 只有 key 不存在才添加
                    self.add(node.key, node.value)
                add_if_absent(node.left)
                add_if_absent(node.right)

        add_if_absent(other.root)

    # iterator
    def iter_from(self, start_key):
        """从 `start_key` 开始进行中序遍历"""
        stack = []
        node = self.root
        found = False

        while stack or node:
            while node:
                stack.append(node)
                node = node.left

            node = stack.pop()

            if node.key >= start_key:
                found = True

            if found:
                yield (node.key, node.value)

            node = node.right


class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


# 示例使用
if __name__ == '__main__':
    d1 = BSTDictionary()
    d1.add(1, 2)
    d1.add(3, 4)

    d2 = BSTDictionary()
    d2.add(2, 3)
    d2.add(4, 5)
    d2.add(3, 5)
    # 使用 concat 合并字典
    d1.concat(d2)

    # 使用 iterator 迭代
    print("=== 从 key = 3 开始迭代 ===")
    for key, value in d1.iter_from(3):
        print(f"Key: {key}, Value: {value}")

    print(f"合并后的字典大小: {d1.size()}")
