"""
参考: https://www.runoob.com/w3cnote/shell-sort.html

希尔排序 - 递减增量排序算法

非稳定排序算法

希尔排序是基于直接插入排序的以下两点性质而提出的改进方法:
1、插入排序在对几乎已经排好序的数据操作时, 效率高, 即可以达到线性排序的效率;
2、插入排序一般来说是低效的, 因为插入排序每次只能将数据移动一位.

先将整个待排序的记录序列分割成为若干子序列分别进行直接插入排序, 待整个序列中的记录"基本有序"时, 再对全体记录进行依次直接插入排序.

好的增量序列的共同特征:
1、最后一个增量必须为1;
2、应该尽量避免序列中的值(尤其是相邻的值)互为倍数的情况.

最好情况 O(n)
最坏情况 O(n * log n)
平均 O(n * log n)
"""


def shell_sort(arr):
    """
    希尔排序
    :param arr:
    :return:
    """

    increment = len(arr) // 2  # 起始增量
    while increment >= 1:
        for i in range(increment, len(arr)):  # 切分成 len(arr) // increment 组序列进行插入排序
            cur = arr[i]
            j = i
            while j > 0 and arr[j - increment] > cur:
                arr[j] = arr[j - increment]
                j -= increment

            arr[j] = cur
            
        increment = increment // 2  # 增量逐渐变小


if __name__ == '__main__':
    tmp = [1, 4, 2, 5, 7, 3, 9, 0, 5]
    shell_sort(tmp)
    print(tmp)
