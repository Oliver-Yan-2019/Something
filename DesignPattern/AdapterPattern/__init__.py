"""
适配器模式
定义一个新的类, 包含一个现存类的实例作为隐藏域, 之后用这个隐藏的实例变量去实现新类的方法.

栈和队列的实现都可以采用适配器模式借鉴python的list实现, 但是对于队列来说, list.pop(0)的情况时间复杂度为O(n), 这种实现方式参考下文的ListQueue,
本项目的队列类实现没有采用适配器模式, 相关操作的时间复杂度皆为O(1).

缺点: 性能上受现有类的实现影响, 可以考虑部分方法采用此模式, 部分方法独立实现.
"""

from DataStructure.Stack import ArrayStack


class ListQueue(object):
    """
    采用适配器模式实现的队列, 更优的实现方式参考ArrayQueue
    """

    def __init__(self):
        self.__data = []

    def __len__(self):
        return len(self.__data)

    def is_empty(self):
        return len(self.__data) == 0

    def first(self):
        return self.__data[0]

    def dequeue(self):
        return self.__data.pop(0)

    def enqueue(self, element):
        self.__data.append(element)


if __name__ == '__main__':
    _stack = ArrayStack()

    _stack.push(1)
    _stack.push(2)
    _stack.push(3)

    print(_stack.top())
    print(_stack.top())

    print(_stack.pop())
    print(_stack.pop())
    print(_stack.pop())
