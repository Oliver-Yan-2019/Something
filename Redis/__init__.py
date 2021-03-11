from redis import StrictRedis


class RedisClient(object):
    def __init__(self, url, db=None, name='default', health_check_interval=30):
        """create a redis client.

        Args:
            url: redis server url.
            db: redis database, default 0.
            name: client name, default 'default'.
            health_check_interval: how many seconds to check whether the redis server is healthy.
        """

        self.client = StrictRedis.from_url(
            url=url,
            db=db,
            client_name=name,
            health_check_interval=health_check_interval,
            decode_responses=True
        )

    def exists(self, *keys):
        """check whether these keys exists.

        Args:
            *keys: these key need to check.

        Returns:

        """

        return self.client.exists(*keys) == len(keys)

    def expire(self, key, seconds):
        """

        Args:
            key:
            seconds:

        Returns:

        """

        self.client.expire(key, seconds)

    def set(self, key, value, expire=None, p_expire=None, nx=None, xx=None):
        """set string, int or float object.

        Args:
            key: the key of object.
            value: the value of object.
            expire: expire time, unit second.
            p_expire: expire time, unit millisecond.
            nx: set if the key doesn't exists.
            xx: set if the key exists.

        Returns:

        """

        self.client.set(
            key, value,
            ex=expire,
            px=p_expire,
            nx=nx,
            xx=xx
        )

    def get(self, key):
        """get the value of object whose key is key.

        Args:
            key: the key of object.

        Returns:

        """

        return self.client.get(key)

    def delete(self, key):
        """

        Args:
            key:

        Returns:

        """

        self.client.delete(key)

    def expires(self, keys, seconds):
        """

        Args:
            keys:
            seconds:

        Returns:

        """

        pipeline = self.client.pipeline()
        for key in keys:
            pipeline.expire(key, seconds)

        pipeline.execute()

    def multi_set(self, mapping, seconds=None):
        """

        Args:
            mapping:
            seconds:

        Returns:

        """

        self.client.mset(mapping)
        if seconds is not None:
            self.expires(mapping.keys(), seconds)

    def multi_get(self, keys):
        """

        Args:
            keys:

        Returns:

        """

        pipeline = self.client.pipeline()
        for key in keys:
            pipeline.get(key)

        return pipeline.execute()

    def multi_delete(self, keys):
        """

        Args:
            keys:

        Returns:

        """

        pipeline = self.client.pipeline()
        for key in keys:
            pipeline.delete(key)

        pipeline.execute()

    def scan(self, cursor=0, match=None, count=None, type_=None):
        """

        Args:
            cursor:
            match:
            count:
            type_:

        Returns:

        """

        _cursor, _list = self.client.scan(
            cursor=cursor,
            match=match,
            count=count,
            _type=type_
        )
        return {'cursor': _cursor, 'list': _list}

    def list_len(self, key):
        """

        Args:
            key:

        Returns:

        """

        return self.client.llen(key)

    def right_push(self, key, item):
        """

        Args:
            key:
            item:

        Returns:

        """

        self.client.rpush(key, item)

    def left_pop(self, key):
        """

        Args:
            key:

        Returns:

        """

        return self.client.lpop(key)

    def block_left_pop(self, key, timeout=0):
        """

        Args:
            key:
            timeout:

        Returns:

        """

        return self.client.blpop(key, timeout=timeout)

    # implement other command if you need.


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
