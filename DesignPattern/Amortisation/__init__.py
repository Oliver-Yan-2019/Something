import sys
from time import time
from Others.DynamicArray import DynamicArray


"""
摊销分析可参考: https://www.cnblogs.com/SeekHit/p/4977678.html 或 http://codingdict.com/article/4859

这里采用摊销分析方法来分析动态数组相关操作的时间复杂度

本项目实现了动态数组 - DynamicArray(当数组已满, 将数组拓展为原来的2倍)
相关操作有:添加、删除、插入
有以下结论:
1、时间复杂度为O(n)
2、避免使用固定的增量, 时间复杂度为O(n^2)
"""


def array_amortise(n):
    """
    列表摊销分析
    :param n:
    :return:
    """

    data = []
    for i in range(n):
        a = len(data)
        b = sys.getsizeof(data)
        print('Length: {0:3d} Size in Bytes: {1:4d}'.format(a, b))
        data.append(0)


def compute_average(n):
    """
    添加的平均时长计算
    :param n:
    :return:
    """

    data = []
    start = time()
    for i in range(n):
        data.append(0)

    end = time()
    return (end - start) / n


if __name__ == '__main__':
    # 动态数组
    arr = DynamicArray()
    arr.append(1)
    arr.append(1)
    arr.append(1)
    arr.append(1)
    print(len(arr))

    # 摊销分析
    array_amortise(64)

    # 平均时长
    print(compute_average(100))
    print(compute_average(1000))
    print(compute_average(10000))
    print(compute_average(100000))
    print(compute_average(1000000))
    print(compute_average(10000000))
