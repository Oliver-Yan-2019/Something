from DataStructure.SearchTree.BinarySearchTree import TreeMap


class SplayTreeMap(TreeMap):
    def _splay(self, position):
        while position != self.root():
            _parent = self.parent(position)
            _grand = self.parent(_parent)
            if _grand is None:
                self._rotate(position)
            elif (_parent == self.left(_grand)) == (position == self.left(_parent)):
                self._rotate(_parent)
            else:
                self._rotate(position)
                self._rotate(position)

    def re_balance_insert(self, position):
        self._splay(position)

    def re_balance_update(self, position):
        self._splay(position)

    def re_balance_delete(self, position):
        if position is not None:
            self._splay(position)
