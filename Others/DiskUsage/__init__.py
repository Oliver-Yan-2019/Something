import os


def disk_usage(path):
    """
    相当于linux的du命令
    :param path:
    :return:
    """

    total = os.path.getsize(path)
    if os.path.isdir(path):
        for filename in os.listdir(path):
            child_path = os.path.join(path, filename)
            total += disk_usage(child_path)
            
    print('{0:<7} Bytes: '.format(total), path)
    return total


if __name__ == '__main__':
    disk_usage('/Users/oliver/Downloads')
