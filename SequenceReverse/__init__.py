def reverse(s, start, stop):
    """
    序列倒置 递归方式实现
    :param s:
    :param start:
    :param stop:
    :return:
    """

    if start < stop:
        s[start], s[stop] = s[stop], s[start]
        reverse(s, start + 1, stop - 1)


def reverse_iterative(s):
    """
    序列倒置 迭代方式实现
    :param s:
    :return:
    """

    start, stop = 0, len(s) - 1
    while start < stop:
        s[start], s[stop] = s[stop], s[start]
        start, stop = start + 1, stop - 1


if __name__ == '__main__':
    a = [1, 2, 3]
    print(a)

    reverse(a, 0, 2)
    print(a)

    reverse_iterative(a)
    print(a)
