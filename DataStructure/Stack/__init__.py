"""
栈

插入和删除遵循"后进先出"原则(LIFO), 即栈顶

可以用于实现数据的逆置
"""


from typing import *
from DataStructure.Link import Node, LinkEmpty


class StackEmpty(Exception):
    """
    空栈异常
    """

    pass


class ArrayStack(object):
    """
    采用适配器模式, 基于python的list类型实现的栈
    """

    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def is_empty(self) -> bool:
        """
        判断是否为空栈
        :return:
        """

        return len(self.__data) == 0

    def push(self, element: Any):
        """
        元素入栈 - O(1)*
        :param element:
        :return:
        """

        self.__data.append(element)

    def top(self):
        """
        获取栈顶元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise StackEmpty('stack is empty!')

        return self.__data[-1]

    def pop(self):
        """
        元素出栈 - O(1)*
        :return:
        """

        if self.is_empty():
            raise StackEmpty('stack is empty!')

        return self.__data.pop()


class LinkStack(object):
    """
    使用链表实现的栈
    """

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        """
        判断是否为空栈
        :return:
        """

        return self.size == 0

    def push(self, element: Any):
        """
        元素入栈 - O(1)
        :param element: 元素
        :return:
        """

        self.head = Node(element, self.head)
        self.size += 1

    def top(self):
        """
        获取栈顶元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        return self.head.element

    def pop(self):
        """
        弹出栈顶元素 - O(1) - 对比列表实现 O(1)*
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        _element = self.head.element

        self.head = self.head.next
        self.size -= 1

        return _element


def reverse_file(filename: Text):
    """
    文件内容按行逆置
    :param filename: 文件名
    :return:
    """

    _stack = ArrayStack()

    original = open(filename)
    for line in original:
        _stack.push(line)

    original.close()

    output = open(filename, 'w')
    while not _stack.is_empty():
        output.write(_stack.pop())

    output.close()


def is_matched(expr: Text):
    """
    算术表达式的分隔符匹配算法
    :param expr: 表达式字符串
    :return:
    """

    left = '([{'
    right = ')]}'
    _stack = ArrayStack()
    for c in expr:
        if c in left:
            _stack.push(c)
        elif c in right:
            if _stack.is_empty():
                return False

            if right.index(c) != left.index(_stack.pop()):  # 在分隔符字典中的索引对不上
                return False

    return _stack.is_empty()


def is_matched_html(raw: Text):
    """
    测试一个HTML文本的标签是否正确匹配
    :param raw: HTML 字符串
    :return:
    """

    _stack = ArrayStack()
    j = raw.find('<')
    while j != -1:
        k = raw.find('>', j + 1)
        if k == -1:
            return False

        tag = raw[j + 1:k]  # 提取标签
        if not tag.startswith('/'):
            _stack.push(tag)
        else:
            if _stack.is_empty():
                return False

            if tag[1:] != _stack.pop():  # 标签匹配不上
                return False

        j = raw.find('<', __start=k + 1)  # 从 k + 1 开始找

    return _stack.is_empty()


if __name__ == '__main__':
    _file = '/Users/oliver/test.txt'
    reverse_file(_file)

    _not_match = '(a + b)]'
    _match = '(a + b) * (c + d)'
    print(is_matched(_not_match))
    print(is_matched(_match))

    _not_match_html = '<a></b>'
    _match_html = '<a></a>'
    print(is_matched_html(_not_match_html))
    print(is_matched_html(_match_html))
