"""
堆
"""

from DataStructure.Queue import PriorityQueueBase, QueueEmpty


class HeapPriorityQueue(PriorityQueueBase):
    """
    小根堆实现的优先级队列
    """

    def __init__(self, contents=()):
        self.data = [self.Item(k, v) for k, v in contents]
        if len(contents) > 1:
            self.__heapify()

    def __heapify(self):
        """
        自底向上构建堆 O(n)
        :return:
        """

        _position = self.parent(len(self.data) - 1)
        for index in range(_position, -1, -1):
            self.down_heap(index)

    def __len__(self):
        return len(self.data)

    @staticmethod
    def parent(index):
        return (index - 1) // 2

    @staticmethod
    def left(index):
        return 2 * index + 1

    @staticmethod
    def right(index):
        return 2 * (index + 1)

    def has_left(self, index):
        return self.left(index) < len(self.data)

    def has_right(self, index):
        return self.right(index) < len(self.data)

    def swap(self, index1, index2):
        self.data[index1], self.data[index2] = self.data[index2], self.data[index1]

    def up_heap(self, index):
        _parent = self.parent(index)
        if index > 0 and self.data[index] < self.data[_parent]:
            self.swap(index, _parent)
            self.up_heap(_parent)

    def down_heap(self, index):
        if self.has_left(index):
            _left = self.left(index)
            _small_child = _left

            if self.has_right(index):
                _right = self.right(index)
                if self.data[_left] > self.data[_right]:
                    _small_child = _right

            if self.data[_small_child] < self.data[index]:
                self.swap(_small_child, index)
                self.down_heap(_small_child)

    def add(self, key, value):
        self.data.append(self.Item(key, value))
        self.up_heap(len(self.data) - 1)

    def min(self):
        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        _item = self.data[0]
        return _item.key, _item.value

    def remove_min(self):
        if self.is_empty():
            raise QueueEmpty('priority queue is empty!')

        self.swap(0, len(self.data) - 1)

        _item = self.data.pop()

        self.down_heap(0)

        return _item.key, _item.value


class AdaptableHeapPriorityQueue(HeapPriorityQueue):
    class Locator(HeapPriorityQueue.Item):
        __slots__ = 'index'

        def __init__(self, key, value, index):
            super(AdaptableHeapPriorityQueue.Locator, self).__init__(key, value)
            self.index = index

    def swap(self, index1, index2):
        super(AdaptableHeapPriorityQueue, self).swap(index1, index2)
        self.data[index1].index = index1
        self.data[index2].index = index2

    def bubble(self, index):
        if index > 0 and self.data[index] < self.data[self.parent(index)]:
            self.up_heap(index)
        else:
            self.down_heap(index)

    def add(self, key, value):
        _locator = self.Locator(key, value, len(self.data))
        self.data.append(_locator)
        self.up_heap(len(self.data) - 1)
        return _locator

    def update(self, locator, key, value):
        index = locator.index
        if not (0 <= index < len(self) and self.data[index] is locator):
            raise ValueError('invalid locator!')

        locator.key = key
        locator.value = value
        self.bubble(index)

    def remove(self, locator):
        index = locator.index
        if not (0 <= index < len(self) and self.data[index] is locator):
            raise ValueError('invalid locator!')

        if index == len(self) - 1:
            self.data.pop()
        else:
            self.swap(index, len(self) - 1)
            self.data.pop()
            self.bubble(index)

        return locator.key, locator.value


if __name__ == '__main__':
    _heap = HeapPriorityQueue(((2, 3), (1, 4), (5, 7), (3, 6)))
    print(_heap.remove_min())
    print(_heap.remove_min())
    print(_heap.remove_min())
    print(_heap.remove_min())

    from DataStructure.Link import PositionalList


    def positional_list_sort(positional_list: PositionalList):
        """
        采用堆对位置列表进行排序
        :param positional_list:
        :return:
        """

        _length = len(positional_list)
        _pq = HeapPriorityQueue()
        for index in range(_length):
            _element = positional_list.delete(positional_list.first())
            _pq.add(_element, _element)

        for index in range(_length):
            _, value = _pq.remove_min()
            positional_list.add_last(value)


    _position_list = PositionalList()
    _position_list.add_first(1)
    _position_list.add_first(5)
    _position_list.add_first(4)
    _position_list.add_first(3)
    positional_list_sort(_position_list)
    for i in _position_list:
        print(i)
