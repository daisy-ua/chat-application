import redis


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class RedisServer(object):
    def __init__(self):
        self._conn = redis.StrictRedis(charset="utf-8", decode_responses=True)

    @property
    def conn(self):
        return self._conn

