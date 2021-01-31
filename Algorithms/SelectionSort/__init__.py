"""
参考: https://www.runoob.com/w3cnote/selection-sort.html

选择排序

首先在未排序序列中找到最小(大)元素, 存放到排序序列的起始位置;
再从剩余未排序元素中继续寻找最小(大)元素, 然后放到已排序序列的末尾;
重复第二, 直到所有元素均排序完毕.
"""


def selection_sort(arr):
    """
    选择排序 O(n^2)
    :param arr:
    :return:
    """

    for i in range(len(arr) - 1):
        min_index = i  # 记录最小数的索引
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_index]:
                min_index = j

        if i != min_index:
            arr[i], arr[min_index] = arr[min_index], arr[i]  # i 不是最小数时, 将 i 和最小数进行交换

    return arr


if __name__ == '__main__':
    tmp = [1, 4, 2, 5, 7, 3, 9, 0, 5]
    selection_sort(tmp)
    print(tmp)

