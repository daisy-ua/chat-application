from services.constants import Colors


def print_initial(options, message="\nSelect option to continue:"):
    print(f"{Colors.YELLOW}%s" % message)
    for item in options:
        print(f"{Colors.WHITE}%s" % item)


def print_enumerated_list(options, message):
    print(f"{Colors.GREEN}%s" % message)
    for index, item in enumerate(options):
        print(f"{Colors.WHITE}%i. %s" % (index + 1, item))


def print_dict(d):
    for key in d.keys():
        print(Colors.YELLOW, key, ': ', Colors.WHITE, d[key])


def print_dict_minimized(d):
    print(Colors.YELLOW, 'from: ', ': ', Colors.WHITE, d['sender'])
    print(Colors.YELLOW, 'body: ', ': ', Colors.WHITE, d['content'])


def print_warning_message(message):
    print(f'{Colors.RED}%s' % message)


def print_info_message(message):
    print(f'{Colors.GREEN}%s' % message)
