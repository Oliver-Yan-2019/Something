class SequenceIterator(object):
    def __init__(self, sequence):
        """
        构造函数，初始化序列迭代器实例
        :param sequence: 序列，支持任何序列类型
        """

        self.__seq = sequence
        self.__k = -1

    def __next__(self):
        self.__k += 1
        if self.__k < len(self.__seq):
            return self.__seq[self.__k]
        else:
            raise StopIteration('index out of range!')

    def __iter__(self):
        return self

    def __str__(self):
        return f'<{str(self.__seq)}>'


if __name__ == '__main__':
    iter1 = SequenceIterator('abc')
    print(iter1)
    print(next(iter1))
    print(next(iter1))
    print(next(iter1))
    print(next(iter1))
