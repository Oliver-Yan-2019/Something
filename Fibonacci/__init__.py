def bad_fibonacci(n):
    """
    效率比较低的斐波那契数列 O(2^n)
    :param n:
    :return:
    """

    if n <= 1:
        return n
    else:
        return bad_fibonacci(n-2) + bad_fibonacci(n - 1)


def good_fibonacci(n):
    """
    效率比较高的斐波那契数列 O(n)
    :param n:
    :return:
    """

    if n <= 1:
        return n, 0
    else:
        a, b = good_fibonacci(n - 1)
        return a + b, a
