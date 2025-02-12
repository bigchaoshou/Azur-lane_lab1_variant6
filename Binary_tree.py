class TreeNode:
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
        """在字典中插入键值对"""
        if self.root is None:
            self.root = TreeNode(key, value)
        else:
            self._add_recursive(self.root, key, value)
        self._size += 1

    def _add_recursive(self, node, key, value):
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value)
            else:
                self._add_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, value)
            else:
                self._add_recursive(node.right, key, value)
        else:
            node.value = value  # 如果键已存在，更新值
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

    def map(self, func):
        """对所有值应用函数"""
        self._map_recursive(self.root, func)

    def _map_recursive(self, node, func):
        if node is not None:
            node.value = func(node.value)
            self._map_recursive(node.left, func)
            self._map_recursive(node.right, func)

    def reduce(self, func, initial_state):
        """对所有 (key, value) 进行 reduce 计算"""
        state = initial_state
        return self._reduce_recursive(self.root, func, state)

    def _reduce_recursive(self, node, func, state):
        if node is not None:
            state = self._reduce_recursive(node.left, func, state)
            state = func(state, (node.key, node.value))
            state = self._reduce_recursive(node.right, func, state)
        return state

    def search(self, key):
        """查找 key，返回对应的 value"""
        node = self._search_recursive(self.root, key)
        return node.value if node else None

    def _search_recursive(self, node, key):
        if node is None or node.key == key:
            return node
        if key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def delete(self, key):
        """删除 key 并维护 BST 结构"""
        self.root = self._delete_recursive(self.root, key)

    def _delete_recursive(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # 节点有两个子节点
            if node.left and node.right:
                successor = self._find_min(node.right)  # 找右子树最小值
                node.key, node.value = successor.key, successor.value
                node.right = self._delete_recursive(node.right, successor.key)
            else:  # 只有一个子节点或者无子节点
                node = node.left if node.left else node.right
        return node

    def _find_min(self, node):
        """找到 BST 最小值（最左侧节点）"""
        while node.left:
            node = node.left
        return node

    def update(self, key, new_value):
        """更新 key 的 value"""
        node = self._search_recursive(self.root, key)
        if node:
            node.value = new_value

    def inorder_traversal(self):
        """中序遍历（升序输出所有键值对）"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append((node.key, node.value))
            self._inorder_recursive(node.right, result)

# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    d = BSTDictionary()
    d.add(5, "apple")
    d.add(3, "banana")
    d.add(7, "cherry")
    d.add(4, "date")

    print(d.to_list())  # [(3, 'banana'), (4, 'date'), (5, 'apple'), (7, 'cherry')]
    print(d.search(4))  # 'date'
    print(d.search(10))  # None

    d.add(8, "A")
    d.add(2, "B")
    d.add(5, "C")
    d.add(9, "D")
    d.add(1, "E")

    print(d.search(5))  # 输出: C
    print(d.search(1))  # 输出: E

    d.update(5, "Z")
    print(d.search(5))  # 输出: Z

    d.delete(7)
    print(d.inorder_traversal())  # 输出: [(3, 'B'), (5, 'Z'), (6, 'D'), (8, 'E')]

    d.map(lambda v: v.upper())
    print(d.to_list())  # [(3, 'BANANA'), (4, 'DATE'), (5, 'APPLE'), (7, 'CHERRY')]

    total_length = d.reduce(lambda acc, pair: acc + len(pair[1]), 0)
    print(total_length)  # 22
