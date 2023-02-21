from setup_db import execute_query


class User:
    def __init__(self, user_id) -> None:
        self.user_id = user_id
        self.email = self.get_data(user_id)[2]
        self.password = self.get_data(user_id)[3]
        self.role = self.get_data(user_id)[1]
        self.role_list = ["Student", "Teacher"]

    def get_data(self, user_id):
        schema = f"""
            SELECT * FROM user
            WHERE user_id = {user_id}
            """

        return execute_query(schema)[0]

    def get_all_ids():
        schema = """
            SELECT user_id FROM user
            """
        data = execute_query(schema)

        return [str(user_id[0]) for user_id in data]

    def new_user(email, password, role):
        schema = f"""
            INSERT INTO user (
                email
              , password
              , role
            ) VALUES (
                '{email}'
              , '{password}'
              , '{role}'
            )
            """
        execute_query(schema)

    def update_user(self, email=None, password=None, role=None):
        query = "UPDATE user SET"
        if email:
            query += f" email = '{email}'"

        if password:
            query += f", password = '{password}'"

        if role:
            query += f", role = '{role}'"

        query += f" WHERE user_id = {self.user_id}"
        execute_query(query)
