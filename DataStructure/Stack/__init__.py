from typing import Any
from DataStructure.Link import Node, LinkEmpty


class StackEmpty(Exception):
    """
    栈为空
    Example:
        >>> raise StackEmpty('stack is empty!')
        Traceback (most recent call last):
        ...
        StackEmpty: stack is empty!
    """


class StackOverflow(Exception):
    """
    栈已满
    Example:
        >>> raise StackOverflow('stack is overflow!')
        Traceback (most recent call last):
        ...
        StackOverflow: stack is overflow!
    """


class ArrayStack(object):
    """采用适配器模式, 基于python的list类型实现的栈

        Example:
        >>> _stack = ArrayStack()
    """

    def __init__(self, limit: int = 10):
        """构造函数

        :param limit: int

        Example:
        >>> _stack = ArrayStack()
        """

        self.__data = []  # list 容器
        self.limit = limit  # 容量

    def __str__(self) -> str:
        """字符串

        :return: str

        Example:
        >>> _stack = ArrayStack()
        >>> _stack.push("c")
        >>> _stack.push("b")
        >>> _stack.push("a")
        >>> str(_stack)
        "['c', 'b', 'a']"
        """

        return str(self.__data)

    def __len__(self) -> int:
        """栈的长度

        :return: int

        Example:
        >>> _stack = ArrayStack()
        >>> _stack.push("c")
        >>> _stack.push("b")
        >>> _stack.push("a")
        >>> len(_stack)
        3
        """

        return len(self.__data)

    def is_empty(self) -> bool:
        """判断是否为空栈

        :return: bool

        Example:
        >>> _stack =  ArrayStack()
        >>> _stack.push(0)
        >>> _stack.is_empty()
        False
        >>> _stack.pop()
        0
        >>> _stack.is_empty()
        True
        """

        return len(self.__data) == 0

    def is_full(self) -> bool:
        """判断是否已满

        :return: bool

        Example:
        >>> _stack =  ArrayStack(1)
        >>> _stack.push(0)
        >>> _stack.is_full()
        True
        >>> _stack.pop()
        0
        >>> _stack.is_full()
        False
        """

        return len(self) == self.limit

    def push(self, element: Any):
        """元素入栈 - O(1)*

        :param element:
        :return:

        Example:
        >>> _stack =  ArrayStack(1)
        >>> _stack.push(1)
        >>> _stack.push(1)
        Traceback (most recent call last):
        ...
        StackOverflow: stack is overflow!
        """

        if len(self) >= self.limit:
            raise StackOverflow('stack is overflow!')

        self.__data.append(element)

    def top(self) -> Any:
        """获取栈顶元素 - O(1)

        :return: Any

        Example:
        >>> _stack =  ArrayStack()
        >>> _stack.push(1)
        >>> _stack.top()
        1
        >>> _stack.pop()
        1
        >>> _stack.top()
        Traceback (most recent call last):
        ...
        StackEmpty: stack is empty!
        """

        if self.is_empty():
            raise StackEmpty('stack is empty!')

        return self.__data[-1]

    def pop(self) -> Any:
        """元素出栈 - O(1)*

        :return: Any

        Example:
        >>> _stack =  ArrayStack()
        >>> _stack.push(1)
        >>> _stack.pop()
        1
        >>> _stack.pop()
        Traceback (most recent call last):
        ...
        StackEmpty: stack is empty!
        """

        if self.is_empty():
            raise StackEmpty('stack is empty!')

        return self.__data.pop()


class LinkStack(object):
    """使用链表实现的栈

        Example:
        >>> _stack = LinkStack()
    """

    def __init__(self, limit: int = 10):
        """构造函数

        :param limit: int

        Example:
        >>> _stack = LinkStack()
        """

        self.head = None  # 栈顶
        self.limit = limit  # 容量
        self.size = 0  # 大小

    def __iter__(self) -> [Any]:
        """遍历

        :return: [Any]

        Example:
        >>> _stack = LinkStack()
        >>> _stack.push("c")
        >>> _stack.push("b")
        >>> _stack.push("a")
        >>> for i in _stack:
        ...     print(i)
        a
        b
        c
        """

        node = self.head
        while node:
            yield node.element
            node = node.next

    def __str__(self) -> str:
        """打印字符串

        :return: str

        Example:
        >>> _stack = LinkStack()
        >>> _stack.push("c")
        >>> _stack.push("b")
        >>> _stack.push("a")
        >>> str(_stack)
        'a->b->c'
        """

        return "->".join([str(item) for item in self])

    def __len__(self) -> int:
        """栈的长度

        :return: int

        Example:
        >>> _stack = LinkStack()
        >>> _stack.push("c")
        >>> _stack.push("b")
        >>> _stack.push("a")
        >>> len(_stack)
        3
        """

        return self.size

    def is_empty(self) -> bool:
        """判断是否为空栈

        :return: bool

        Example:
        >>> _stack =  LinkStack()
        >>> _stack.push(0)
        >>> _stack.is_empty()
        False
        >>> _stack.pop()
        0
        >>> _stack.is_empty()
        True
        """

        return self.size == 0

    def is_full(self) -> bool:
        """判断是否已满

        :return: bool

        Example:
        >>> _stack =  LinkStack(1)
        >>> _stack.push(0)
        >>> _stack.is_full()
        True
        >>> _stack.pop()
        0
        >>> _stack.is_full()
        False
        """

        return len(self) == self.limit

    def push(self, element: Any) -> Any:
        """元素入栈 - O(1)

        :param element: 元素
        :return: Any

        Example:
        >>> _stack =  LinkStack()
        >>> _stack.push(0)
        >>> _stack.is_empty()
        False
        >>> _stack.pop()
        0
        >>> _stack.is_empty()
        True
        """

        if len(self) >= self.limit:
            raise StackOverflow('stack is overflow!')

        self.head = Node(element, self.head)
        self.size += 1

    def top(self) -> Any:
        """获取栈顶元素 - O(1)

        :return: Any

        Example:
        >>> _stack =  ArrayStack()
        >>> _stack.push(1)
        >>> _stack.top()
        1
        >>> _stack.pop()
        1
        >>> _stack.top()
        Traceback (most recent call last):
        ...
        StackEmpty: stack is empty!
        """

        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        return self.head.element

    def pop(self):
        """弹出栈顶元素 - O(1) - 对比列表实现 O(1)*

        :return: Any

        Example:
        >>> _stack =  ArrayStack()
        >>> _stack.push(1)
        >>> _stack.pop()
        1
        >>> _stack.pop()
        Traceback (most recent call last):
        ...
        StackEmpty: stack is empty!
        """

        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        _element = self.head.element

        self.head = self.head.next
        self.size -= 1

        return _element


if __name__ == '__main__':
    import doctest

    doctest.testmod()
