class Vector(object):
    def __init__(self, dimensions):
        """
        构造函数, 初始化n维向量
        :param dimensions: int 维度
        """

        self.__coords = [0] * dimensions

    def __len__(self):
        return len(self.__coords)

    def __getitem__(self, j):
        return self.__coords[j]

    def __setitem__(self, j, val):
        self.__coords[j] = val

    def __add__(self, other):
        if len(self) != len(other):
            raise ValueError('dimensions not match!')

        result = Vector(len(self))
        for j in range(len(self)):
            result[j] = self[j] + other[j]

        return result

    def __eq__(self, other):
        return self.__coords == other.value

    def __ne__(self, other):
        return not self.__coords == other.value

    def __str__(self):
        return f'<{str(self.__coords)[1:-1]}>'

    @property
    def value(self):
        """
        向量的坐标
        :return:
        """

        return self.__coords


if __name__ == '__main__':
    vector1 = Vector(3)
    vector1[0] = 0
    vector1[1] = 1
    vector1[2] = 2

    vector2 = Vector(3)
    vector2[0] = 0
    vector2[1] = 1
    vector2[2] = 2

    print(vector1 + vector2)
