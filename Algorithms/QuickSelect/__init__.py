import random


class QuickSelect(object):
    """
    O(n)
    """

    @classmethod
    def select(cls, arr, k):
        while arr:
            if len(arr) == 1:
                return arr[0]

            _pivot = random.choice(arr)
            _less = [x for x in arr if x < _pivot]
            _equal = [x for x in arr if x == _pivot]
            _greater = [x for x in arr if x > _pivot]
            if k <= len(_less):
                arr = _less
            elif k <= len(_less) + len(_equal):
                return _pivot
            else:
                arr = _greater
                k -= (len(_less) + len(_equal))


if __name__ == '__main__':
    l_ = [1, 3, 4, 7, 5, 6, 9, 2, 11, 2, 34]
    print(QuickSelect.select(l_, 8))
