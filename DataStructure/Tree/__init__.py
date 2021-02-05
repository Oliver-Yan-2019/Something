"""
树
"""

from abc import ABCMeta, abstractmethod


class Tree(metaclass=ABCMeta):
    """
    所有树的抽象基类
    """

    class Position(metaclass=ABCMeta):
        @abstractmethod
        def element(self):
            pass

        @abstractmethod
        def __eq__(self, other):
            pass

        def __ne__(self, other):
            return not (self == other)

    @abstractmethod
    def root(self):
        pass

    @abstractmethod
    def parent(self, position):
        pass

    @abstractmethod
    def num_children(self, position):
        pass

    @abstractmethod
    def children(self, position):
        pass

    def positions(self):
        return self.preorder()  # 先序遍历
        # return self.postorder()  # 后序遍历
        # return self.breadth_first()  # 广度优先遍历

    def preorder(self):
        if not self.is_empty():
            for position in self.__subtree_preorder(self.root()):
                yield position

    def __subtree_preorder(self, position):
        """
        先序遍历 - 递归实现
        :param position:
        :return:
        """

        yield position
        for _child_position in self.children(position):
            for _c_p in self.__subtree_preorder(_child_position):
                yield _c_p

    def postorder(self):
        if not self.is_empty():
            for position in self.__subtree_postorder(self.root()):
                yield position

    def __subtree_postorder(self, position):
        """
        后序遍历 - 递归实现
        :param position:
        :return:
        """

        for _child_position in self.children(position):
            for _c_p in self.__subtree_postorder(_child_position):
                yield _c_p

        yield position

    def breadth_first(self):
        """
        广度优先遍历
        :return:
        """

        from DataStructure.Link import LinkQueue

        if not self.is_empty():
            _fringe = LinkQueue()
            _fringe.enqueue(self.root())
            while not _fringe.is_empty():
                _position = _fringe.dequeue()
                yield _position
                for _child_position in self.children(_position):
                    _fringe.enqueue(_child_position)

    @abstractmethod
    def __len__(self):
        pass

    def __iter__(self):
        for position in self.positions():
            yield position.element()

    def is_root(self, position):
        return self.root() == position

    def is_leaf(self, position):
        return self.num_children(position) == 0

    def is_empty(self):
        return len(self) == 0

    def depth(self, position):
        """
        计算当前位置的深度 O(dp) dp为深度
        :param position:
        :return:
        """

        if self.is_root(position):
            return 0
        else:
            return self.depth(self.parent(position)) + 1

    # def __height1(self):
    #     """
    #     计算树的高度 最坏情况O(n^2)
    #     :return:
    #     """
    #
    #     return max(self.depth(position) for position in self.positions() if self.is_leaf(position))
    #
    # def __height2(self, position):
    #     """
    #     计算树的高度 O(n)
    #     :param position:
    #     :return:
    #     """
    #
    #     if self.is_leaf(position):
    #         return 0
    #     else:
    #         return max(self.height(child) for child in self.children(position)) + 1
    #
    # def height(self, position = None):
    #     if position is None:
    #         position = self.root()
    #
    #     return self.__height2(position)


class BinaryTree(Tree, metaclass=ABCMeta):
    """
    二叉树的抽象基类
    """

    def positions(self):
        return self.inorder()  # 中序遍历
        # return self.preorder()  # 先序遍历
        # return self.postorder()  # 后序遍历
        # return self.breadth_first()  # 广度优先遍历

    def inorder(self):
        if not self.is_empty():
            for _position in self.__subtree_inorder(self.root()):
                yield _position

    def __subtree_inorder(self, position):
        _left = self.left(position)
        if _left is not None:
            for _p in self.__subtree_inorder(_left):
                yield _p

        yield position

        _right = self.right(position)
        if _right is not None:
            for _p in self.__subtree_inorder(_right):
                yield _p

    @abstractmethod
    def left(self, position):
        pass

    @abstractmethod
    def right(self, position):
        pass

    def sibling(self, position):
        """
        获取兄弟节点
        :param position:
        :return:
        """

        _parent = self.parent(position)
        if _parent is None:
            return None
        else:
            _left = self.left(position)
            if position == _left:
                return self.right(_parent)
            else:
                return _left

    def children(self, position):
        """
        遍历子节点
        :param position:
        :return:
        """

        _left = self.left(position)
        if _left is not None:
            yield _left

        _right = self.right(position)
        if _right is not None:
            yield _right


"""
链式二叉树
"""


class LinkBinaryTree(BinaryTree):
    class Node(object):
        __slots__ = 'element', 'parent', 'left', 'right'

        def __init__(self, element, parent=None, left=None, right=None):
            self.element = element

            self.parent = parent
            self.left = left
            self.right = right

    class Position(object):
        def __init__(self, container, node):
            self.container = container
            self.node = node

        def element(self):
            return self.node.element

        def __eq__(self, other):
            return type(other) is type(self) and other.node is self.node

    def __validate(self, position):
        if not isinstance(position, self.Position):
            raise TypeError('position must be proper Position type!')

        if position.container is not self:
            raise ValueError('position does not belong to this container!')

        if position.node.parent is position.node:  # ???
            raise ValueError('position is no longer valid!')

        return position.node

    def __make_position(self, node):
        return self.Position(self, node)

    def __init__(self):
        self.root_node = None
        self.size = 0

    def __len__(self):
        return self.size

    def root(self):
        return self.__make_position(self.root_node)

    def parent(self, position):
        _node = self.__validate(position)
        return self.__make_position(_node.parent)

    def left(self, position):
        _node = self.__validate(position)
        return self.__make_position(_node.left)

    def right(self, position):
        _node = self.__validate(position)
        return self.__make_position(_node.right)

    def num_children(self, position):
        _node = self.__validate(position)
        _count = 0
        if _node.left is not None:
            _count += 1

        if _node.right is not None:
            _count += 1

        return _count

    def add_root(self, element):
        if self.root_node is not None:
            raise ValueError('root exists!')

        self.size = 1
        self.root_node = self.Node(element)
        return self.__make_position(self.root_node)

    def add_left(self, position, element):
        _node = self.__validate(position)
        if _node.left is not None:
            raise ValueError('left child exists!')

        self.size += 1
        _node.left = self.Node(element, parent=_node)
        return self.__make_position(_node.left)

    def add_right(self, position, element):
        _node = self.__validate(position)
        if _node.right is not None:
            raise ValueError('right child exists!')

        self.size += 1
        _node.right = self.Node(element, parent=_node)
        return self.__make_position(_node.right)

    def replace(self, position, element):
        _node = self.__validate(position)
        _old_element, _node.element = _node.element, element
        return _old_element

    def delete(self, position):
        _node = self.__validate(position)
        if self.num_children(position) == 2:
            raise ValueError('position has two children!')

        _child = _node.left if _node.left else _node.right
        if _child is not None:
            _child.parent = _node.parent

            if _node is self.root_node:
                self.root_node = _child
            else:
                _parent = _node.parent
                if _node is _parent.left:
                    _parent.left = _child
                else:
                    _parent.right = _child

            self.size -= 1
            _node.parent = _node  # 提高内存回收效率
            return _node.element

    def attach(self, position, tree_1, tree_2):
        _node = self.__validate(position)
        if not self.is_leaf(position):
            raise ValueError('position must be leaf!')

        if not type(self) is type(tree_1) is type(tree_2):
            raise TypeError('tree types must match!')

        self.size += len(tree_1) + len(tree_2)
        if not tree_1.is_empty():
            _root_1 = tree_1.root_node
            _root_1.parent = _node
            _node.left = _root_1

            tree_1.root_node = None
            tree_1.size = 0

        if not tree_2.is_empty():
            _root_2 = tree_2.root_node
            _root_2.parent = _node
            _node.right = _root_2

            tree_2.root_node = None
            tree_2.size = 0


"""
封装欧拉遍历
"""


class EulerTour(object):
    def __init__(self, tree):
        self.__tree = tree

    def tree(self):
        return self.__tree

    def execute(self):
        pass

    def _tour(self, position, depth, path):
        self._hook_pre_visit(position, depth, path)

        results = []
        path.append(0)
        for _child in self.__tree.children(position):
            results.append(self._tour(_child, depth + 1, path))
            path[-1] += 1

        path.pop()

        return self._hook_post_visit(position, depth, path, results)

    """
    模版方法模式 - 开放以下钩子, 提供节点访问前后的辅助函数
    """
    def _hook_pre_visit(self, position, depth, path):
        pass

    def _hook_post_visit(self, position, depth, path, results):
        pass


class BinaryEulerTour(EulerTour):
    """
    二叉树欧拉遍历
    """

    def _tour(self, position, depth, path):
        self._hook_pre_visit(position, depth, path)

        results = []
        _left = self.tree().left(position)
        if _left is not None:
            path.append(0)
            results.extend([self._tour(_left, depth + 1, path)])
            path.pop(0)

        self._hook_in_visit(position, depth, path, results)

        _right = self.tree().right(position)
        if _right is not None:
            path.append(0)
            results.extend([self._tour(_right, depth + 1, path)])
            path.pop(0)

        return self._hook_post_visit(position, depth, path, results)

    def _hook_in_visit(self, position, depth, path, results):
        pass


class BinaryLayout(BinaryEulerTour):
    """
    二叉树在坐标系的描绘算法
    """

    def __init__(self, tree):
        super(BinaryLayout, self).__init__(tree)
        self.__count = 0

    def _hook_in_visit(self, position, depth, path, results):
        position.elemet().setX(self.__count)
        position.elemet().setY(depth)
        self.__count += 1


"""
算术表达式树
"""


class ExpressionTree(LinkBinaryTree):
    def __init__(self, token, left=None, right=None):
        super(ExpressionTree, self).__init__()
        if not isinstance(token, str):
            raise TypeError('token must be a string!')

        self.add_root(token)

        if left is not None:
            if token not in '+-*x/':
                raise ValueError('token must be valid operator!')

            self.attach(self.root(), left, right)

    def __str__(self):
        pieces = []
        self.__parenthesize_recur(self.root(), pieces)
        return ''.join(pieces)

    def __parenthesize_recur(self, position, result):
        if self.is_leaf(position):
            result.append(str(position.element()))
        else:
            result.append('(')
            self.__parenthesize_recur(self.left(position), result)
            result.append(position.element())
            self.__parenthesize_recur(self.right(position), result)
            result.append(')')

    def evaluate(self):
        return self.__evaluate_recur(self.root())

    def __evaluate_recur(self, position):
        if self.is_leaf(position):
            return float(position.element())
        else:
            op = position.element()
            left_val = self.__evaluate_recur(self.left(position))
            right_val = self.__evaluate_recur(self.right(position))
            if op == '+':
                return left_val + right_val
            elif op == '-':
                return left_val - right_val
            elif op == '/':
                return left_val / right_val
            else:
                return left_val * right_val


if __name__ == '__main__':
    # 打印目录缩进
    def preorder_indent(tree, position, depth):
        print(2 * depth * ' ' + str(position.element()))
        for _child in tree.children(position):
            preorder_indent(tree, _child, depth + 1)

    # 打印目录缩进 - 欧拉图实现
    class PreorderPrintIndentedTour(EulerTour):
        def _hook_pre_visit(self, position, depth, path):
            print(2 * depth * ' ' + str(position.element()))

    # 打印目录缩进, 包含索引
    def preorder_label(tree, position, depth, path):
        label = '.'.join(str(i + 1) for i in path)
        print(2 * depth * ' ' + label, position.element())
        path.append(0)
        for _child in tree.children(position):
            preorder_label(tree, _child, depth + 1, path)
            path[-1] += 1

        path.pop()

    # 打印目录缩进, 包含索引 - 欧拉图实现
    class PreorderPrintLabelTour(EulerTour):
        def _hook_pre_visit(self, position, depth, path):
            label = '.'.join(str(i + 1) for i in path)
            print(2 * depth * ' ' + label, position.element())

    # 一个虚拟公司的表示
    def parenthesize(tree, position):
        print(position.element(), end='')
        if not tree.is_leaf(position):
            first_time = True
            for _child in tree.children(position):
                sep = '(' if first_time else ','
                print(sep, end='')
                first_time = False
                parenthesize(tree, _child)

            print(')', end='')

    # 一个虚拟公司的表示 - 欧拉遍历实现
    class ParenthesizeTour(EulerTour):
        def _hook_pre_visit(self, position, depth, path):
            if path and path[-1] > 0:
                print(',', end='')

            print(position.element(), end='')
            if not self.tree().is_leaf(position):
                print('(', end='')

        def _hook_post_visit(self, position, depth, path, results):
            if not self.tree().is_leaf(position):
                print(')', end='')

    # 计算磁盘空间
    def disk_usage(tree, position):
        subtotal = position.element()
        for _child in tree.children(position):
            subtotal += disk_usage(tree, _child)

        return subtotal

    # 计算磁盘空间
    class DiskUsage(EulerTour):
        def _hook_post_visit(self, position, depth, path, results):
            return position.element().space() + sum(results)  # 位置实例需要添加space方法

    # 创建表达式树
    def build_expression_tree(tokens):
        _stack = []
        for t in tokens:
            if t in '+-x*/':
                _stack.append(t)
            elif t not in '()':
                _stack.append(ExpressionTree(t))
            elif t == ')':
                right = _stack.pop()
                op = _stack.pop()
                left = _stack.pop()
                _stack.append(ExpressionTree(op, left, right))

        return _stack.pop()


    _tokens = '(((3+1)x4)/((9-5)+2))'
    _tree = build_expression_tree(_tokens)
    print(_tree)
    print(_tree.evaluate())
