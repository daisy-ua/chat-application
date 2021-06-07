import time
from services.constants import MessageStatus, Key
from services.redis_server import RedisServer


class Message:
    def __init__(self, sender, recipients, content=None, msg_id=None, status=None, tags=','):
        self.redis = RedisServer().conn
        self.sender = sender
        self.recipients = recipients
        self.content = content
        self.msg_id = msg_id
        self.status = status
        self.tags = tags

    def __get_id__(self):
        return '{0}:{1}:{2}'.format(self.sender, self.recipients, time.ctime())

    def set_data(self, content: str, tags=','):
        self.content = content
        self.tags = tags
        self.msg_id = self.__get_id__()
        self.status = MessageStatus.CREATED

    def __convert_to_dict__(self):
        return {
            'sender': self.sender,
            'recipients': self.recipients,
            'content': self.content,
            'msg_id': self.msg_id,
            'status': self.status,
            'tags': self.tags,
        }

    def save(self):
        self.redis.hset('{0}:{1}'.format(Key.MESSAGE_DATA, self.msg_id), mapping=self.__convert_to_dict__())

    @staticmethod
    def load(redis, message_id):
        message = redis.hgetall("{0}:{1}".format(Key.MESSAGE_DATA, message_id))
        return Message(**message) if message else None
