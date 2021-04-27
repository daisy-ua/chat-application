from services.user import User
from user_interface.user_scene import show_user_menu
from user_interface.admin_scene import show_admin_menu
from user_interface.worker_scene import load_worker_scene
from user_interface.emulator import load_emulator_scene
from user_interface.print_method import print_initial

WORKER = 1
USER = 2
EMULATOR = 3
EXIT = 4

menu = [
    '1. worker',
    '2. user',
    '3. emulator',
    '4. exit'
]


def login_as_user():
    username = input("Username: ")
    user = User(username, True if username == 'admin' else False)

    if bool(user.admin):
        show_admin_menu(user)
    else:
        show_user_menu(user)


def load():
    while True:
        print_initial(menu)

        option = int(input("----> "))

        if option == WORKER:
            load_worker_scene()

        if option == USER:
            login_as_user()

        if option == EMULATOR:
            load_emulator_scene()

        if option == EXIT:
            print("bye!")
            break

        continue

