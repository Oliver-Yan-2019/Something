from abc import ABCMeta, abstractmethod


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
