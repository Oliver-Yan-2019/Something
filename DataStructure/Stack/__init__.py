"""
栈

插入和删除遵循"后进先出"原则(LIFO), 即栈顶

可以用于实现数据的逆置
"""


class StackEmpty(Exception):
    """
    空栈异常
    """

    pass


class ArrayStack(object):
    """
    采用适配器模式, 基于python的list类型实现的栈
    """

    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def is_empty(self):
        return len(self.__data) == 0

    def push(self, element):
        self.__data.append(element)

    def top(self):
        if self.is_empty():
            raise StackEmpty('stack is empty!')

        return self.__data[-1]

    def pop(self):
        if self.is_empty():
            raise StackEmpty('stack is empty!')

        return self.__data.pop()


if __name__ == '__main__':
    # 实现一个文件中各行的逆置
    def reverse_file(filename):
        _stack = ArrayStack()

        original = open(filename)
        for line in original:
            _stack.push(line)

        original.close()

        output = open(filename, 'w')
        while not _stack.is_empty():
            output.write(_stack.pop())

        output.close()


    _file = '/Users/oliver/test.txt'
    reverse_file(_file)

    # 算术表达式的分隔符匹配算法
    def is_matched(expr):
        left = '([{'
        right = ')]}'
        _stack = ArrayStack()
        for c in expr:
            if c in left:
                _stack.push(c)
            elif c in right:
                if _stack.is_empty():
                    return False

                if right.index(c) != left.index(_stack.pop()):
                    return False

        return _stack.is_empty()


    _not_match = '(a + b)]'
    _match = '(a + b) * (c + d)'
    print(is_matched(_not_match))
    print(is_matched(_match))

    # 测试一个HTML文本的标签是否正确匹配
    def is_matched_html(raw):
        _stack = ArrayStack()
        j = raw.find('<')
        while j != -1:
            k = raw.find('>', j + 1)
            if k == -1:
                return False

            tag = raw[j + 1:k]
            if not tag.startswith('/'):
                _stack.push(tag)
            else:
                if _stack.is_empty():
                    return False

                if tag[1:] != _stack.pop():
                    return False

            j = raw.find('<', k + 1)

        return _stack.is_empty()

    _not_match_html = '<a></b>'
    _match_html = '<a></a>'
    print(is_matched_html(_not_match_html))
    print(is_matched_html(_match_html))
