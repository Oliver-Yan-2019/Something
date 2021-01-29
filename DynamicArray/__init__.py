import ctypes


class DynamicArray(object):
    """动态数组"""
    def __init__(self):
        self.__length = 0
        self.__capacity = 1
        self.__Arr = self.__make_array(self.__capacity)

    @staticmethod
    def __make_array(capacity):
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
        __new_Arr = self.__make_array(capacity)
        for i in range(self.__length):
            __new_Arr[i] = self.__Arr[i]

        self.__Arr = __new_Arr
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
                return

        raise ValueError('value not found!')
