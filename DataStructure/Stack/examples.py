from DataStructure.Stack import ArrayStack
from typing import Text


def reverse_file(filename: Text):
    """文件内容按行逆置

    :param filename: 文件名
    :return:

    Example:
    >>> _file = '/Users/oliver/test.txt'
    >>> reverse_file(_file)
    """

    _stack = ArrayStack()

    original = open(filename)
    for line in original:
        _stack.push(line)

    original.close()

    output = open(filename, 'w')
    while not _stack.is_empty():
        output.write(_stack.pop())

    output.close()


def is_matched(expr: Text) -> bool:
    """算术表达式的分隔符匹配算法

    :param expr: 表达式字符串
    :return: bool

    Example:
    >>> _not_match = '(a + b)]'
    >>> _match = '(a + b) * (c + d)'
    >>> is_matched(_not_match)
    False
    >>> is_matched(_match)
    True
    """

    stack = ArrayStack()
    bracket_pairs = {"(": ")", "[": "]", "{": "}"}
    for bracket in expr:
        if bracket in bracket_pairs:
            stack.push(bracket)
        elif bracket in (")", "]", "}"):
            if stack.is_empty() or bracket_pairs[stack.pop()] != bracket:
                return False

    return stack.is_empty()


def is_matched_html(raw: Text) -> bool:
    """测试一个HTML文本的标签是否正确匹配

    :param raw: HTML 字符串
    :return: bool

    Example:
    >>> _not_match_html = '<a></b>'
    >>> _match_html = '<a></a>'
    >>> is_matched_html(_not_match_html)
    False
    >>> is_matched_html(_match_html)
    True
    """

    _stack = ArrayStack()
    j = raw.find('<')
    while j != -1:
        k = raw.find('>', j + 1)  # 从 j + 1 开始找
        if k == -1:
            return False

        tag = raw[j + 1:k]  # 提取标签
        if not tag.startswith('/'):
            _stack.push(tag)
        else:
            if _stack.is_empty():
                return False

            if tag[1:] != _stack.pop():  # 标签匹配不上
                return False

        j = raw.find('<', k + 1)  # 从 k + 1 开始找

    return _stack.is_empty()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
