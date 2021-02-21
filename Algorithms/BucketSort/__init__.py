import math


class BucketSort(object):
    @classmethod
    def sort(cls, arr, bucket_num=5):
        """
        O(n + N)
        :param arr:
        :param bucket_num:
        :return:
        """

        if len(arr) < 2:
            return arr

        max_element = arr[0]
        min_element = arr[0]
        for i in range(1, len(arr)):  # 找到最大最小值
            if arr[i] < min_element:
                min_element = arr[i]
            elif arr[i] > max_element:
                max_element = arr[i]
            else:
                continue

        bucket_size = math.ceil((max_element - min_element + 1) / bucket_num)  # 根据桶的数量找到每个桶的范围
        buckets = [[] for _ in range(bucket_num)]
        for i in range(len(arr)):  # 将各个数分配到各个桶
            buckets[(arr[i] - min_element) // bucket_size].append(arr[i])

        for i in range(bucket_num):  # 桶内排序，可以使用各种排序方法
            buckets[i].sort()

        res = []
        for i in range(len(buckets)):  # 分别将各个桶内的数提出来，压入结果
            for j in range(len(buckets[i])):
                res.append(buckets[i][j])

        return res


if __name__ == '__main__':
    _l = [1, 3, 5, 2, 4, 7, 6, 8]
    print(_l)
    print(BucketSort.sort(_l))
