import ctypes


class DynamicArray(object):
    def __init__(self):
        self.__length = 0  # 数组当前存储的实际元素个数
        self.__capacity = 1  # 数组当前允许存储的最大元素个数, 容量
        self.__Arr = self.__make_array(self.__capacity)  # 当前所分配的数组的引用

    @staticmethod
    def __make_array(capacity):
        """
        创建容量为capacity的cpython对象数组
        :param capacity:
        :return:
        """

        return (capacity * ctypes.py_object)()

    def __len__(self):
        return self.__length

    def __getitem__(self, item):
        if not 0 <= item < self.__length:
            raise IndexError('invalid index')

        return self.__Arr[item]

    def append(self, item):
        if self.__length == self.__capacity:
            self.__resize(2 * self.__capacity)

        self.__Arr[self.__length] = item
        self.__length += 1

    def __resize(self, capacity):
        """
        重新分配数组
        :param capacity:
        :return:
        """

        __new_Arr = self.__make_array(capacity)
        for i in range(self.__length):  # 移动元素到新的数组空间
            __new_Arr[i] = self.__Arr[i]

        self.__Arr = __new_Arr  # 修改引用, 原数组内存释放
        self.__capacity = capacity

    def insert(self, index, item):
        if self.__length == self.__capacity:
            self.__resize(2 * self.__capacity)

        for i in range(self.__length, index, -1):
            self.__Arr[i] = self.__Arr[i - 1]

        self.__Arr[index] = item
        self.__length += 1

    def remove(self, item):
        for i in range(self.__length):
            if self.__Arr[i] == item:
                for j in range(i, self.__length - 1):
                    self.__Arr[j] = self.__Arr[j + 1]

                self.__Arr[self.__length - 1] = None
                self.__length -= 1

                if 0 < self.__length < self.__capacity // 4:  # 当数组的实际储存的元素个数小于列表长度的四分之一时
                    self.__resize(self.__capacity // 2)

                return

        raise ValueError('value not found!')


if __name__ == '__main__':
    _array = DynamicArray()
    _array.append(1)
    _array.append(1)
    _array.append(1)
    _array.append(1)
    _array.append(1)

    print(len(_array))
    print(_array[3])
    _array.insert(3, 2)
    print(_array[3])
    _array.remove(2)
    print(_array[3])
