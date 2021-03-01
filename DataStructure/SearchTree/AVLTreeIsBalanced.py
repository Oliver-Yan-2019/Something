class AVLTreeIsBalanced:
    class TreeNode:
        def __init__(self, x):
            self.val = x
            self.left = None
            self.right = None

    @classmethod
    def is_balanced(cls, root: TreeNode):
        def depth(node):
            if not node:
                return 0

            l_dep = depth(node.left)
            if l_dep == -1:
                return -1

            r_dep = depth(node.right)
            if r_dep == -1:
                return -1

            div = abs(l_dep - r_dep)
            if div > 1:
                return -1

            return max(l_dep, r_dep) + 1

        return depth(root) != -1
