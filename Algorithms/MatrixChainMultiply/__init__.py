

class MatrixChainMultiply(object):
    @classmethod
    def do(cls, size_chain):
        """

        :param size_chain: A2,3 * B3,4 -> size_chain = [2, 3, 4]
        :return:
        """

        _len = len(size_chain) - 1
        _matrix = [[0] * _len for _ in range(_len)]
        for _index in range(1, _len):
            for i in range(_len - _index):
                j = i + _index
                _matrix[i][j] = min(
                    _matrix[i][k] + _matrix[k][j] + size_chain[i] * size_chain[k + 1] * size_chain[j + 1]
                    for k in range(i, j)
                )

        return _matrix


if __name__ == '__main__':
    _l = [2, 3, 6, 4, 5, 7]
    print(MatrixChainMultiply.do(_l))
