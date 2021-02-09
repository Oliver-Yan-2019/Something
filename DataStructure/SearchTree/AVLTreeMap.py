from DataStructure.SearchTree.BinarySearchTree import TreeMap


class AVLTreeMap(TreeMap):
    class Node(TreeMap.Node):
        __slots__ = 'height'

        def __init__(self, element, parent=None, left=None, right=None):
            super(AVLTreeMap.Node, self).__init__(element, parent, left, right)
            self.height = 0

        def left_height(self):
            return self.left.height if self.left is not None else 0

        def right_height(self):
            return self.right.height if self.right is not None else 0

    @staticmethod
    def _recompute_height(position):
        position.node.height = 1 + max(position.node.left_height(), position.node.right_height())

    @staticmethod
    def _is_balanced(position):
        return abs(position.node.left_height() - position.node.right_height()) <= 1

    def _tall_child(self, position, favor_left=False):
        if position.node.left_height() + (1 if favor_left else 0) > position.node.right_height():
            return self.left(position)
        else:
            return self.right(position)
        
    def _tall_grandchild(self, position):
        _child = self._tall_child(position)
        _alignment = (_child == self.left(position))
        return self._tall_child(_child, _alignment)

    def _re_balance(self, position):
        while position is not None:
            _old_height = position.node.height
            if not self._is_balanced(position):
                position = self._restructure(self._tall_grandchild(position))
                self._recompute_height(self.left(position))
                self._recompute_height(self.right(position))

            self._recompute_height(position)
            if position.node.height == _old_height:
                position = None
            else:
                position = self.parent(position)

    def re_balance_insert(self, position):
        self._re_balance(position)

    def re_balance_delete(self, position):
        self._re_balance(position)
