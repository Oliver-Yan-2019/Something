"""
队列

插入和删除遵循"先进先出"原则(FIFO), 队头的元素才能访问和删除, 队尾才允许插入元素
"""

from abc import ABCMeta, abstractmethod
from typing import *
from DataStructure.Link import Node, LinkEmpty, DLink


class QueueEmpty(Exception):
    """
    空队列异常
    """

    pass


class ArrayQueue(object):
    """
    队列 - 使用循环列表实现
    """

    CAPACITY = 10  # 容量

    def __init__(self):
        self.__data = [None] * ArrayQueue.CAPACITY  # 初始化容器, 采用循环列表作为容器
        self.__size = 0  # 队列的大小
        self.__front = 0  # 队头在列表中的索引

    def __len__(self) -> int:
        return self.__size

    def is_empty(self) -> bool:
        """
        判断是否为空队列
        :return:
        """

        return self.__size == 0

    def first(self):
        """
        获取队头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        return self.__data[self.__front]

    def dequeue(self):
        """
        队头元素出队 - O(1)*
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        element = self.__data[self.__front]

        self.__data[self.__front] = None
        self.__front = (self.__front + 1) % len(self.__data)  # 循环使用列表, 队头推出一个元素, 新的索引需要取模
        self.__size -= 1

        if 0 < self.__size < len(self.__data) // 4:  # 当队列的大小小于列表长度的四分之一时, 缩小容器
            self._resize(len(self.__data) // 2)

        return element

    def enqueue(self, element: Any):
        """
        元素入队 - O(1)*
        :param element: 元素
        :return:
        """

        if self.__size == len(self.__data):
            self._resize(2 * len(self.__data))

        _end = (self.__front + self.__size) % len(self.__data)  # 获取插入位置在容器中的索引
        self.__data[_end] = element
        self.__size += 1

    def _resize(self, capacity: int):
        """
        循环数组动态调整大小 - O(n)
        :param capacity: 容量
        :return:
        """

        _data = self.__data
        _walk_index = self.__front
        self.__data = [None] * capacity

        for i in range(self.__size):
            self.__data[i] = _data[_walk_index]
            _walk_index = (1 + _walk_index) % len(_data)  # 下一个元素索引, 需要取模

        self.__front = 0


class LinkQueue(object):
    """
    链表实现的队列
    """

    def __init__(self):
        self.head = None  # 队头
        self.tail = None  # 队尾
        self.size = 0  # 队长

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        """
        是否为空队
        :return:
        """

        return self.size == 0

    def first(self):
        """
        获取队头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.head.element

    def dequeue(self):
        """
        弹出队头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        _element = self.head.element

        self.head = self.head.next
        self.size -= 1

        if self.is_empty():
            self.tail = None

        return _element

    def enqueue(self, element: Any):
        """
        元素入队 - O(1)
        :param element: 元素
        :return:
        """

        _node = Node(element, None)
        if self.is_empty():
            self.head = _node
        else:
            self.tail.next = _node

        self.tail = _node
        self.size += 1


class ArrayDeque(object):
    """
    双端队列
    """

    CAPACITY = 10  # 容量

    def __init__(self):
        self.__data = [None] * ArrayQueue.CAPACITY  # 初始化列表
        self.__size = 0  # 队列的大小
        self.__front = 0  # 队头在列表中的索引

    def __len__(self) -> int:
        return self.__size

    def is_empty(self) -> bool:
        """
        判断是否为空队列
        :return:
        """

        return self.__size == 0

    def first(self):
        """
        获取队头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        return self.__data[self.__front]

    def last(self):
        """
        获取队尾元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        _back = (self.__front + self.__size - 1) % len(self.__data)
        return self.__data[_back]

    def add_first(self, element: Any):
        """
        元素从队头入队 - O(1)*
        :param element: 元素
        :return:
        """

        if self.__size == len(self.__data):
            self._resize(2 * len(self.__data))

        _front = (self.__front - 1) % len(self.__data)
        self.__data[_front] = element
        self.__front = _front
        self.__size += 1

    def delete_first(self):
        """
        队头元素出队 - O(1)*
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        element = self.__data[self.__front]

        self.__data[self.__front] = None
        self.__front = (self.__front + 1) % len(self.__data)  # 循环使用列表, 队头推出一个元素, 新的索引需要取模
        self.__size -= 1

        if 0 < self.__size < len(self.__data) // 4:  # 当队列的大小小于列表长度的四分之一时
            self._resize(len(self.__data) // 2)

        return element

    def add_last(self, element: Any):
        """
        元素从队尾入队 - O(1)*
        :param element: 元素
        :return:
        """

        if self.__size == len(self.__data):
            self._resize(2 * len(self.__data))

        _end = (self.__front + self.__size) % len(self.__data)
        self.__data[_end] = element
        self.__size += 1

    def delete_last(self):
        """
        队尾元素出队 - O(1)*
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        _end = (self.__front + self.__size - 1) % len(self.__data)
        element = self.__data[_end]

        self.__data[_end] = None
        self.__size -= 1

        if 0 < self.__size < len(self.__data) // 4:
            self._resize(len(self.__data) // 2)

        return element

    def _resize(self, capacity: int):
        """
        循环数组动态调整大小 - O(n)
        :param capacity: 容量
        :return:
        """

        _data = self.__data
        _walk_index = self.__front
        self.__data = [None] * capacity

        for i in range(self.__size):
            self.__data[i] = _data[_walk_index]
            _walk_index = (1 + _walk_index) % len(_data)

        self.__front = 0


class LinkDeque(DLink):
    """
    采用双向链表实现的双端队列
    """

    def first(self):
        """
        获取第一个节点 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.header.next.element

    def last(self):
        """
        获取最后一个节点 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.trailer.prev.element

    def insert_first(self, element: Any):
        """
        从表头插入元素 - O(1)
        :param element: 元素
        :return:
        """

        return self.insert_between(element, self.header, self.header.next)

    def insert_last(self, element: Any):
        """
        从表尾插入元素 - O(1)
        :param element: 元素
        :return:
        """

        return self.insert_between(element, self.trailer.prev, self.trailer)

    def delete_first(self):
        """
        删除队(表)头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.delete_node(self.header.next)

    def delete_last(self):
        """
        删除队(表)尾元素 - O(1)
        :return:
        """
        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.delete_node(self.trailer.prev)


class CircularQueue(object):
    """
    使用循环链表实现的循环队列
    """

    def __init__(self):
        self.tail = None  # 队尾
        self.size = 0  # 队长

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        """
        判断是否为空队
        :return:
        """

        return self.size == 0

    def first(self):
        """
        获取队头元素
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.tail.next.element

    def dequeue(self):
        """
        弹出队头元素
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        head = self.tail.next
        if self.size == 1:
            self.tail = None
        else:
            self.tail.next = head.next

        self.size -= 1
        return head.element

    def enqueue(self, element: Any):
        """
        元素入队 - O(1)
        :param element: 元素
        :return:
        """

        _node = Node(element, None)
        if self.is_empty():
            _node.next = _node
        else:
            _node.next = self.tail.next
            self.tail.next = _node

        self.tail = _node
        self.size += 1

    def rotate(self):
        """
        元素位置轮换 - O(1)
        :return:
        """

        if self.size > 0:
            self.tail = self.tail.next


class PriorityQueueBase(object, metaclass=ABCMeta):
    """
    优先级队列抽象基类
    """

    class Item(object):
        __slots__ = 'key', 'value'

        def __init__(self, key: Any, value: Any):
            self.key = key  # 键
            self.value = value  # 值

        def __lt__(self, other) -> bool:
            return self.key < other.key

    @abstractmethod
    def __len__(self) -> int:
        pass

    def is_empty(self) -> bool:
        """
        判断是否为空队列
        :return:
        """

        return len(self) == 0


class UnsortedPriorityQueue(PriorityQueueBase):
    """
    未排序优先级队列
    """

    def __init__(self):
        from DataStructure.Link import PositionalList

        self.__data = PositionalList()  # 使用位置列表作为队列容器

    def __len__(self) -> int:
        return len(self.__data)

    def __find_min(self):
        """
        获取优先级最高(大小最小)的元素 - O(n)
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        _small = self.__data.first()
        _walk = self.__data.after(_small)
        while _walk is not None:
            if _walk.element() < _small.element():
                _small = _walk

            _walk = self.__data.after(_walk)

        return _small

    def add(self, key: Any, value: Any):
        """
        元素入队 - 不排序 - O(1)
        :param key: 键
        :param value: 值
        :return:
        """

        self.__data.add_last(self.Item(key, value))

    def min(self):
        """
        获取优先级最高(大小最小)的元素 - O(n)
        :return:
        """

        _position = self.__find_min()
        _item = _position.element()
        return _item.key, _item.value

    def remove_min(self):
        """
        优先级最高(大小最小)的元素出队 - O(n)
        :return:
        """

        _position = self.__find_min()
        _item = self.__data.delete(_position)
        return _item.key, _item.value


class SortedPriorityQueue(PriorityQueueBase):
    """
    已排序优先级队列
    """

    def __init__(self):
        from DataStructure.Link import PositionalList

        self.__data = PositionalList()  # 使用位置列表作为队列的容器

    def __len__(self) -> int:
        return len(self.__data)

    def add(self, key: Any, value: Any):
        """
        元素入队 - 插入排序 - O(n)
        :param key: 键
        :param value: 值
        :return:
        """

        _item = self.Item(key, value)
        _walk = self.__data.first()
        while _walk is not None and _walk.element() > _item:
            _walk = self.__data.after(_walk)

        if _walk is None:
            self.__data.add_first(_item)
        else:
            self.__data.add_after(_walk, _item)

    def min(self):
        """
        获取优先级最高(大小最小)的元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        _position = self.__data.first()
        _item = _position.element()
        return _item.key, _item.value

    def remove_min(self):
        """
        优先级最高(大小最小)的元素出队 - O(1)
        :return:
        """

        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        _item = self.__data.delete(self.__data.first())
        return _item.key, _item.value


if __name__ == '__main__':
    _array_queue = ArrayQueue()
    print(_array_queue.is_empty())
    _array_queue.enqueue(1)
    _array_queue.enqueue(2)
    print(_array_queue.first())
    print(_array_queue.is_empty())
    _array_queue.dequeue()
    _array_queue.dequeue()
    print(_array_queue.is_empty())

    _array_deque = ArrayDeque()
    print(_array_deque.is_empty())
    _array_deque.add_first(1)
    _array_deque.add_last(2)
    print(_array_deque.first())
    print(_array_deque.last())
    print(_array_deque.is_empty())
    _array_deque.delete_first()
    _array_deque.delete_last()
    print(_array_deque.is_empty())

    _unsorted_priority_queue = UnsortedPriorityQueue()
    print(_unsorted_priority_queue.is_empty())
    _unsorted_priority_queue.add(1, 1)
    _unsorted_priority_queue.add(2, 2)
    print(_unsorted_priority_queue.min())
    print(_unsorted_priority_queue.is_empty())
    _unsorted_priority_queue.remove_min()
    _unsorted_priority_queue.remove_min()
    print(_unsorted_priority_queue.is_empty())

    _sorted_priority_queue = SortedPriorityQueue()
    print(_sorted_priority_queue.is_empty())
    _sorted_priority_queue.add(1, 1)
    _sorted_priority_queue.add(2, 2)
    print(_sorted_priority_queue.min())
    print(_sorted_priority_queue.is_empty())
    _sorted_priority_queue.remove_min()
    _sorted_priority_queue.remove_min()
    print(_sorted_priority_queue.is_empty())
