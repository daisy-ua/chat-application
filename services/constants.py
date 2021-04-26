class Key:
    ALL_USERS = "users"
    ONLINE_USERS = "users_online"
    MESSAGE_DATA = "message_data"

    LOG_CHANNEL = "log_channel"
    SPAM_CHANNEL = "spam_channel"
    MESSAGE_CHANNEL = "message_channel"

    MESSAGE_QUEUE = "message_queue"
    INCOMING_MESSAGES = "incoming_messages"

    ACTIVE_SENDERS = "active_users"
    ACTIVE_SPAMMERS = "active_spammers"

    CREATED_MESSAGES = "created_messages"
    PUBLISHED_MESSAGES = "published_messages"
    IN_MODERATION_MESSAGES = "in_moderation_messages"
    BLOCKED_MESSAGES = "blocked_messages"
    SENT_MESSAGES = "message_sent"
    READ_MESSAGES = "read_messages"


class MessageStatus:
    CREATED = "created"
    IN_QUEUE = "in_queue"
    IN_MODERATION = "in_moderation"
    BLOCKED_BY_SPAM = "blocked_by_spam"
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


class Colors:
    YELLOW = "\033[38;5;208m"
    WHITE = "\033[38;5;231m"
    RED = "\033[31m"
    GREEN = "\033[32m"
