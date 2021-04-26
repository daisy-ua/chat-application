from services.chat_controller import ChatController
from services.constants import Colors
from services.message import Message
import user_interface.print_method as pm

SEND_MESSAGE = 1
READ_MESSAGES = 2
GET_USER_MESSAGES_INFO = 3
BACK = 0

user_options = [
    '1. send message',
    '2. read messages',
    '3. show my message info',
    '0. back'
]


def send_message(user):
    while True:
        recipient_username = input('Recipient: ----> ')

        if not user.load(recipient_username):
            pm.print_warning_message('The user {0} does not exist! Try again.'.format(recipient_username))
            continue

        content = input(f'{Colors.WHITE}Content: ---> ')

        message = Message(user.username, recipient_username)
        message.set_data(content)
        ChatController.create_message(message)

        confirm = input(f'{Colors.WHITE}Confirm[y/n]: ----> ')

        if confirm == 'y':
            ChatController.publish_message(message)
            break
        else:
            continue


def read_message(user):
    while True:
        messages = list(ChatController.get_incoming_messages(user))

        if len(messages) == 0:
            pm.print_info_message('\nNo new messages!')
            break

        pm.print_enumerated_list(messages, message='Unread message ids:')

        index = int(input(f'{Colors.WHITE}\nSelect index to get detailed info ----> '))
        try:
            message = ChatController.convert_to_message_object(messages[index - 1])
        except IndexError:
            pm.print_warning_message('\nOut of index. Try again.')
            continue

        ChatController.read_message(message)

        pm.print_info_message('\nSelected object: ')
        pm.print_dict_minimized(message.__dict__)

        break


def get_user_messages_info(user):
    msg_info = ChatController.get_user_messages(user)
    pm.print_info_message('\nMessage statistic:')
    pm.print_dict(msg_info)


def show_user_menu(user):
    pm.print_info_message('\nYou logged in as {0}.'.format(user.username))

    while True:
        pm.print_initial(user_options)

        option = int(input("----> "))

        if option == SEND_MESSAGE:
            send_message(user)

        if option == READ_MESSAGES:
            read_message(user)

        if option == GET_USER_MESSAGES_INFO:
            get_user_messages_info(user)

        if option == BACK:
            break

        continue

