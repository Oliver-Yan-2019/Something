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
