"""
映射
"""

from abc import abstractmethod, ABCMeta
from typing import *
from random import randrange


class MapBase(MutableMapping, metaclass=ABCMeta):
    class Item(object):
        __slots__ = 'key', 'value'

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __eq__(self, other):
            return self.key == other.key

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            return self.key < other.key


class UnsortedTableMap(MapBase):
    def __init__(self):
        self._table = []

    def __getitem__(self, key):
        for item in self._table:
            if item.key == key:
                return item

        raise KeyError('key error: {}' + repr(key))

    def __setitem__(self, key, value):
        for item in self._table:
            if item.key == key:
                item.value = value
                return

        self._table.append(self.Item(key, value))

    def __delitem__(self, key):
        for index in range(len(self._table)):
            if self._table[index].key == key:
                self._table.pop(index)
                return

        raise KeyError('key error: ' + repr(key))

    def __len__(self):
        return len(self._table)

    def __iter__(self):
        for item in self._table:
            yield item.key


class HashMapBase(MapBase, metaclass=ABCMeta):
    def __init__(self, capacity=11, prime=109345121):
        from random import randrange

        self._table: List[Any] = [None] * capacity
        self._length = 0

        self.__prime = prime
        self.__scale = 1 + randrange(prime - 1)
        self.__shift = randrange(prime)

    def hash_function(self, key):
        """
        MAD
        :param key:
        :return:
        """

        return (hash(key) * self.__scale + self.__shift) % self.__prime % len(self._table)

    def __len__(self):
        return self._length

    def __getitem__(self, key):
        index = self.hash_function(key)
        return self._bucket_getitem(index, key)

    def __setitem__(self, key, value):
        index = self.hash_function(key)
        self._bucket_setitem(index, key, value)
        if self._length > len(self._table) // 2:
            self.__resize(2 * len(self._table) - 1)

    def __delitem__(self, key):
        index = self.hash_function(key)
        self._bucket_delitem(index, key)
        self._length -= 1

    def __resize(self, capacity):
        _old_table = list(self.items())
        self._table = capacity * [None]
        self._length = 0
        for key, value in _old_table:
            self[key] = value

    @abstractmethod
    def _bucket_getitem(self, index, key):
        pass

    @abstractmethod
    def _bucket_setitem(self, index, key, value):
        pass

    @abstractmethod
    def _bucket_delitem(self, index, key):
        pass

    @abstractmethod
    def __iter__(self):
        pass


class ChainHashMap(HashMapBase):
    def _bucket_getitem(self, index, key):
        bucket = self._table[index]
        if bucket is None:
            raise KeyError('key error: ' + repr(key))

        return bucket[key]

    def _bucket_setitem(self, index, key, value):
        if self._table[index] is None:
            self._table[index] = UnsortedTableMap()

        _old_size = len(self._table[index])
        self._table[index][key] = value
        if len(self._table[index]) > _old_size:
            self._length += 1

    def _bucket_delitem(self, index, key):
        bucket = self._table[index]
        if bucket is None:
            raise KeyError('key error: ' + repr(key))

        del bucket[key]

    def __iter__(self):
        for bucket in self._table:
            if bucket is not None and isinstance(bucket, UnsortedTableMap):
                for key in bucket:
                    yield key


class ProbeHashMap(HashMapBase):
    _AVAIL = object()

    def __is_available(self, index):
        return self._table[index] is None or self._table[index] is ProbeHashMap._AVAIL

    def __find_slots(self, index, key):
        first_avail = None
        while True:
            _item = self._table[index]
            if self.__is_available(index):
                if first_avail is None:
                    first_avail = index

                if _item is None:
                    return False, first_avail
            elif isinstance(_item, ProbeHashMap.Item) and key == _item.key:
                return True, index

            index = (index + 1) % len(self._table)

    def _bucket_getitem(self, index, key):
        _exist, _slots = self.__find_slots(index, key)
        if not _exist:
            raise KeyError('key error: ' + repr(key))

        _item = self._table[_slots]
        if isinstance(_item, self.Item):
            return _item.value
        else:
            raise KeyError('value error: ' + repr(key))

    def _bucket_setitem(self, index, key, value):
        _exist, _slots = self.__find_slots(index, key)
        if not _exist:
            self._table[_slots] = self.Item(key, value)
            self._length += 1
        else:
            self._table[_slots].value = value

    def _bucket_delitem(self, index, key):
        _exist, _slots = self.__find_slots(index, key)
        if not _exist:
            raise KeyError('key error: ' + repr(key))

        self._table[_slots] = ProbeHashMap._AVAIL

    def __iter__(self):
        for index in range(len(self._table)):
            if not self.__is_available(index):
                yield self._table[index].key


class SortedTableMap(MapBase):
    def __init__(self):
        self._table = []

    def __len__(self):
        return len(self._table)

    def __getitem__(self, key):
        index = self.__find_index(key)
        if index == len(self._table) or self._table[index].key != key:
            raise KeyError('key error: ' + repr(key))

        return self._table[index].value

    def __setitem__(self, key, value):
        index = self.__find_index(key)
        if index < len(self._table) and self._table[index].key == key:
            self._table[index].value = value
        else:
            self._table.insert(index, self.Item(key, value))

    def __delitem__(self, key):
        index = self.__find_index(key)
        if index == len(self._table) or self._table[index].key != key:
            raise KeyError('key error: ' + repr(key))

        self._table.pop()

    def __iter__(self):
        for item in self._table:
            yield item.key

    def __reversed__(self):
        for item in reversed(self._table):
            yield item.key

    def __find_index(self, key, mode='ge'):
        low = 0
        high = len(self._table) - 1
        while low <= high:
            mid = (low + high) // 2
            if key == self._table[mid].key:
                return mid
            elif key < self._table[mid].key:
                high = mid - 1
            else:
                low = mid + 1

        return high + 1 if mode == 'ge' else low - 1

    def find_min(self):
        if len(self._table) > 0:
            _item = self._table[0]
            return _item.key, _item.value
        else:
            return None

    def find_max(self):
        if len(self._table) > 0:
            _item = self._table[-1]
            return _item.key, _item.value
        else:
            return None

    def find_le(self, key):
        index = self.__find_index(key, mode='le')
        if index >= 0:
            _item = self._table[index]
            return _item.key, _item.value
        else:
            return None

    def find_ge(self, key):
        index = self.__find_index(key)
        if index < len(self._table):
            _item = self._table[index]
            return _item.key, _item.value
        else:
            return None

    def find_lt(self, key):
        index = self.__find_index(key)
        if index > 0:
            _item = self._table[index - 1]
            return _item.key, _item.value
        else:
            return None

    def find_gt(self, key):
        index = self.__find_index(key)
        if index < len(self._table) and self._table[index].key == key:
            index += 1

        if index < len(self._table):
            _item = self._table[index]
            return _item.key, _item.value
        else:
            return None

    def find_range(self, start, stop):
        if start is None:
            index = 0
        else:
            index = self.__find_index(start)

        while index < len(self._table) and (stop is None or self._table[index].key < stop):
            _item = self._table[index]
            yield _item.key, _item.value
            index += 1


class CostPerformanceDatabase(object):
    def __init__(self):
        self.map = SortedTableMap()

    def best(self, cost):
        return self.map.find_le(cost)

    def add(self, cost, performance):
        _item = self.map.find_le(cost)
        if _item is not None and _item[1] > performance:
            return

        self.map[cost] = performance

        _item = self.map.find_gt(cost)
        while _item is not None and _item[1] <= performance:
            del self.map[_item[0]]
            _item = self.map.find_gt(cost)


class SkipTable(MapBase):
    class Node(object):
        def __init__(self, element, next_=None, prev=None, above=None, below=None):
            self.element = element
            self.next = next_
            self.prev = prev
            self.above = above
            self.below = below

    def __init__(self):
        self.start = self.Node((-float('inf'), None))
        self.start.next = self.Node((float('inf'), None), prev=self.start)

        self.height = 0
        self.size = 0

    def __len__(self):
        return self.size

    def __iter__(self):
        _node = self.start
        while _node.below:
            _node = _node.below
            while _node.next.element[0] != float('inf'):
                yield _node.element[0]

    def __search(self, key):
        _node = self.start
        while _node.below is not None:
            _node = _node.below
            while _node.next.element[0] <= key:
                _node = _node.next

        return _node

    def __insert_after_above(self, left, below, element):
        _node = self.Node(element)
        if left is not None:
            _node.next, left.next, _node.prev = left.next, _node, left

        if below is not None:
            _node.above, below.above, _node.below = below.above, _node, below

        return _node

    def __getitem__(self, key):
        _node = self.__search(key)

        if _node is self.start:
            raise KeyError('key error: ' + repr(key))

        return _node.element[1]

    def __setitem__(self, key, value):
        _node = self.__search(key)
        _next_node = None
        _index = -1
        while True:
            _index += 1
            if _index >= self.height:
                self.height += 1
                _stop = self.start.next
                self.start = self.__insert_after_above(None, self.start, (-float('inf'), None))
                self.__insert_after_above(self.start, _stop, (float('inf'), None))

            _next_node = self.__insert_after_above(_node, _next_node, (key, value))

            while _node.above is None:
                _node = _node.prev

            _node = _node.above

            if randrange(2) == 0:
                break

        self.size += 1

    def __delitem__(self, key):
        _node = self.__search(key)
        while _node.above is not None:
            _node.prev.next = _node.next
            _node = _node.above

        if _node is self.start:
            raise KeyError('key error: ' + repr(key))


class MultiMap(object):
    _MAP_TYPE = dict

    def __init__(self):
        self.map = self._MAP_TYPE()
        self.length = 0

    def __iter__(self):
        for key, value in self.map.items():
            for v in value:
                yield v

    def add(self, key, value):
        _container = self.map.setdefault(key, [])
        _container.append(value)
        self.length += 1

    def pop(self, key):
        value = self.map[key]
        v = value.pop()
        if len(value) == 0:
            del self.map[key]

        self.length -= 1
        return key, v

    def find(self, key):
        value = self.map[key]
        return key, value[0]

    def find_all(self, key):
        value = self.map.get(key, [])
        for v in value:
            yield key, v


if __name__ == '__main__':
    _chain = ChainHashMap()

    _chain['a'] = 1
    _chain['b'] = 2
    for i in _chain:
        print(i)
        print(_chain[i].value)

    _probe = ProbeHashMap()

    _probe['a'] = 1
    _probe['b'] = 2
    for i in _probe:
        print(i)
        print(_probe[i])

    _skip = SkipTable()
    _skip[1] = 1
    _skip[2] = 2
    _skip[3] = 3
    _skip[4] = 4
    _skip[5] = 5

    print(_skip[1])
    print(_skip[2])
    print(_skip[3])
    print(_skip[4])
    print(_skip[5])
