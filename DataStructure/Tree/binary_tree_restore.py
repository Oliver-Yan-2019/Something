from DataStructure.Tree import LinkBinaryTree
from DataStructure.Queue import LinkQueue
from typing import Any, Union


# 假设二叉树的节点没有重复元素
# 先序遍历结果: [根节点, 左子树, 右子树]
# 中序遍历结果: [左子树, 根节点, 右子树]
# 后序遍历结果: [左子树, 右子树, 根节点]
#
# 很容易从先序遍历和后序遍历结果中取到根节点
# 遍历中序遍历结果, 可以确定左右子树的分界线, 进而可以在先序遍历和后序遍历结果中找到左右子树根节点
# 所以从中序和先序或者中序和后序遍历结果还原整个二叉树(先序和后序不能还原)
#
# 以下采用链表队列实现左右子树的递归生成算法


class BinaryTreeRestore(object):
    @classmethod
    def restore_by_preorder_inorder(cls, preorder: [Any], inorder: [Any]) -> Union[LinkBinaryTree, None]:
        """从先序遍历和中序遍历还原链式二叉树

        :param preorder: [Any] 先序遍历列表
        :param inorder: [Any] 中序遍历列表
        :return: LinkBinaryTree

        Example:
        >>> a = list()
        >>> for node in BinaryTreeRestore.restore_by_preorder_inorder([1,2,3,4,5,6,7], [3,2,4,1,6,5,7]):
        ...     a.append(node)
        >>> a
        [1, 2, 5, 3, 4, 6, 7]
        """

        def create_binary_tree(t: LinkBinaryTree, n: LinkBinaryTree.Position, p: [Any], i: [Any], s: int):
            """生成二叉树

            :param t: LinkBinaryTree
            :param n: LinkBinaryTree.Position
            :param p: [Any]
            :param i: [Any]
            :param s: int
            :return:
            """

            queue = LinkQueue()  # 采用链表实现的队列顺序遍历左右子树, 不用list, 使用pop代价太高, 不使用pop则浪费空间

            while True:
                # 循环从先序遍历列表中确定子树的跟节点, 其中:
                # p[1]是左子树的根节点
                # p[k + 1]是右子树的根节点

                k = 0
                while p[0] != i[k]:
                    k += 1

                if k != 0:
                    t.add_left(n, p[1])
                    queue.enqueue((t.left(n), p[1:], i, k))  # k为左子树的长度

                if s - k - 1 != 0:
                    t.add_right(n, p[k + 1])
                    queue.enqueue((t.right(n), p[k + 1:], i[k + 1:], s - k - 1))  # s - k - 1为右子树的长度(去掉了根节点需要-1)

                if len(queue) == 0:
                    break

                n, p, i, s = queue.dequeue()

        if len(preorder) == 0:
            return None

        _tree = LinkBinaryTree()
        _tree.add_root(preorder[0])

        create_binary_tree(_tree, _tree.root(), preorder, inorder, len(preorder))
        return _tree

    @classmethod
    def restore_by_postorder_inorder(cls, postorder: [Any], inorder: [Any]) -> Union[LinkBinaryTree, None]:
        """从后序遍历和中序遍历还原链式二叉树

        :param postorder: [Any] 先序遍历列表
        :param inorder: [Any] 中序遍历列表
        :return: LinkBinaryTree

        Example:
        >>> a = list()
        >>> for node in BinaryTreeRestore.restore_by_postorder_inorder([3,4,2,6,7,5,1], [3,2,4,1,6,5,7]):
        ...     a.append(node)
        >>> a
        [1, 2, 5, 3, 4, 6, 7]
        """

        def create_binary_tree(t: LinkBinaryTree, n: LinkBinaryTree.Position, p: [Any], i: [Any], s: int):
            """生成二叉树

            :param t: LinkBinaryTree
            :param n: LinkBinaryTree.Position
            :param p: [Any]
            :param i: [Any]
            :param s: int
            :return:
            """

            queue = LinkQueue()  # 采用链表实现的队列顺序遍历左右子树, 不用list, 使用pop代价太高, 不使用pop则浪费空间

            while True:
                # 循环从后序遍历列表中确定子树的跟节点, 其中:
                # p[-1]是左子树的根节点
                # p[k - 1]是左子树的根节点

                k = 0
                while p[-1] != i[k]:
                    k += 1

                if k != 0:
                    t.add_left(n, p[k - 1])
                    queue.enqueue((t.left(n), p[:k], i[:k], k))  # k为左子树的长度

                if s - k - 1 != 0:
                    t.add_right(n, p[-2])
                    queue.enqueue((t.right(n), p[k:-1], i[k + 1:], s - k - 1))  # s - k - 1为右子树的长度(去掉了根节点需要-1)

                if len(queue) == 0:
                    break

                n, p, i, s = queue.dequeue()

        if len(postorder) == 0:
            return None
        import pdb; pdb.set_trace()  # breakpoint 876d40dd //

        _tree = LinkBinaryTree()
        _tree.add_root(postorder[-1])

        create_binary_tree(_tree, _tree.root(), postorder, inorder, len(postorder))
        return _tree


if __name__ == '__main__':
    import doctest

    doctest.testmod()
