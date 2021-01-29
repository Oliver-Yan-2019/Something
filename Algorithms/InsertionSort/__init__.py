"""
参考: https://www.runoob.com/w3cnote/insertion-sort.html
"""


def insertion_sort(arr):
    """
    插入排序 O(n)

    将大于待排元素的往后挪
    :param arr:
    :return:
    """

    for i in range(1, len(arr)):
        cur = arr[i]  # 当前待排元素
        j = i
        while j > 0 and arr[j - 1] > cur:
            arr[j] = arr[j - 1]  # 将大于待排元素的元素往后挪
            j -= 1

        arr[j] = cur


if __name__ == '__main__':
    tmp = [1, 4, 2, 5, 7, 3, 9, 0, 5]
    insertion_sort(tmp)
    print(tmp)
