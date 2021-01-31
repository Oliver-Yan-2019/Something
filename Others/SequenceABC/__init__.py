from abc import ABCMeta, abstractmethod


"""
所有的序列对象都继承自序列抽象基类, 这个例子用于学习抽象基类, 可以参考 collections.abc 的 Sequence 实现
"""


class Sequence(metaclass=ABCMeta):
    @abstractmethod
    def __len__(self):
        """返回序列长度"""

    @abstractmethod
    def __getitem__(self, item):
        """根据索引获取序列元素"""

    def __contains__(self, item):
        for i in range(len(self)):
            if self[i] == item:
                return True

        return False

    def index(self, item):
        for i in range(len(self)):
            if self[i] == item:
                return i

        raise ValueError('item is not in sequence!')

    def count(self, item):
        k = 0
        for i in range(len(self)):
            if self[i] == item:
                k += 1

        return k
