"""
二叉搜索树
"""

from DataStructure.Tree import LinkBinaryTree
from DataStructure.Mapping import MapBase


class TreeMap(LinkBinaryTree, MapBase):
    class Position(LinkBinaryTree.Position):
        def key(self):
            _item = self.element()
            return _item.key

        def value(self):
            _item = self.element()
            return _item.value

    def __subtree_search(self, position, key):
        _walk = position
        while True:
            if key == _walk.key():
                return _walk
            elif key < _walk.key():
                _left = self.left(_walk)
                if _left is not None:
                    _walk = _left
                else:
                    return _walk
            else:
                _right = self.right(_walk)
                if _right is not None:
                    _walk = _right
                else:
                    return _walk

    def __subtree_first_position(self, position):
        _walk = position
        while self.left(_walk) is not None:
            _walk = self.left(_walk)

        return _walk

    def __subtree_last_position(self, position):
        _walk = position
        while self.right(_walk) is not None:
            _walk = self.right(_walk)

        return _walk

    def first(self):
        return self.__subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self):
        return self.__subtree_last_position(self.root()) if len(self) > 0 else None

    def before(self, position):
        self.validate(position)
        _left = self.left(position)
        if _left is not None:
            return self.__subtree_last_position(_left)
        else:
            _walk = position
            _above = self.parent(_walk)
            while _above is not None and _walk == self.left(_above):
                _walk = _above
                _above = self.parent(_walk)

            return _above

    def after(self, position):
        self.validate(position)
        _right = self.right(position)
        if _right is not None:
            return self.__subtree_first_position(_right)
        else:
            _walk = position
            _above = self.parent(_walk)
            while _above is not None and _walk == self.right(_above):
                _walk = _above
                _above = self.parent(_walk)

            return _above

    def find_position(self, key):
        if self.is_empty():
            return None
        else:
            _position = self.__subtree_search(self.root(), key)
            self.re_balance_access(_position)
            return _position

    def re_balance_access(self, position):
        pass

    def re_balance_insert(self, position):
        pass

    def re_balance_delete(self, position):
        pass

    def find_min(self):
        if self.is_empty():
            return None
        else:
            _position = self.first()
            return _position.key(), _position.value

    def find_ge(self, key):
        if self.is_empty():
            return None
        else:
            _position = self.find_position(key)
            if _position.key() > key:
                _position = self.before(_position)

            return (_position.key(), _position.value) if _position is not None else None

    def find_range(self, start, stop):
        if not self.is_empty():
            if start is None:
                _position = self.first()
            else:
                _position = self.find_position(start)
                if _position.key() < start:
                    _position = self.after(_position)

            while _position is not None and (stop is not None and _position.key() < stop):
                yield _position.key(), _position.value()
                _position = self.after(_position)

    def __getitem__(self, key):
        if self.is_empty():
            raise KeyError('key error: ' + repr(key))
        else:
            _position = self.__subtree_search(self.root(), key)
            if _position.key() != key:
                raise KeyError('key error: ' + repr(key))

            return _position.value()

    def __setitem__(self, key, value):
        if self.is_empty():
            _leaf = self.add_root(self.Item(key, value))
        else:
            _position = self.__subtree_search(self.root(), key)
            if _position.key() == key:
                _position.element().value = value
                self.re_balance_access(_position)
                return
            else:
                _item = self.Item(key, value)
                if _position.key() > key:
                    _leaf = self.add_left(_position, _item)
                else:
                    _leaf = self.add_right(_position, _item)

        self.re_balance_insert(_leaf)

    def __iter__(self):
        _position = self.first()
        while _position is not None:
            yield _position.key()
            _position = self.after(_position)

    def delete(self, position):
        self.validate(position)
        if self.left(position) and self.right(position):
            _replace_position = self.__subtree_last_position(self.left(position))
            self.replace(position, _replace_position.element())
            position = _replace_position

        _parent = self.parent(position)
        super(TreeMap, self).delete(position)
        self.re_balance_delete(_parent)

    def __delitem__(self, key):
        if not self.is_empty():
            _position = self.__subtree_search(self.root(), key)
            if key == _position.key():
                self.delete(_position)
                return

            self.re_balance_delete(_position)

        raise KeyError('key error: ' + repr(key))

    @staticmethod
    def _relink(parent, child, make_left_child):
        if make_left_child:
            parent.left = child
        else:
            parent.right = child

        if child is not None:
            child.parent = parent

    def _rotate(self, position):
        x = position.node
        y = x.parent
        z = y.parent
        if z is None:
            self.root_node = x
            x.parent = None
        else:
            self._relink(z, x, y == z.left)

        if x == y.left:
            self._relink(y, x.right, True)
            self._relink(x, y, False)
        else:
            self._relink(y, x.left, False)
            self._relink(x, y, True)

    def _restructure(self, x):
        y = self.parent(x)
        z = self.parent(y)
        if (x == self.right(y)) == (y == self.right(z)):
            self._rotate(y)
            return y
        else:
            self._rotate(x)
            self._rotate(x)
            return x
