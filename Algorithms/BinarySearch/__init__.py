"""
参考: http://data.biancheng.net/view/122.html

二分查找
两个要求:
1, 数列有序
2, 数列使用顺序存储结构

优化: 插值查找(数列比较大并且比较均匀)
时间复杂度: O(log n)
"""


def binary_search(data, target, low, high):
    """
    二分查找 递归方式实现
    :param data:
    :param target:
    :param low:
    :param high:
    :return:
    """

    if low > high:
        return False
    else:
        mid = (low + high) // 2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            return binary_search(data, target, low, mid - 1)
        else:
            return binary_search(data, target, mid + 1, high)


def binary_search_iterative(data, target):
    """
    二分查找 迭代方式实现
    :param data:
    :param target:
    :return:
    """

    low = 0
    high = len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if target == data[mid]:
            return True
        elif target < data[mid]:
            high = mid - 1
        else:
            low = mid + 1

    return False


if __name__ == '__main__':
    print(binary_search(list(range(100)), 50, 0, 99))
    print(binary_search_iterative(list(range(100)), 50))
