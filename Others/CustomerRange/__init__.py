from Others.SequenceABC import Sequence


class CustomerRange(Sequence):
    def __init__(self, start, stop=None, step=1):
        """
        构造函数，初始化自定义Range实例
        :param start: 起始索引
        :param stop: 结束索引
        :param step: 步长
        """

        if step == 0:
            raise ValueError('step can not be 0!')

        if stop is None:
            start, stop = 0, start

        self.__length = max(0, (stop - start + step - 1) // step)

        self.__start = start
        self.__step = step

    def __len__(self):
        return self.__length

    def __getitem__(self, item):
        if item < 0:
            item += len(self)

        if not 0 <= item < self.__length:
            raise IndexError('index out of range!') # for ... in ... 会捕获 IndexError 停止迭代

        return self.__start + item * self.__step


if __name__ == '__main__':
    for i in CustomerRange(100):
        print(i)

    _range = CustomerRange(10)
    print(_range.index(3))
    print(_range.count(3))
