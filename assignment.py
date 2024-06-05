from neo4j import GraphDatabase

class SocialNetworkApp:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # User Registration
    def register_user(self, name, age, location, interests):
        with self.driver.session() as session:
            session.execute_write(self._create_user, name, age, location, interests)

    @staticmethod
    def _create_user(tx, name, age, location, interests):
        tx.run("CREATE (:User {name: $name, age: $age, location: $location, interests: $interests})",
               name=name, age=age, location=location, interests=interests)

    def update_user_info(self, name, **kwargs):
        with self.driver.session() as session:
            session.execute_write(self._update_user, name, kwargs)

    @staticmethod
    def _update_user(tx, name, properties):
        set_clause = ", ".join([f"u.{key} = ${key}" for key in properties])
        properties["name"] = name
        tx.run(f"MATCH (u:User {{name: $name}}) SET {set_clause}", **properties)

    # Friend Management
    def send_friend_request(self, from_user, to_user):
        with self.driver.session() as session:
            session.execute_write(self._create_friend_request, from_user, to_user)

    @staticmethod
    def _create_friend_request(tx, from_user, to_user):
        tx.run("MATCH (a:User {name: $from_user}), (b:User {name: $to_user}) "
               "MERGE (a)-[:OUTGOING_REQUEST]->(b)",
               from_user=from_user, to_user=to_user)

    def accept_friend_request(self, from_user, to_user):
        with self.driver.session() as session:
            session.execute_write(self._accept_friend_request, from_user, to_user)

    @staticmethod
    def _accept_friend_request(tx, from_user, to_user):
        tx.run("MATCH (a:User {name: $from_user})-[r:OUTGOING_REQUEST]->(b:User {name: $to_user}) "
               "DELETE r "
               "MERGE (a)-[:FRIENDS_WITH]->(b) "
               "MERGE (b)-[:FRIENDS_WITH]->(a)",
               from_user=from_user, to_user=to_user)

    def unfriend(self, user1, user2):
        with self.driver.session() as session:
            session.execute_write(self._remove_friend, user1, user2)

    @staticmethod
    def _remove_friend(tx, user1, user2):
        tx.run("MATCH (a:User {name: $user1})-[r:FRIENDS_WITH]-(b:User {name: $user2}) DELETE r",
               user1=user1, user2=user2)

    # User Interaction
    def create_post(self, user_name, content):
        with self.driver.session() as session:
            session.execute_write(self._create_post, user_name, content)

    @staticmethod
    def _create_post(tx, user_name, content):
        tx.run("MATCH (u:User {name: $user_name}) "
               "CREATE (u)-[:POSTED]->(:Post {content: $content, timestamp: timestamp()})",
               user_name=user_name, content=content)

    def like_post(self, user_name, post_id):
        with self.driver.session() as session:
            session.execute_write(self._like_post, user_name, post_id)

    @staticmethod
    def _like_post(tx, user_name, post_id):
        tx.run("MATCH (u:User {name: $user_name}), (p:Post) WHERE ID(p) = $post_id "
               "MERGE (u)-[:LIKES]->(p)",
               user_name=user_name, post_id=post_id)

    def comment_on_post(self, user_name, post_id, comment):
        with self.driver.session() as session:
            session.execute_write(self._comment_on_post, user_name, post_id, comment)

    @staticmethod
    def _comment_on_post(tx, user_name, post_id, comment):
        tx.run("MATCH (u:User {name: $user_name}), (p:Post) WHERE ID(p) = $post_id "
               "CREATE (u)-[:COMMENTED_ON {text: $comment}]->(p)",
               user_name=user_name, post_id=post_id, comment=comment)

    # Creative Features
    def recommend_friends(self, user_name):
        with self.driver.session() as session:
            result = session.execute_read(self._recommend_friends, user_name)
            return [record["name"] for record in result]

    @staticmethod
    def _recommend_friends(tx, user_name):
        return tx.run("MATCH (u:User {name: $user_name})-[:FRIENDS_WITH]-(friend)-[:FRIENDS_WITH]-(fof) "
                      "WHERE NOT (u)-[:FRIENDS_WITH]-(fof) AND u <> fof "
                      "RETURN fof.name AS name",
                      user_name=user_name)

    def search_users(self, **kwargs):
        with self.driver.session() as session:
            result = session.execute_read(self._search_users, kwargs)
            return [record["name"] for record in result]

    @staticmethod
    def _search_users(tx, search_params):
        where_clause = " AND ".join([f"u.{key} = ${key}" for key in search_params])
        return tx.run(f"MATCH (u:User) WHERE {where_clause} RETURN u.name AS name", **search_params)


def main():
    print('Running Social Network Application')
    app = SocialNetworkApp("Url", "neo4j", "password")

    # User registration
    app.register_user("Alice", 30, "New York", ["Music", "Sports"])
    app.register_user("Bob", 25, "San Francisco", ["Music", "Travel"])
    app.register_user("Charlie", 35, "New York", ["Sports", "Travel"])

    # Update user info
    app.update_user_info("Alice", age=31)

    # Friend management
    app.send_friend_request("Alice", "Bob")
    app.accept_friend_request("Alice", "Bob")

    app.send_friend_request("Charlie", "Bob")
    app.accept_friend_request("Alice", "Bob")

    # Unfriend (uncomment to use)
    # app.unfriend("Alice", "Bob")

    # User interaction
    app.create_post("Alice", "Hello World!")
    app.like_post("Bob", 1)
    app.comment_on_post("Bob", 1, "Nice post!")

    # Recommendations and search
    friends = app.recommend_friends("Alice")
    users = app.search_users(location="New York")

    print("Friend Recommendations for Alice:", friends)
    print("Users in New York:", users)


if __name__ == "__main__":
    main()
