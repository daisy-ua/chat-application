import time

from services.constants import Key
from services.redis_server import RedisServer
from services.neo4j_server import neo4j


class User:
    def __init__(self, username, admin: bool = False):
        self.username = username
        self.admin = admin
        self.redis = RedisServer().conn
        self.save() if not self.load(self.username) else None
        self.login()

    def login(self):
        self.redis.sadd(Key.ONLINE_USERS, self.username)
        log_msg = 'User {0} logged in at {1}'.format(self.username, time.ctime())
        self.redis.publish(Key.LOG_CHANNEL, log_msg)

    def save(self):
        self.redis.hset('{0}:{1}'.format(Key.ALL_USERS, self.username),
                        mapping={'username': self.username, 'admin': str(self.admin)})
        neo4j.add_user(self.username)
        log_msg = 'User {0} registered at {1}'.format(self.username, time.ctime())
        self.redis.publish(Key.LOG_CHANNEL, log_msg)

    def load(self, username):
        user = self.redis.hgetall('{0}:{1}'.format(Key.ALL_USERS, username))
        return user if user else None

    def __del__(self):
        self.redis.srem(Key.ONLINE_USERS, self.username)
        log_msg = 'User {0} logged out at {1}'.format(self.username, time.ctime())
        self.redis.publish(Key.LOG_CHANNEL, log_msg)
