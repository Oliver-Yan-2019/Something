class Progression(object):
    def __init__(self, start=0):
        """
        构造函数，初始化通用数列实例
        :param start:
        """

        self._current = start

    def _progress(self):
        """
        更新当前值
        :return:
        """

        self._current += 1

    def __next__(self):
        if self._current is None:
            raise StopIteration
        else:
            this_element = self._current
            self._progress()
            return this_element

    def __iter__(self):
        return self


class ArithmeticProgression(Progression):
    def __init__(self, increment=1, start=0):
        """
        构造函数，初始化等差数列实例
        :param increment: 增量
        :param start: 初始值
        """

        super(ArithmeticProgression, self).__init__(start)
        self._increment = increment

    def _progress(self):
        self._current += self._increment


class GeometricProgression(Progression):
    def __init__(self, base=2, start=1):
        """
        构造函数，初始化等比数列实例
        :param base: 默认基数
        :param start: 初始值
        """

        super(GeometricProgression, self).__init__(start)
        self._base = base

    def _progress(self):
        self._current *= self._base


class FibonacciProgression(Progression):
    def __init__(self, first=0, second=1):
        """
        构造函数，初始化斐波那契数列实例
        :param first:
        :param second:
        """

        super(FibonacciProgression, self).__init__(first)
        self._prev = second - first

    def _progress(self):
        self._prev, self._current = self._current, self._current + self._prev


if __name__ == '__main__':
    arithmetic = ArithmeticProgression(5)
    print(next(arithmetic))
    print(next(arithmetic))
    print(next(arithmetic))

    print('\n')

    geometric = GeometricProgression()
    print(next(geometric))
    print(next(geometric))
    print(next(geometric))

    print('\n')

    fibonacci = FibonacciProgression()
    print(next(fibonacci))
    print(next(fibonacci))
    print(next(fibonacci))
    print(next(fibonacci))
    print(next(fibonacci))
    print(next(fibonacci))
    print(next(fibonacci))
    print(next(fibonacci))
    print(next(fibonacci))
