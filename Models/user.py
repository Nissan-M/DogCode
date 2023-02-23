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

    def create_user(email, password, role, name):
        schema = f"""
            INSERT INTO user (
                email,
                password,
                role
            ) VALUES (
                '{email}',
                '{password}',
                '{role}'
            )
            """
        execute_query(schema)

        schema = f"SELECT user_id FROM user WHERE email = '{email}'"
        user_id = execute_query(schema)[0][0]
        if role == "Student":
            table = "student"
        if role == "Teacher":
            table = "teacher"
        schema = f"""
            INSERT INTO {table} (
                user_id,
                name
            ) VALUES (
                {user_id},
                '{name}'
            )
            """
        execute_query(schema)

    def update_user(user_id, email=None, password=None, role=None):
        query = "UPDATE user SET"
        if email:
            query += f"\nemail = '{email}'"

        if password:
            query += f"\npassword = '{password}',"

        if role:
            query += f"\nrole = '{role}',"

        query = query.rstrip(',') + f"\nWHERE user_id = {user_id}"
        execute_query(query)

    def delete_user(user_id):
        query = f"SELECT role FROM user WHERE user_id = {user_id}"
        role = execute_query(query)[0][0]

        if role == "Student":
            table = "student"
        elif role == "Teacher":
            table = "teacher"

        query = f"""
            DELETE FROM {table}
            WHERE user_id = {user_id}
            """
        execute_query(query)

        query = f"""
            DELETE FROM user
            WHERE user_id = {user_id}
            """
        execute_query(query)
