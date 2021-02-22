

class StringMatch(object):
    @classmethod
    def brute(cls, target, pattern):
        """
        穷举法 O(t_len * p_len)
        :param target:
        :param pattern:
        :return:
        """

        t_len, p_len = len(target), len(pattern)
        for i in range(t_len - p_len + 1):
            k = 0
            while k < p_len and target[i + k] == pattern[k]:
                k += 1

            if k == p_len:
                return i

        return - 1

    @classmethod
    def boyer_moore(cls, target, pattern):
        """
        镜像启发式 + 字幕跳跃启发式 O(t_len * p_len)
        :param target:
        :param pattern:
        :return:
        """

        t_len, p_len = len(target), len(pattern)
        if p_len == 0:
            return 0

        _last = {}
        for i, k in enumerate(pattern):
            _last[k] = i

        t_index = p_len - 1
        p_index = p_len - 1
        while t_index < t_len:
            if target[t_index] == pattern[p_index]:
                if p_index == 0:
                    return t_index
                else:
                    t_index -= 1
                    p_index -= 1
            else:
                _l_index = _last.get(target[t_index], -1)
                t_index += p_len - min(p_index, _l_index + 1)
                p_index = p_len - 1

        return -1

    @classmethod
    def knuth_morris_pratt(cls, target, pattern):
        """
        KMP O(t_len + p_len)
        :param target:
        :param pattern:
        :return:
        """

        t_len, p_len = len(target), len(pattern)
        if p_len == 0:
            return 0

        _fail = cls._compute_kmp_fail(pattern)
        t_index = 0
        p_index = 0
        while t_index < t_len:
            if target[t_index] == pattern[p_index]:
                if p_index == p_len - 1:
                    return t_index - p_len + 1

                t_index += 1
                p_index += 1
            elif p_index > 0:
                p_index = _fail[p_index - 1]
            else:
                t_index += 1

        return -1

    @staticmethod
    def _compute_kmp_fail(pattern):
        """
        KMP失败函数
        :param pattern:
        :return:
        """

        p_len = len(pattern)
        _fail = [0] * p_len
        _index = 1
        _c_index = 0
        while _index < p_len:
            if pattern[_index] == pattern[_c_index]:
                _fail[_index] = _c_index + 1
                _index += 1
                _c_index += 1
            elif _c_index > 0:
                _c_index = _fail[_c_index - 1]
            else:
                _index += 1

        return _fail


if __name__ == '__main__':
    print(StringMatch.brute("jasdhfkasjhdkfasdgfkjhaklsjdhflkjhasdkhf", "jhd"))
    print(StringMatch.boyer_moore("jasdhfkasjhdkfasdgfkjhaklsjdhflkjhasdkhf", "jhd"))
    print(StringMatch.knuth_morris_pratt("jasdhfkasjhdkfasdgfkjhaklsjdhflkjhasdkhf", "asdhfkasjhd"))
