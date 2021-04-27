from services.chat_controller import ChatController
import user_interface.print_method as pm


READ_LOGS = 1
GET_ONLINE_USERS = 2
GET_ACTIVE_SENDERS = 3
GET_ACTIVE_SPAMMERS = 4
BACK = 0

TOP_USERS_NUMBER = 5


admin_options = [
    '1. read logs',
    '2. show online users',
    '3. show most active senders',
    '4. show most active spammers',
    '0. back'
]


def get_online_users():
    users = ChatController.get_online_users()
    pm.print_initial(users, message='\nOnline users: ')


def get_active_senders():
    users = ChatController.get_active_senders(TOP_USERS_NUMBER)
    pm.print_initial(users, message='\nTop {0} senders:'.format(TOP_USERS_NUMBER))


def get_active_spammers():
    users = ChatController.get_active_spammers(TOP_USERS_NUMBER)
    pm.print_initial(users, message='\nTop {0} spammers:'.format(TOP_USERS_NUMBER))


def read_logs():
    listener = ChatController.get_logs_subscriber()

    for message in listener.listen():
        if message.get('type') == 'message':
            channel = message.get('channel')
            data = message.get('data')
            print('%s: %s' % (channel, data))


def show_admin_menu(user):
    pm.print_info_message('\nYou logged in as admin.')

    while True:
        pm.print_initial(admin_options)

        option = int(input("----> "))

        if option == READ_LOGS:
            read_logs()

        if option == GET_ONLINE_USERS:
            get_online_users()

        if option == GET_ACTIVE_SENDERS:
            get_active_senders()

        if option == GET_ACTIVE_SPAMMERS:
            get_active_spammers()

        if option == BACK:
            break

        continue


