import sys
import os
from app.database import execute_query


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class User:
    def __init__(self, user_id: int, role: str, email: str, password: str):
        self.user_id = user_id
        self.role = role
        self.email = email
        self.password = password

    def create(role: str, email: str, password: str):
        query = "INSERT INTO users (role, email, password) VALUES (?, ?, ?)"
        params = [role, email, password]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating user: {str(e)}")

    def read():
        query = "SELECT user_id, role, email, password FROM users"

        try:
            data_rows = execute_query(query)
            user_objects = [User(*data_row) for data_row in data_rows]
            return user_objects
        except Exception as e:
            print(f"Error occurred while retrieving users: {str(e)}")
            return None

    def read_by(user_id: int = None, email: str = None):
        query = "SELECT user_id, role, email, password FROM users"
        params = []

        if user_id:
            query += " WHERE user_id = ?"
            params.append(user_id)

        elif email:
            query += " WHERE email = ?"
            params.append(email)

        try:
            data_row = execute_query(query, tuple(params))[0]
            user_object = User(*data_row)
            return user_object
        except Exception as e:
            print(f"Error occurred while retrieving user: {str(e)}")
            return None

    def update(user_id: int, role: str = None, email: str = None,
               password: str = None):
        query = "UPDATE users SET"
        params = []

        if role:
            query += " role = ?,"
            params.append(role)

        if email:
            query += " email = ?,"
            params.append(email)

        if password:
            query += " password = ?,"
            params.append(password)

        query = query.rstrip(',') + " WHERE user_id = ?"
        params.append(user_id)

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while updating user: {str(e)}")

    def delete(user_id: int):
        query = "DELETE FROM users WHERE user_id = ?"
        params = [user_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting user: {str(e)}")

    def auth(email: str, password: str):
        query = """
            SELECT user_id, role
            FROM users
            WHERE email = ? AND password = ?
        """
        params = [email, password]

        try:
            data_row = execute_query(query, tuple(params))

            if data_row:
                user_id, role = data_row[0]
                return {'user_id': user_id, 'role': role}

        except Exception as e:
            print(f"Error occurred while authenticating user: {str(e)}")
            return None
