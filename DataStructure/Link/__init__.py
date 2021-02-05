"""
链表

list的一些明显的缺点:
1, 动态数组的长度可能超过是寄存处数组元素所需的长度
2, 在实时系统中对操作的摊销边界是不可接受的
3, 在一个数组内部做插入和删除的操作, 代价太高

数组集中表示, 链表分布表示

几个常见的操作:
1, 遍历链表
2, 指针跳跃
3, 在头部插入元素
4, 在尾部插入元素
5, 删除一个元素(头部)

单向链表
不对称性 - 很难从尾部删除一个节点, 因为很难定位删除节点的前驱节点

循环链表 - 循环队列
尾节点指向头节点

双向链表
头哨兵和尾哨兵
位置列表 -> 使用组合模式, 设计维护访问频率的新类
"""


from typing import *


class LinkEmpty(Exception):
    """
    空链表异常
    """

    pass


class Node(object):
    """
    单向节点
    """

    __slots__ = 'element', 'next'  # 提高内存利用率

    def __init__(self, element, next_):
        self.element = element
        self.next = next_


"""
单向链表
"""


class LinkStack(object):
    """
    使用链表实现的栈
    """

    def __init__(self):
        self.head = None
        self.size = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        """
        判断是否为空栈
        :return:
        """

        return self.size == 0

    def push(self, element: Any):
        """
        元素入栈 - O(1)
        :param element: 元素
        :return:
        """

        self.head = Node(element, self.head)
        self.size += 1

    def top(self):
        """
        获取栈顶元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        return self.head.element

    def pop(self):
        """
        弹出栈顶元素 - O(1) - 对比列表实现 O(1)*
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('stack is empty!')

        _element = self.head.element

        self.head = self.head.next
        self.size -= 1

        return _element


class LinkQueue(object):
    """
    链表实现的队列
    """

    def __init__(self):
        self.head = None  # 队头
        self.tail = None  # 队尾
        self.size = 0  # 队长

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        """
        是否为空队
        :return:
        """

        return self.size == 0

    def first(self):
        """
        获取队头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.head.element

    def dequeue(self):
        """
        弹出队头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        _element = self.head.element

        self.head = self.head.next
        self.size -= 1

        if self.is_empty():
            self.tail = None

        return _element

    def enqueue(self, element: Any):
        """
        元素入队 - O(1)
        :param element: 元素
        :return:
        """

        _node = Node(element, None)
        if self.is_empty():
            self.head = _node
        else:
            self.tail.next = _node

        self.tail = _node
        self.size += 1


"""
循环链表
"""


class CircularQueue(object):
    """
    使用循环链表实现的循环队列
    """

    def __init__(self):
        self.tail = None  # 队尾
        self.size = 0  # 队长

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        """
        判断是否为空队
        :return:
        """

        return self.size == 0

    def first(self):
        """
        获取队头元素
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.tail.next.element

    def dequeue(self):
        """
        弹出队头元素
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        head = self.tail.next
        if self.size == 1:
            self.tail = None
        else:
            self.tail.next = head.next

        self.size -= 1
        return head.element

    def enqueue(self, element: Any):
        """
        元素入队 - O(1)
        :param element: 元素
        :return:
        """

        _node = Node(element, None)
        if self.is_empty():
            _node.next = _node
        else:
            _node.next = self.tail.next
            self.tail.next = _node

        self.tail = _node
        self.size += 1

    def rotate(self):
        """
        元素位置轮换 - O(1)
        :return:
        """

        if self.size > 0:
            self.tail = self.tail.next


"""
双向链表
"""


class DNode(object):
    """双向节点"""

    __slots__ = 'element', 'prev', 'next'

    def __init__(self, element, prev, next_):
        self.element = element
        self.prev = prev
        self.next = next_


class DLink(object):
    """
    双向链表
    """

    def __init__(self):
        self.header = DNode(None, None, None)  # 头哨兵
        self.trailer = DNode(None, None, None)  # 尾哨兵

        self.header.next = self.trailer
        self.trailer.prev = self.header

        self.size = 0

    def __len__(self) -> int:
        return self.size

    def is_empty(self) -> bool:
        """
        是否为空链表
        :return:
        """

        return self.size == 0

    def insert_between(self, element, predecessor, successor):
        """
        在两个节点中间插入元素 - O(1)
        :param element: 元素
        :param predecessor: 前驱节点
        :param successor: 后继节点
        :return:
        """

        _node = DNode(element, predecessor, successor)

        predecessor.next = _node
        successor.prev = _node
        self.size += 1
        return _node

    def delete_node(self, node):
        """
        删除节点 - O(1)
        :param node: 节点
        :return:
        """
        predecessor = node.prev
        successor = node.next
        predecessor.next = successor
        successor.prev = predecessor
        self.size -= 1

        element = node.element
        node.next = node.prev = node.element = None  # 节点回收
        return element


class LinkDeque(DLink):
    """
    采用双向链表实现的双端队列
    """

    def first(self):
        """
        获取第一个节点 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.header.next.element

    def last(self):
        """
        获取最后一个节点 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.trailer.prev.element

    def insert_first(self, element: Any):
        """
        从表头插入元素 - O(1)
        :param element: 元素
        :return:
        """

        return self.insert_between(element, self.header, self.header.next)

    def insert_last(self, element: Any):
        """
        从表尾插入元素 - O(1)
        :param element: 元素
        :return:
        """

        return self.insert_between(element, self.trailer.prev, self.trailer)

    def delete_first(self):
        """
        删除队(表)头元素 - O(1)
        :return:
        """

        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.delete_node(self.header.next)

    def delete_last(self):
        """
        删除队(表)尾元素 - O(1)
        :return:
        """
        if self.is_empty():
            raise LinkEmpty('queue is empty!')

        return self.delete_node(self.trailer.prev)


class PositionalList(DLink):
    """
    使用双向链表实现的位置列表
    """

    class Position(object):
        """
        位置
        """

        def __init__(self, container, node):
            self.container = container  # 所属列表容器实例
            self.node = node  # 指向节点

        def element(self):
            return self.node.element

        def __eq__(self, other) -> bool:
            return type(other) is type(self) and other.node is self.node

        def __ne__(self, other) -> bool:
            return not self == other

    def validate(self, position):
        """
        校验位置有效性并返回指向节点 - O(1)
        :param position:
        :return:
        """

        if not isinstance(position, self.Position):
            raise TypeError('position must be proper Position type!')

        if position.container is not self:
            raise ValueError('position is not belong to this container!')

        if position.node.next is None:
            raise ValueError('position is no longer valid!')

        return position.node

    def make_position(self, node):
        """
        生成节点对应的位置实例 - O(1)
        :param node:
        :return:
        """

        if node is self.header or node is self.trailer:
            return None
        else:
            return self.Position(self, node)

    def first(self):
        """
        获取第一个位置的元素 - n(1)
        :return:
        """

        return self.make_position(self.header.next)

    def last(self):
        """
        获取最后一个位置的元素 - n(1)
        :return:
        """

        return self.make_position(self.trailer.prev)

    def before(self, position):
        """
        获取前一个元素 - n(1)
        :param position:
        :return:
        """

        _node = self.validate(position)
        return self.make_position(_node.prev)

    def after(self, position):
        """
        获取后一个元素 - n(1)
        :param position:
        :return:
        """

        _node = self.validate(position)
        return self.make_position(_node.next)

    def __iter__(self):
        cursor = self.first()
        while cursor is not None:
            yield cursor.element()
            cursor = self.after(cursor)

    def insert_between(self, element, predecessor, successor):
        _node = super(PositionalList, self).insert_between(element, predecessor, successor)
        return self.make_position(_node)

    def add_first(self, element):
        return self.insert_between(element, self.header, self.header.next)

    def add_last(self, element):
        return self.insert_between(element, self.trailer.prev, self.trailer)

    def add_before(self, position, element):
        _node = self.validate(position)
        return self.insert_between(element, _node.prev, _node)

    def add_after(self, position, element):
        _node = self.validate(position)
        return self.insert_between(element, _node, _node.next)

    def delete(self, position):
        _node = self.validate(position)
        return self.delete_node(_node)

    def replace(self, position, element):
        _node = self.validate(position)
        _old_element, _node.element = _node.element, element
        return _old_element


class FavoritesList(object):
    """
    访问频率队列
    两个操作:
        1, 访问某个节点: 访问数加一, 排序上移
        2, 获取访问频率最高的k个节点
    """

    class Item(object):
        __slots__ = 'value', 'count'

        def __init__(self, value):
            self.value = value
            self.count = 0

    def __init__(self):
        self.__data = PositionalList()

    def __len__(self):
        return len(self.__data)

    def is_empty(self):
        return len(self.__data) == 0

    def __find_position(self, value):
        walk = self.__data.first()
        while walk is not None and walk.element().value != value:
            walk = self.__data.after(walk)

        return walk

    def __move_up(self, position):
        if position != self.__data.first():
            _count = position.element().count
            walk = self.__data.before(position)
            if _count > walk.element().count:
                while walk != self.__data.first() and _count > self.__data.before(walk).element().count:
                    walk = self.__data.before(walk)

                self.__data.add_before(walk, self.__data.delete(position))

    def access(self, value):
        """
        访问某个节点
        :param value:
        :return:
        """

        _position = self.__find_position(value)
        if _position is None:
            _position = self.__data.add_last(self.Item(value))

        _position.element().count += 1
        self.__move_up(_position)

    def top(self, k):
        """
        获取访问频率最高的k个节点
        :param k:
        :return:
        """

        if not 1 <= k <= len(self):
            raise ValueError('illegal value for k!')

        walk = self.__data.first()
        for i in range(k):
            item = walk.element()
            yield item.value
            walk = self.__data.after(walk)


class FavoritesListMTF(FavoritesList):
    """
    访问频率列表的启发算法实现

    被访问的节点很可能在最近会被访问, 所以直接放到队头
    """

    def __move_up(self, position):
        if position != self.__data.first():
            self.__data.add_first(self.__data.delete(position))

    def top(self, k):
        if not 1 <= k <= len(self):
            raise ValueError('illegal value for k!')

        tmp = PositionalList()
        for item in self.__data:
            tmp.add_last(item)

        for i in range(k):
            high_position = tmp.first()
            walk = tmp.after(high_position)
            while walk is not None:
                if walk.element().count < high_position.element().count:
                    high_position = walk

                walk = tmp.after(walk)

            yield high_position.element().value
            tmp.delete(high_position)


if __name__ == '__main__':
    def insertion_sort(position_list: PositionalList):
        """
        基于位置列表实现的插入排序
        :param position_list:
        :return:
        """

        if len(position_list) > 1:
            maker = position_list.first()
            while maker != position_list.last():
                pivot = position_list.after(maker)  # 待排区第一个节点
                value = pivot.element()
                if value > maker.element():  # 待排区第一个节点比当前节点大, 直接放入已排区
                    maker = pivot
                else:
                    walk = maker
                    while walk != position_list.first() and position_list.before(walk).element() > value:
                        walk = position_list.before(walk)  # 遍历已排区, 给待排区第一个节点找到相应位置

                    # 从待排区挪到已排区
                    position_list.delete(pivot)
                    position_list.add_before(walk, value)


    _position_list = PositionalList()
    _position_list.add_first(3)
    _position_list.add_first(2)
    _position_list.add_first(0)
    _position_list.add_first(1)
    _position_list.add_first(5)
    _position_list.add_first(4)

    print(f'{[i for i in _position_list]}')
    insertion_sort(_position_list)
    print(f'{[i for i in _position_list]}')
