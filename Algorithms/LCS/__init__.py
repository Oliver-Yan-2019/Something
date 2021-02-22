

class LCS(object):
    @classmethod
    def do(cls, x, y):
        """
        O(x_len * y_len)
        :param x:
        :param y:
        :return:
        """

        x_len, y_len = len(x), len(y)
        l_ = [[0] * (y_len + 1) for _ in range(x_len + 1)]
        for j in range(x_len):
            for k in range(y_len):
                if x[j] == y[k]:
                    l_[j + 1][k + 1] = l_[j][k] + 1
                else:
                    l_[j + 1][k + 1] = max(l_[j][k + 1], l_[j + 1][k])

        return cls._solution(x, y, l_)

    @classmethod
    def _solution(cls, x, y, l_):
        _solution = []
        x_len, y_len = len(x), len(y)
        while l_[x_len][y_len] > 0:
            if x[x_len - 1] == y[y_len - 1]:
                _solution.append(x[x_len - 1])
                x_len -= 1
                y_len -= 1
            elif l_[x_len - 1][y_len] >= l_[x_len][y_len - 1]:
                x_len -= 1
            else:
                y_len -= 1

        return ''.join(reversed(_solution))


if __name__ == '__main__':
    _x = 'qwerdfghjklcghgdfkhaljdflvbkajdsfkjlnm'
    _y = 'qwerdfghjklcghgdfkhlvbkajdsfkjlnm'
    print(_x)
    print(_y)
    print(LCS.do(_x, _y))
