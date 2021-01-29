if __name__ == '__main__':
    document = ["a"] * 10000

    # instance 1
    letters = ''
    for c in document:
        if c.isalpha():
            letters += c

    print(letters)

    # instance 2
    temp = []
    for c in document:
        if c.isalpha():
            temp.append(c)

    letters = "".join(temp)
    print(letters)

    # instance 3
    letters = "".join([c for c in document if c.isalpha()])
    print(letters)

    # instance 4
    letters = "".join(c for c in document if c.isalpha())
    print(letters)
