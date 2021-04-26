import time
import random

from services.server import RedisServer
from services.constants import Key, MessageStatus
from services.message import Message

redis = RedisServer().conn


class ChatController:
    @staticmethod
    def create_message(message):
        message.save()
        redis.lpush('{0}:{1}'.format(Key.CREATED_MESSAGES, message.sender), message.msg_id)

    @staticmethod
    def publish_message(message):
        message.status = MessageStatus.IN_QUEUE
        message.save()

        redis.rpush(Key.MESSAGE_QUEUE, message.msg_id)
        redis.lrem('{0}:{1}'.format(Key.CREATED_MESSAGES, message.sender), 1, message.msg_id)
        redis.lpush("{0}:{1}".format(Key.PUBLISHED_MESSAGES, message.sender), message.msg_id)

        log_msg = 'Message {0} was published new message at {1}'.format(message.msg_id, time.ctime())
        redis.publish(Key.MESSAGE_CHANNEL, log_msg)

    @staticmethod
    def send_message(message):
        redis.lrem('{0}:{1}'.format(Key.IN_MODERATION_MESSAGES, message.sender), 1, message.msg_id)
        redis.lrem(Key.MESSAGE_QUEUE, 1, message.msg_id)
        redis.rpush('{0}:{1}'.format(Key.SENT_MESSAGES, message.sender), message.msg_id)
        redis.zincrby(Key.ACTIVE_SENDERS, 1, message.sender)
        redis.rpush('{0}:{1}'.format(Key.INCOMING_MESSAGES, message.recipients), message.msg_id)

        message.status = MessageStatus.SENT
        message.save()

        log_msg = 'Message {0} was sent at {1}'.format(message.msg_id, time.ctime())
        redis.publish(Key.MESSAGE_CHANNEL, log_msg)

    @staticmethod
    def block_massage(message):
        message.status = MessageStatus.BLOCKED_BY_SPAM
        message.save()

        redis.lrem('{0}:{1}'.format(Key.IN_MODERATION_MESSAGES, message.sender), 1, message.msg_id)
        redis.lrem(Key.MESSAGE_QUEUE, 1, message.msg_id)
        redis.lpush('{0}:{1}'.format(Key.BLOCKED_MESSAGES, message.sender), message.msg_id)
        redis.zincrby(Key.ACTIVE_SPAMMERS, 1, message.sender)

        log_msg = 'Message {0} was blocked at {1}'.format(message.msg_id, time.ctime())
        redis.publish(Key.MESSAGE_CHANNEL, log_msg)
        redis.publish(Key.SENT_MESSAGES, log_msg)

    @staticmethod
    def read_message(message):
        message.status = MessageStatus.READ
        message.save()

        redis.lrem('{0}:{1}'.format(Key.SENT_MESSAGES, message.sender), 1, message.msg_id)
        redis.lrem('{0}:{1}'.format(Key.INCOMING_MESSAGES, message.recipients), 1, message.msg_id)
        redis.lpush('{0}:{1}'.format(Key.READ_MESSAGES, message.sender), message.msg_id)

        log_msg = 'Message by {0} was read by {1} at {2}'.format(message.sender, message.recipients, time.ctime())
        redis.publish(Key.MESSAGE_CHANNEL, log_msg)

    @staticmethod
    def get_selected_message_from_queue(index):
        message_id = redis.lrange(Key.MESSAGE_QUEUE, index, index)[0]
        message = Message.load(redis, message_id)

        message.status = MessageStatus.IN_MODERATION
        message.save()

        redis.lrem('{0}:{1}'.format(Key.PUBLISHED_MESSAGES, message.sender), 1, message_id)
        redis.lpush('{0}:{1}'.format(Key.IN_MODERATION_MESSAGES, message.sender), message_id)

        return message

    @staticmethod
    def is_spam(message) -> bool:
        time.sleep(1)
        return bool(random.getrandbits(1))

    @staticmethod
    def get_message_queue():
        return redis.lrange(Key.MESSAGE_QUEUE, 0, -1)

    @staticmethod
    def get_online_users():
        return redis.smembers(Key.ONLINE_USERS)

    @staticmethod
    def get_active_senders(counter):
        return list(map(lambda t: '{0}: {1}'.format(t[0], int(t[1])),
                        redis.zrange(Key.ACTIVE_SENDERS, 0, counter, desc=True, withscores=True)))

    @staticmethod
    def get_active_spammers(counter):
        return list(map(lambda t: '{0}: {1}'.format(t[0], int(t[1])),
                        redis.zrange(Key.ACTIVE_SPAMMERS, 0, counter, desc=True, withscores=True)))

    @staticmethod
    def get_incoming_messages(user):
        return redis.lrange('{0}:{1}'.format(Key.INCOMING_MESSAGES, user.username), 0, -1)

    @staticmethod
    def get_user_messages(user):
        return {
            MessageStatus.CREATED: redis.llen('{0}:{1}'.format(Key.CREATED_MESSAGES, user.username)),
            MessageStatus.IN_QUEUE: redis.llen('{0}:{1}'.format(Key.PUBLISHED_MESSAGES, user.username)),
            MessageStatus.IN_MODERATION: redis.llen('{0}:{1}'.format(Key.IN_MODERATION_MESSAGES, user.username)),
            MessageStatus.BLOCKED_BY_SPAM: redis.llen('{0}:{1}'.format(Key.BLOCKED_MESSAGES, user.username)),
            MessageStatus.SENT: redis.llen('{0}:{1}'.format(Key.SENT_MESSAGES, user.username)),
            MessageStatus.READ: redis.llen('{0}:{1}'.format(Key.READ_MESSAGES, user.username)),
        }

    @staticmethod
    def convert_to_message_object(message_id):
        return Message.load(redis, message_id)

    @staticmethod
    def get_logs_subscriber():
        logs = redis.pubsub()
        logs.subscribe(Key.LOG_CHANNEL, Key.MESSAGE_CHANNEL, Key.SPAM_CHANNEL)
        return logs
