from services.neo4j_server import neo4j

tags = [
    'ads', 'swag', 'kpop', 'vegan', 'solotravel', 'puppylove', 'vr', 'bts', 'bantansonyendan',
    'fitfam', 'cardio', 'giveaway', 'weddinghair'
]

OPTIONS = []


def get_users_by_tags():
    for tag in tags:
        users = neo4j.get_users_by_tag(tag)
        users = list(set(users))
        if len(users) != 0:
            print("For tag '{0}'".format(tag))
            for user in users:
                print(user['username'])


def get_pairs_by_msg_len(len):
    pairs = neo4j.get_pairs_by_msg_len(len)
    pairs = list(set(pairs))
    for pair in pairs:
        print(pair['u1'] + " : " + pair['u2'])


def load_neo4j_scene():
    get_users_by_tags()

    # get_pairs_by_msg_len(2)

    # users = neo4j.get_unrelated_by_tags('cardio')
    # print(len(users))
    # for lis in users:
    #     print(lis)
