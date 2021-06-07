from neo4j import GraphDatabase
import services.server_config as conf


class Neo4jServer:
    def __init__(self, user, password):
        self.driver = GraphDatabase.driver('neo4j://localhost:7687', auth=(user, password))

    def close(self):
        self.driver.close()

    def add_massage(self, message):
        with self.driver.session() as session:
            session.write_transaction(self.__add_message, message)

    def add_user(self, username):
        with self.driver.session() as session:
            session.write_transaction(self.__register_user, username)

    def get_users_by_tag(self, tag):
        with self.driver.session() as session:
            query = [f"MATCH (tag:Tag) where tag.name in ['{tag}']", "MATCH (msg:Message)-[*]->(tag)",
                     "MATCH (sender:User)-[:SENT]->(msg)-[:TO]->(recipient:User)",
                     "RETURN sender.username as username"]
            return list(session.run('\n'.join(query)))

    def get_pairs_by_msg_len(self, len):
        with self.driver.session() as session:
            query = ["MATCH (user1:User)", "MATCH (user2:User)",
                     f"MATCH (user1)-[:SENT|TO*{len}]-(user2) where user1.username <> user2.username",
                     "RETURN user1.username as u1, user2.username as u2"]
            return list(session.run('\n'.join(query)))

    def get_shortest_way(self, user1, user2):
        with self.driver.session() as session:
            query = [f"MATCH (user1:User {{username: '{user1}'}})",
                     f"MATCH (user2:User {{username: '{user2}'}})",
                     "with shortestPath((user1)-[:SENT|TO*]-(user2)) as path",
                     "RETURN path"]
            return list(session.run('\n'.join(query)))

    def get_shortest_way_count(self, user1, user2):
        with self.driver.session() as session:
            query = [f"MATCH (user1:User {{username: '{user1}'}})",
                     f"MATCH (user2:User {{username: '{user2}'}})",
                     "with shortestPath((user1)-[:SENT|TO*]-(user2)) as path",
                     "RETURN size(nodes(path))"]
            return session.run('\n'.join(query)).single()[0]

    def set_spam_message(self, message):
        with self.driver.session() as session:
            session.run("MATCH (u1:User)-[msg:Message]->(u2:User) WHERE msg.id IN msg.all AND NOT msg.id IN msg.spam "
                        "SET msg.spam = msg.spam + $id", id=message.msg_id)

    def get_users_with_spam_messages_only(self):
        with self.driver.session() as session:
            res = session.run("MATCH p = (u1:User)-[]-(u2:User) WHERE u1 <> u2 AND all(x in relationships(p)"
                              "WHERE x.all = x.spam) RETURN u1, u2")
            return list(res)

    def get_unrelated_by_tags(self, tag):
        users = self.get_users_by_tag(tag)
        users = list(set(users))
        unrelated_users = []
        for user1 in users:
            pair = [user1['username']]
            for user2 in users:
                if user1['username'] != user2['username'] and user2['username'] not in pair:
                    nodes_count = self.get_shortest_way_count(user1['username'], user2['username'])
                    if nodes_count > 3:
                        pair.append(user2['username'])
            unrelated_users.append(pair)
        return unrelated_users

    @staticmethod
    def __add_message(tx, message):
        tags = message.tags.split(',')
        query = ["CREATE (msg:Message {id: $id})"]
        for index, tag in enumerate(tags):
            if tag != '' and tag is not None:
                query.append(f"MERGE (tag{index}:Tag {{ name: '{tag}' }})")
                query.append(f"CREATE (msg)-[:CONTAINS_TAG]->(tag{index})")
        query.append("MERGE (sender:User {username: $sender})")
        query.append("MERGE (recipient:User {username: $recipient})")
        query.append("MERGE (sender)-[:SENT {to: $recipient}]->(msg)")
        query.append("MERGE (msg)-[:TO {from: $sender}]->(recipient)")

        print('\n' + message.sender + '\n' + message.recipients)
        tx.run(
            '\n'.join(query),
            id=message.msg_id,
            sender=message.sender,
            recipient=message.recipients
        )

    @staticmethod
    def __register_user(tx, username):
        users = tx.run('MATCH (user:User {username: $username}) RETURN user', username=username)
        for user in users:
            existing_username = user['user']['username']
            print(existing_username, username)
            if existing_username == username:
                return
        tx.run(
            "MERGE (user:User {username: $username})",
            username=username
        )


neo4j = Neo4jServer(conf.USERNAME, conf.PASSWORD)
