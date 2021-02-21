

class CountingSort(object):
    """
    计数排序 - 有确定范围的整数
    O(n + k)
    """

    @classmethod
    def sort(cls, arr, max_element):
        _bucket_len = max_element + 1
        _bucket_list = [0] * _bucket_len
        sorted_index = 0
        _arr_len = len(arr)
        for i in range(_arr_len):
            if not _bucket_list[arr[i]]:
                _bucket_list[arr[i]] = 0

            _bucket_list[arr[i]] += 1

        for j in range(_bucket_len):
            while _bucket_list[j] > 0:
                arr[sorted_index] = j
                sorted_index += 1
                _bucket_list[j] -= 1

        return arr


if __name__ == '__main__':
    _l = [1, 3, 5, 2, 4, 7, 6, 8]
    print(_l)
    print(CountingSort.sort(_l, 8))
