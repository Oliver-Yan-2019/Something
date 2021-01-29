class CaesarCipher(object):
    """凯撒密码"""
    def __init__(self, shift):
        encoder = []
        decoder = []
        for i in range(26):
            encoder.append(chr((i + shift) % 26 + ord('A')))
            decoder.append(chr((i - shift) % 26 + ord('A')))

        self.__forward = ''.join(encoder)
        self.__backward = ''.join(decoder)

    def encrypt(self, message):
        return self.__transform(message, self.__forward)

    def decrypt(self, secret):
        return self.__transform(secret, self.__backward)

    @staticmethod
    def __transform(original, code):
        msg = list(original)
        for i in range(len(msg)):
            if msg[i].isupper():
                j = ord(msg[i]) - ord('A')
                msg[i] = code[j]

        return ''.join(msg)


if __name__ == '__main__':
    _cipher = CaesarCipher(3)
    _message = "I'M GOD!"

    coded = _cipher.encrypt(_message)
    print('Secret: ', coded)

    answer = _cipher.decrypt(coded)
    print('Answer: ', answer)
