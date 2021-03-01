from DataStructure.Tree import LinkBinaryTree
from DataStructure.Queue import LinkQueue


class IsSymmetric(object):
    @classmethod
    def check(cls, tree: LinkBinaryTree) -> bool:
        """检查二叉树是否对称

        :param tree: LinkBinaryTree
        :return: bool

        Example:
        >>> t = LinkBinaryTree()
        >>> r = t.add_root(1)
        >>> i = t.add_left(r, 2)
        >>> j = t.add_right(r, 2)
        >>> IsSymmetric.check(t)
        True
        >>> e = t.add_left(i, 3)
        >>> f = t.add_left(j, 3)
        >>> IsSymmetric.check(t)
        False
        """

        if len(tree) == 0:
            return True

        queue = LinkQueue()
        queue.enqueue(tree.left(tree.root()))
        queue.enqueue(tree.right(tree.root()))
        while not queue.is_empty():
            left, right = queue.dequeue(), queue.dequeue()
            if left is None and right is None:
                continue

            if left is None or right is None or left.element() != right.element():
                return False

            queue.enqueue(tree.left(left))
            queue.enqueue(tree.right(right))
            queue.enqueue(tree.right(left))
            queue.enqueue(tree.left(right))

        return True


if __name__ == '__main__':
    import doctest

    doctest.testmod()
