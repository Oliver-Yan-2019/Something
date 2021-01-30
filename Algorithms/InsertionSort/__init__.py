"""
参考: https://www.runoob.com/w3cnote/insertion-sort.html
"""


def insertion_sort(arr):
    """
    插入排序 O(n) - 双指针实现方式

    将元素从未排序序列挪至已排序序列
    :param arr:
    :return:
    """

    for i in range(1, len(arr)):
        cur = arr[i]  # 当前待排元素
        j = i
        while j > 0 and arr[j - 1] > cur:
            arr[j] = arr[j - 1]  # 将大于待排元素的元素往后挪(未排序序列)
            j -= 1

        arr[j] = cur  # 将待排元素放到已排序序列


if __name__ == '__main__':
    tmp = [1, 4, 2, 5, 7, 3, 9, 0, 5]
    insertion_sort(tmp)
    print(tmp)
