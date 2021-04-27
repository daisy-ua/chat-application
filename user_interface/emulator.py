import random
import time

from services.chat_controller import ChatController
from user_interface.worker_scene import process_message
from services.message import Message
from services.user import User
from user_interface.print_method import print_info_message

usernames = [
    'Frank', 'Fiona', 'Lip', 'Ian', 'Debbie', 'Carl', 'Liam'
]

listener = ChatController.get_message_subscriber()


def publish_message(user):
    recipient = random.choice(usernames)
    message = Message(user.username, recipient)
    message.set_data('{0} -> {1}: {2}'.format(message.sender, message.recipients, message.msg_id))
    print('User %s sending new message to %s' % (message.sender, message.recipients))
    ChatController.create_message(message)
    ChatController.publish_message(message)


def read_message(user):
    messages = list(ChatController.get_incoming_messages(user))

    if len(messages) == 0:
        print_info_message('User {0} has no messages'.format(user.username))
        return

    msg_id = messages[0] if len(messages) == 1 else messages[random.randrange(0, len(messages) - 1, 1)]

    message = ChatController.convert_to_message_object(msg_id)
    print_info_message('{0} read a message from {1}'.format(message.recipients, message.sender))

    ChatController.read_message(message)


def load_emulator_scene():
    print_info_message('\nYou are in emulator mode\n')

    for username in usernames:
        user = User(username)
        for i in range(1, 2):
            time.sleep(random.random() * 2)
            if not random.getrandbits(1):
                read_message(user)
            publish_message(user)

    try:
        for message in listener.listen():
            if message.get('type') == 'message':
                msg = ChatController.convert_to_message_object(message.get('data'))
                process_message(msg)
    except KeyboardInterrupt:
        pass
