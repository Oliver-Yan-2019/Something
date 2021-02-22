from typing import List
from DataStructure.Link import LinkQueue
import math


class ListMergeSort(object):
    """
    递归实现 O(n * log n)
    """

    @staticmethod
    def merge(l_1: List, l_2: List, l_: List):
        i = j = 0
        while i + j < len(l_):
            if j == len(l_2) or (i < len(l_1) and l_1[i] < l_2[j]):
                l_[i + j] = l_1[i]
                i += 1
            else:
                l_[i + j] = l_2[j]
                j += 1

    @classmethod
    def merge_sort(cls, l_: List):
        _len = len(l_)
        if _len < 2:
            return

        _mid = _len // 2
        l_1 = l_[0:_mid]
        l_2 = l_[_mid:_len]
        cls.merge_sort(l_1)
        cls.merge_sort(l_2)
        cls.merge(l_1, l_2, l_)


class LinkedQueueMergeSort(object):
    """
    递归实现 O(n * log n)
    """

    @staticmethod
    def merge(l_1: LinkQueue, l_2: LinkQueue, l_: LinkQueue):
        while not l_1.is_empty() and not l_2.is_empty():
            if l_1.first() > l_2.first():
                l_.enqueue(l_1.dequeue())
            else:
                l_.enqueue(l_2.dequeue())

        while not l_1.is_empty():
            l_.enqueue(l_1.dequeue())

        while not l_2.is_empty():
            l_.enqueue(l_2.dequeue())

    @classmethod
    def merge_sort(cls, l_: LinkQueue):
        _len = len(l_)
        if _len < 2:
            return

        l_1 = LinkQueue()
        l_2 = LinkQueue()
        while len(l_1) < _len // 2:
            l_1.enqueue(l_.dequeue())

        while not l_.is_empty():
            l_2.enqueue(l_.dequeue())

        cls.merge_sort(l_1)
        cls.merge_sort(l_2)
        cls.merge(l_1, l_2, l_)


class IterativeMergeSort(object):
    """
    自下而上 - 非递归实现 O(n * log n)
    """

    @staticmethod
    def merge(source, result, start, increment):
        end_1 = start + increment
        end_2 = min(start + 2 * increment, len(source))
        x, y, z = start, start + increment, start
        while x < end_1 and y < end_2:
            if source[x] < source[y]:
                result[z] = source[x]
                x += 1
            else:
                result[z] = source[y]
                y += 1

            z += 1

        if x < end_1:
            result[z:end_2] = source[x:end_1]
        elif y < end_2:
            result[z:end_2] = source[y:end_2]

    @classmethod
    def merge_sort(cls, l_):
        _len = len(l_)
        _log_n = math.ceil(math.log(_len, 2))
        _source, _dest = l_, [None] * _len
        for i in (2 ** k for k in range(_log_n)):
            for j in range(0, _len, 2 * i):
                cls.merge(_source, _dest, j, i)

            _source, _dest = _dest, _source

        if l_ is not _source:
            l_[0:_len] = _source[0:_len]


if __name__ == '__main__':
    _l = [85, 24, 63, 45, 17, 31, 96, 50]
    print(_l)
    ListMergeSort.merge_sort(_l)
    print(_l)

    _l = [85, 24, 63, 45, 17, 31, 96, 50]
    print(_l)
    IterativeMergeSort.merge_sort(_l)
    print(_l)

    _l = LinkQueue()
    [_l.enqueue(i) for i in [85, 24, 63, 45, 17, 31, 96, 50]]
    LinkedQueueMergeSort.merge_sort(_l)
    print([_l.dequeue() for _ in range(len(_l))])

    def decorated_merge_sort(data, key=None):
        """
        装饰 - 排序 - 取消 设计模式
        :param data:
        :param key:
        :return:
        """

        class Item(object):
            __slots__ = 'key', 'value'

            def __init__(self, k, v):
                self.key = k  # 键
                self.value = v  # 值

            def __lt__(self, other) -> bool:
                return self.key < other.key

        if key is not None:
            for i in range(len(data)):
                data[i] = Item(key(data[i]), data[i])

        IterativeMergeSort.merge_sort(data)
        if key is not None:
            for i in range(len(data)):
                data[i] = data[i].value

    _l = [85, 24, 63, 45, 17, 31, 96, 50]
    print(_l)
    decorated_merge_sort(_l, key=lambda x: x)
    print(_l)
