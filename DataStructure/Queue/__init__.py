"""
队列

插入和删除遵循"先进先出"原则(FIFO), 队头的元素才能访问和删除, 队尾才允许插入元素
"""


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
