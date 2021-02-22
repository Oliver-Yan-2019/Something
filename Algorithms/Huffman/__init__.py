from DataStructure.Heap import HeapPriorityQueue
from DataStructure.Stack import ArrayStack
from DataStructure.Tree import LinkBinaryTree


class Huffman(object):
    @classmethod
    def do(cls, sequence: str):
        _heap = HeapPriorityQueue()
        for char in set(sequence):
            _freq = sequence.count(char)
            _tree = LinkBinaryTree()
            _tree.add_root((_freq, char))
            _heap.add(_freq, _tree)
            
        while len(_heap) > 1:
            (_f1, _tree1) = _heap.remove_min()
            (_f2, _tree2) = _heap.remove_min()
            
            _tree = LinkBinaryTree()
            _f = _f1 + _f2
            _tree.add_root((_f, None))
            _tree.attach(_tree.root(), _tree1, _tree2)
            
            _heap.add(_f, _tree)
            
        (_f, _tree) = _heap.remove_min()
        return _tree
    
    
if __name__ == '__main__':
    _sequence = "I am a superman"
    _t = Huffman.do(_sequence)

    for _p in _t.positions():
        if isinstance(_p.element()[1], str):
            _q = ArrayStack()
            while _p is not None:
                _q.push(_p)
                _p = _t.parent(_p)

            _numbers = []
            while not _q.is_empty():
                _p = _q.pop()
                if _t.parent(_p):
                    _numbers.append(_t.right(_t.parent(_p)) == _p)

            print(_p.element()[0], _p.element()[1], ''.join("1" if _e else "0" for _e in _numbers))
