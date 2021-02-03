"""
队列

插入和删除遵循"先进先出"原则(FIFO), 队头的元素才能访问和删除, 队尾才允许插入元素
"""

from abc import ABCMeta, abstractmethod
from DataStructure.Link import PositionalList


class QueueEmpty(Exception):
    """
    空队列异常
    """

    pass


class ArrayQueue(object):
    """
    普通队列 - 使用循环列表实现
    """

    CAPACITY = 10  # 容量

    def __init__(self):
        self.__data = [None] * ArrayQueue.CAPACITY  # 初始化容器, 采用循环列表作为容器
        self.__size = 0  # 队列的大小
        self.__front = 0  # 队头在列表中的索引

    def __len__(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def first(self):
        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        return self.__data[self.__front]

    def dequeue(self):
        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        element = self.__data[self.__front]

        self.__data[self.__front] = None
        self.__front = (self.__front + 1) % len(self.__data)  # 循环使用列表, 队头推出一个元素, 新的索引需要取模
        self.__size -= 1

        if 0 < self.__size < len(self.__data) // 4:  # 当队列的大小小于列表长度的四分之一时, 缩小容器
            self._resize(len(self.__data) // 2)

        return element

    def enqueue(self, element):
        if self.__size == len(self.__data):
            self._resize(2 * len(self.__data))

        _end = (self.__front + self.__size) % len(self.__data)  # 获取插入位置在容器中的索引
        self.__data[_end] = element
        self.__size += 1

    def _resize(self, capacity):
        _data = self.__data
        _walk_index = self.__front
        self.__data = [None] * capacity

        for i in range(self.__size):
            self.__data[i] = _data[_walk_index]
            _walk_index = (1 + _walk_index) % len(_data)  # 下一个元素索引, 需要取模

        self.__front = 0


class ArrayDeque(object):
    """
    双端队列
    """

    CAPACITY = 10  # 容量

    def __init__(self):
        self.__data = [None] * ArrayQueue.CAPACITY  # 初始化列表
        self.__size = 0  # 队列的大小
        self.__front = 0  # 队头在列表中的索引

    def __len__(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def first(self):
        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        return self.__data[self.__front]

    def last(self):
        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        _back = (self.__front + self.__size - 1) % len(self.__data)
        return self.__data

    def add_first(self, element):
        if self.__size == len(self.__data):
            self._resize(2 * len(self.__data))

        _front = (self.__front - 1) % len(self.__data)
        self.__data[_front] = element
        self.__front = _front
        self.__size += 1

    def delete_first(self):
        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        element = self.__data[self.__front]

        self.__data[self.__front] = None
        self.__front = (self.__front + 1) % len(self.__data)  # 循环使用列表, 队头推出一个元素, 新的索引需要取模
        self.__size -= 1

        if 0 < self.__size < len(self.__data) // 4:  # 当队列的大小小于列表长度的四分之一时
            self._resize(len(self.__data) // 2)

        return element

    def add_last(self, element):
        if self.__size == len(self.__data):
            self._resize(2 * len(self.__data))

        _end = (self.__front + self.__size) % len(self.__data)
        self.__data[_end] = element
        self.__size += 1

    def delete_last(self):
        if self.is_empty():
            raise QueueEmpty('queue is empty!')

        _end = (self.__front + self.__size - 1) % len(self.__data)
        element = self.__data[_end]

        self.__data[_end] = None
        self.__size -= 1

        if 0 < self.__size < len(self.__data) // 4:
            self._resize(len(self.__data) // 2)

        return element

    def _resize(self, capacity):
        _data = self.__data
        _walk_index = self.__front
        self.__data = [None] * capacity

        for i in range(self.__size):
            self.__data[i] = _data[_walk_index]
            _walk_index = (1 + _walk_index) % len(_data)

        self.__front = 0


class PriorityQueueBase(object, metaclass=ABCMeta):
    class Item(object):
        __slots__ = 'key', 'value'

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __lt__(self, other):
            return self.key < other.key

    @abstractmethod
    def __len__(self):
        pass

    def is_empty(self):
        return len(self) == 0


class UnsortedPriorityQueue(PriorityQueueBase):
    def __init__(self):
        self.__data = PositionalList()

    def __len__(self):
        return len(self.__data)

    def __find_min(self):
        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        _small = self.__data.first()
        _walk = self.__data.after(_small)
        while _walk is not None:
            if _walk.element() < _small.element():
                _small = _walk

            _walk = self.__data.after(_walk)

        return _small

    def add(self, key, value):
        self.__data.add_last(self.Item(key, value))

    def min(self):
        _position = self.__find_min()
        _item = _position.element()
        return _item.key, _item.value

    def remove_min(self):
        _position = self.__find_min()
        _item = self.__data.delete(_position)
        return _item.key, _item.value


class SortedPriorityQueue(PriorityQueueBase):
    def __init__(self):
        self.__data = PositionalList()

    def __len__(self):
        return len(self.__data)

    def add(self, key, value):
        _item = self.Item(key, value)
        _walk = self.__data.first()
        while _walk is not None and _walk.element() < _item:
            _walk = self.__data.after(_walk)

        if _walk is None:
            self.__data.add_first(_item)
        else:
            self.__data.add_after(_walk, _item)

    def min(self):
        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        _position = self.__data.first()
        _item = _position.element()
        return _item.key, _item.value

    def remove_min(self):
        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        _position = self.__data.delete(self.__data.first())
        _item = _position.element()
        return _item.key, _item.value
