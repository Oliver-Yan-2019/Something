def insertion_sort(arr):
    """
    插入排序 O(n)
    :param arr:
    :return:
    """

    for i in range(1, len(arr)):
        cur = arr[i]
        j = i
        while j > 0 and arr[j - 1] > cur:
            arr[j] = arr[j - 1]
            j -= 1

        arr[j] = cur


if __name__ == '__main__':
    tmp = [1, 4, 2, 5, 7, 3, 9, 0, 5]
    insertion_sort(tmp)
    print(tmp)
