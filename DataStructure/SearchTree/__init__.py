from DataStructure.SearchTree.BinarySearchTree import LinkBinaryTree
from DataStructure.SearchTree.AVLTreeMap import AVLTreeMap


if __name__ == '__main__':
    _tree = LinkBinaryTree()
    _tree.add_root((1, 1))

    for _node in _tree:
        print(_node[0], _node[1])

    _avl_tree = AVLTreeMap()
    _avl_tree[1] = 1
    _avl_tree[2] = 1
    _avl_tree[3] = 1
    _avl_tree[4] = 1
    _avl_tree[5] = 1

    for _key, _value in _avl_tree.items():
        print(_key, _value)
