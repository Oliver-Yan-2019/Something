class HeapSortInPlace(object):
    """
    原地堆排序 O(n * log n)
    """

    @classmethod
    def sort(cls, l_):
        _len = len(l_)
        cls.__heapify(l_, _len)
        for i in range(_len - 1, 0, -1):  # O(n)
            cls.__swap(l_, 0, i)
            _len -= 1
            cls.__down_heap(0, l_, _len)

    @classmethod
    def __heapify(cls, l_, length):
        _position = length // 2 - 1
        for index in range(_position, -1, -1):  # O(n)
            cls.__down_heap(index, l_, length)

    @classmethod
    def __down_heap(cls, index, l_, length):
        while True:  # O(log n)
            _left = 2 * index + 1
            if _left < length:
                _large_child = _left

                _right = 2 * (index + 1)
                if _right < length and l_[_left] < l_[_right]:
                    _large_child = _right

                if l_[_large_child] > l_[index]:
                    cls.__swap(l_, _large_child, index)
                    index = _large_child
                else:
                    break
            else:
                break

    @staticmethod
    def __swap(l_, index1, index2):
        l_[index1], l_[index2] = l_[index2], l_[index1]


if __name__ == '__main__':
    _l = [1, 3, 5, 2, 4, 7, 6, 8]
    print(_l)
    HeapSortInPlace.sort(_l)
    print(_l)
