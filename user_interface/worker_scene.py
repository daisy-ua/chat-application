import user_interface.print_method as print_method
from services.chat_controller import ChatController
from services.constants import Colors
from services.neo4j_server import neo4j


GET_MESSAGE_QUEUE = 1
SELECT_MESSAGE = 2

BACK = 0

options = [
    '1. get message queue',
    '2. select message',
    '0. back'
]


def get_message_queue():
    queue = ChatController.get_message_queue()
    print_method.print_enumerated_list(queue, 'Message queue: [{0}]'.format(len(list(queue))))


def select_message_from_queue():
    while True:
        index = int(input(f'{Colors.WHITE}Select index: ----> '))

        try:
            message = ChatController.get_selected_message_from_queue(index - 1)
        except IndexError:
            print_method.print_warning_message('Out of index. Try again.')
            continue

        print_method.print_info_message('Selected object: ')
        print_method.print_dict(message.__dict__)

        process_message(message)
        break


def process_message(message):
    print_method.print_info_message('\nChecking for spam.. ')

    if ChatController.is_spam(message.content):
        print_method.print_warning_message('Spam detected! Blocking this message?')
        ChatController.block_massage(message)
        neo4j.set_spam_message(message)

        return

    print_method.print_info_message('No spam detected! Sending this message...')
    ChatController.send_message(message)


def load_worker_scene():
    print_method.print_info_message('You logged in as worker.')

    while True:
        print_method.print_initial(options)

        option = int(input("----> "))

        if option == GET_MESSAGE_QUEUE:
            get_message_queue()

        if option == SELECT_MESSAGE:
            select_message_from_queue()

        if option == BACK:
            break

        continue
