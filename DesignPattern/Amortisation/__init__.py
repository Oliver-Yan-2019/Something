import sys
from time import time
from Others.DynamicArray import DynamicArray


def array_amortise(n):
    data = []
    for i in range(n):
        a = len(data)
        b = sys.getsizeof(data)
        print('Length: {0:3d} Size in Bytes: {1:4d}'.format(a, b))
        data.append(0)


def compute_average(n):
    data = []
    start = time()
    for i in range(n):
        data.append(0)

    end = time()
    return (end - start) / n


if __name__ == '__main__':
    arr = DynamicArray()
    arr.append(1)
    arr.append(1)
    arr.append(1)
    arr.append(1)
    print(len(arr))

    array_amortise(64)

    print(compute_average(100))
    print(compute_average(1000))
    print(compute_average(10000))
    print(compute_average(100000))
    print(compute_average(1000000))
    print(compute_average(10000000))
