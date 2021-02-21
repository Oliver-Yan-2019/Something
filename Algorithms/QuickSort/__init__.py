from DataStructure.Link import LinkQueue


class QuickSort(object):
    """
    快速排序 O(n^2) -> O(n * log n)
    """

    @classmethod
    def sort(cls, l_: LinkQueue):
        _len = len(l_)
        if _len < 2:
            return

        _pivot = l_.first()
        _less = LinkQueue()
        _equal = LinkQueue()
        _greater = LinkQueue()
        while not l_.is_empty():
            if l_.first() < _pivot:
                _less.enqueue(l_.dequeue())
            elif _pivot < l_.first():
                _greater.enqueue(l_.dequeue())
            else:
                _equal.enqueue(l_.dequeue())

        cls.sort(_less)
        cls.sort(_greater)
        while not _less.is_empty():
            l_.enqueue(_less.dequeue())

        while not _equal.is_empty():
            l_.enqueue(_equal.dequeue())

        while not _greater.is_empty():
            l_.enqueue(_greater.dequeue())

    @classmethod
    def sort_inplace(cls, l_, a, b):
        """
        原地排序
        :param l_:
        :param a:
        :param b:
        :return:
        """

        if a > b:
            return

        _pivot = l_[b]
        _left = a
        _right = b - 1
        while _left <= _right:
            while _left <= _right and l_[_left] < _pivot:
                _left += 1

            while _left <= _right and _pivot < l_[_right]:
                _right -= 1

            if _left <= _right:
                l_[_left], l_[_right] = l_[_right], l_[_left]
                _left, _right = _left + 1, _right - 1

        l_[_left], l_[b] = l_[b], l_[_left]

        cls.sort_inplace(l_, a, _left - 1)
        cls.sort_inplace(l_, _left + 1, b)


if __name__ == '__main__':
    _l = LinkQueue()
    [_l.enqueue(i) for i in [1, 3, 5, 2, 4, 7, 6, 8]]
    QuickSort.sort(_l)
    print([_l.dequeue() for _ in range(len(_l))])

    _l = [1, 3, 5, 2, 4, 7, 6, 8]
    print(_l)
    QuickSort.sort_inplace(_l, 0, len(_l) - 1)
    print(_l)
