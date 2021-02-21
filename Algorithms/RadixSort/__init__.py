

class RadixSort(object):
    @classmethod
    def sort(cls, arr):
        _max_digit = cls._get_max_digit(arr)
        return cls._sort(arr, _max_digit)
    
    @classmethod
    def _get_max_digit(cls, arr):
        max_element = cls._get_max_element(arr)
        return cls._get_element_length(max_element)

    @staticmethod
    def _get_max_element(arr):
        max_element = arr[0]
        for i in range(1, len(arr)):  # 找到最大最小值
            if arr[i] > max_element:
                max_element = arr[i]

        return max_element

    @staticmethod
    def _get_element_length(element):
        if element == 0:
            return 1

        length = 0
        while element != 0:
            length += 1
            element //= 10

        return length

    @classmethod
    def _sort(cls, arr, max_digit):
        _mod = 10
        _div = 1
        for _digit in range(max_digit):
            _bucket_list = [[] for _ in range(2 * _mod)]
            for _element in arr:
                _bucket_index = ((_element % _mod) // _div) + (_mod if _element > 0 else 0)
                _bucket_list[_bucket_index].append(_element)

            _pos = 0
            for _bucket in _bucket_list:
                for _element in _bucket:
                    arr[_pos] = _element
                    _pos += 1

            _mod *= 10
            _div *= 10

        return arr


if __name__ == '__main__':
    _l = [11, 53, 25, 32, 44, 87, 76, -11, -12, -23, 75, 98]
    print(_l)
    print(RadixSort.sort(_l))
