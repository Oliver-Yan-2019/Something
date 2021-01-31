"""
参考: https://www.runoob.com/w3cnote/bubble-sort.html

冒泡排序

比较相邻的元素, 如果第一个比第二个大, 就交换他们两个.
"""


def bubble_sort(arr):
    """
    冒泡排序 O(n^2)
    :param arr:
    :return:
    """

    for j in range(1, len(arr)):
        for i in range(0, len(arr) - j):  # 这里不是len(arr) - 1而是len(arr) - j, 因为每一轮遍历都会把每一轮最大元素挪到最后一位
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]


if __name__ == '__main__':
    tmp = [1, 4, 2, 5, 7, 3, 9, 0, 5]
    bubble_sort(tmp)
    print(tmp)
