from Redis.client import RedisClient


class RedisQueue(object):
    def __init__(self, name='default', namespace='default', capacity=None, client=None):
        """

        Args:
            name:
            namespace:
            capacity:
            client:
        """

        self.client: RedisClient = client
        self.name = name
        self.namespace = namespace
        self.capacity = capacity

        self.key = f'Q:{namespace}:{name}'

    def size(self):
        """

        Returns:

        """

        return self.client.list_len(self.key)

    def is_empty(self):
        """

        Returns:

        """

        return self.size() == 0

    def push(self, item):
        """

        Args:
            item:

        Returns:

        """

        if self.capacity is not None:
            if self.size() >= self.capacity:
                raise Exception(f'redis queue <{self.key}> is full!')

        self.client.right_push(self.key, item)

    def block_pop(self, block=True, timeout=0):
        """

        Args:
            block: if block.
            timeout:

        Returns:

        """

        if block:
            item = self.client.block_left_pop(self.key, timeout=timeout)
            item = item[1] if item else None
        else:
            item = self.client.left_pop(self.key)

        return item

    def pop(self):
        """

        Returns:

        """

        return self.block_pop(False)


class RedisList(object):
    def __init__(self, name='default', namespace='default', client=None):
        self.name = name
        self.namespace = namespace
        self.client = client

        self.key = f'L:{namespace}:{name}'


if __name__ == '__main__':
    _client = RedisClient(url='redis://localhost:6379')
    print(_client.exists('test'))
    _client.set('test', 'test', expire=30)
    print(_client.get('test'))
    _client.delete('test')

    _client.multi_set({'test1': 'test1', 'test2': 'test2'})
    print(_client.multi_get(['test1', 'test2']))
    print(_client.scan(0, '*', 10, 'string'))
    _client.multi_delete(['test1', 'test2'])

    _queue = RedisQueue(client=_client, capacity=10)
    for i in range(10):
        _queue.push(i)

    for i in range(10):
        print(_queue.pop())
