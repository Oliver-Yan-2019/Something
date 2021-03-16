# 第一种方式
from concurrent.futures import ThreadPoolExecutor, as_completed
# 第二种方式
import threading

import requests
import time

URL = 'https://cn.bing.com/search?'
'q=python+%e5%a4%9a%e8%bf%9b%e7%a8%8b%e4%b8%8e%e5%a4%9a%e7%ba%bf%e7%a8%8b&FORM=QSRE1'


def write_file(file_name):
    response = requests.get(url=URL)

    with open(file_name, 'w') as f:
        f.write(response.content.decode())

    return 'finish'


def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()[:63]


def main():
    t1 = int(time.time() * 1000)
    _list = [f'file_{i}.html' for i in range(1, 6)]

    with ThreadPoolExecutor(max_workers=5) as executor:
        # 方法一：直接使用executor执行所有任务
        _re_list = executor.map(write_file, _list)

    t2 = int(time.time() * 1000)
    print('write1 time cost', t2 - t1, 'ms')

    with ThreadPoolExecutor(max_workers=5) as executor:
        # 方法二：使用submit来一个一个任务添加，并通过as_completed方法获取到已经执行完成的futures，使用futures.result获取结果
        _todo = []
        for i in _list:
            _f = executor.submit(write_file, i)
            _todo.append(_f)
            print(f'Schedule:{i}')

        for i in as_completed(_todo):
            print(f'Completed:{i.result()}')

    t3 = int(time.time() * 1000)
    print('write2 time cost', t3 - t2, 'ms')

    # 单线程

    # 结果
    for i in _list:
        _f = read_file(i)
        print(i, ':', _f)


if __name__ == '__main__':
    main()
