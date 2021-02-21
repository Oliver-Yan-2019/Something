from DataStructure.SearchTree.BinarySearchTree import TreeMap


class RedBlackTreeMap(TreeMap):
    class Node(TreeMap.Node):
        __slots__ = 'red'

        def __init__(self, element, parent=None, left=None, right=None):
            super(RedBlackTreeMap.Node, self).__init__(element, parent, left, right)
            self.red = True

    @staticmethod
    def _set_red(position):
        position.node.red = True

    @staticmethod
    def _set_black(position):
        position.node.red = False

    @staticmethod
    def _set_color(position, make_red):
        position.node.red = make_red

    @staticmethod
    def _is_red(position):
        return position is not None and position.node.red

    def _is_red_leaf(self, position):
        return self._is_red(position) and self.is_leaf(position)

    def _get_red_child(self, position):
        for _child in (self.left(position), self.right(position)):
            if self._is_red(_child):
                return _child

        return None

    def _resolve_red(self, position):
        if self.is_root(position):
            self._set_black(position)
        else:
            _parent = self.parent(position)
            if self._is_red(_parent):
                _uncle = self.sibling(position)
                if not self._is_red(_uncle):
                    _middle = self._restructure(position)
                    self._set_black(_middle)
                    self._set_red(self.left(position))
                    self._set_red(self.right(position))
                else:
                    _grand = self.parent(_parent)
                    self._set_red(_grand)
                    self._set_black(self.left(_grand))
                    self._set_black(self.right(_grand))
                    self._resolve_red(_grand)  # 递归

    def re_balance_insert(self, position):
        self._resolve_red(position)

    def re_balance_delete(self, position):
        if len(self) == 1:
            self._set_black(self.root())
        elif position is not None:
            _number = self.num_children(position)
            if _number == 1:
                _child = next(self.children(position))
                if not self._is_red(_child):
                    self._fix_deficit(position, _child)
                elif _number == 2:
                    if self._is_red_leaf(self.left(position)):
                        self._set_black(self.left(position))
                    else:
                        self._set_black(self.right(position))

    def _fix_deficit(self, z, y):
        if not self._is_red(y):
            x = self._get_red_child(y)
            if x is not None:
                _old_color = self._is_red(z)
                _middle = self._restructure(x)
                self._set_color(_middle, _old_color)
                self._set_black(self.left(_middle))
                self._set_black(self.right(_middle))
            else:
                self._set_red(y)
                if self._is_red(z):
                    self._set_black(z)
                elif not self.is_root(z):
                    self._fix_deficit(self.parent(z), self.sibling(z))
                else:
                    self._rotate(y)
                    self._set_black(y)
                    self._set_red(z)
                    if z == self.right(y):
                        self._fix_deficit(z, self.left(y))
                    else:
                        self._fix_deficit(z, self.right(y))
