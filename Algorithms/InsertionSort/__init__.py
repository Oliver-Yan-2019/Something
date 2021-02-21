"""
参考: https://www.runoob.com/w3cnote/insertion-sort.html

插入排序
通过构建有序序列, 对于未排序数据, 在已排序序列中从后向前扫描, 找到相应位置并插入.

优化 - 拆半插入
"""


def insertion_sort(arr):
    """
    插入排序
    O(n^2) -> O(n + m)
    m是逆序元素的个数
    :param arr:
    :return:
    """

    for i in range(1, len(arr)):  # 从第二个开始, 第一个默认为已排序元素
        cur = arr[i]  # 当前待排元素
        j = i
        while j > 0 and arr[j - 1] > cur:
            arr[j] = arr[j - 1]  # 扫描已排序序列, 大于当前待排元素的元素往后挪
            j -= 1

        arr[j] = cur  # 将待排元素放到已排序序列相应位置


if __name__ == '__main__':
    tmp = [1, 4, 2, 5, 7, 3, 9, 0, 5]
    insertion_sort(tmp)
    print(tmp)
