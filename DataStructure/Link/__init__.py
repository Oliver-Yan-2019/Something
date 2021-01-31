"""
链表

list的一些明显的缺点:
1、动态数组的长度可能超过是寄存处数组元素所需的长度
2、在实时系统中对操作的摊销边界是不可接受的
3、在一个数组内部做插入和删除的操作, 代价太高

数组集中表示, 链表分布表示

几个常见的操作:
1、遍历链表
2、指针跳跃
3、在头部插入元素
4、在尾部插入元素
5、删除一个元素(头部)

"""


class LinkEmpty(Exception):
    """
    空链表异常
    """

    pass


class Node(object):

    __slots__ = 'element', 'next'  # 提高内存利用率

    def __init__(self, element, next_):
        self.element = element
        self.next = next_


class LinkStack(object):
    """
    使用链表实现的栈
    """

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def push(self, element):
        self.head = Node(element, self.head)
        self.size += 1

    def top(self):
        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        return self.head.element

    def pop(self):
        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        _element = self.head.element

        self.head = self.head.next
        self.size -= 1

        return _element


class LinkQueue(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def first(self):
        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.head.element

    def dequeue(self):
        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        _element = self.head.element

        self.head = self.head.next
        self.size -= 1

        if self.is_empty():
            self.tail = None

        return _element

    def enqueue(self, element):
        _node = Node(element, None)
        if self.is_empty():
            self.head = _node
        else:
            self.tail.next = _node

        self.tail = _node
        self.size += 1
