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


def dijkstra_two_stack_algorithm(equation: str) -> int:
    """我们可以使用Dijkstra的两栈算法来求解如下方程: (5 + ((4 * 2)* (2 + 3)))

    >>> dijkstra_two_stack_algorithm("(5 + 3)")
    8
    >>> dijkstra_two_stack_algorithm("((9 - (2 + 9)) + (8 - 1))")
    5
    >>> dijkstra_two_stack_algorithm("((((3 - 2) - (2 + 3)) + (2 - 4)) + 3)")
    -3

    :param equation: str
    :return: result: int
    """

    import operator as op

    operators = {"*": op.mul, "/": op.truediv, "+": op.add, "-": op.sub}

    operand_stack = ArrayStack()
    operator_stack = ArrayStack()

    for i in equation:
        if i.isdigit():
            # 从左到右扫描表达式. 当遇到一个操作数时, 将其压入操作数堆栈.
            operand_stack.push(int(i))
        elif i in operators:
            # 当表达式中遇到运算符时, 将其压入运算符堆栈.
            operator_stack.push(i)
        elif i == ")":
            # 当表达式中遇到右括号时, 从操作符堆栈中弹出一个操作符.
            # 它必须操作的两个操作数必须是压入操作数堆栈的最后两个操作数.
            # 因此, 我们弹出操作数堆栈两次, 执行操作, 并将结果压回操作数堆栈,
            # 这样它就可以作为弹出操作数堆栈的下一个操作数的操作数.
            # 当表达式中遇到左括号时, 忽略它.
            opr = operator_stack.top()
            operator_stack.pop()
            num1 = operand_stack.top()
            operand_stack.pop()
            num2 = operand_stack.top()
            operand_stack.pop()

            total = operators[opr](num2, num1)
            operand_stack.push(total)

    # 当扫描完整个中缀表达式后, 留在操作数堆栈上的值表示该表达式的值.
    return operand_stack.top()


if __name__ == '__main__':
    import doctest

    doctest.testmod()
