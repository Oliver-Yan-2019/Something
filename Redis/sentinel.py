from redis import StrictRedis


class SentinelClient(object):
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


if __name__ == '__main__':
    _client = SentinelClient(url='redis://localhost:26379')
    _pub_sub = _client.client.pubsub()
    _pub_sub.psubscribe('*')
    for i in _pub_sub.listen():
        print(i)
