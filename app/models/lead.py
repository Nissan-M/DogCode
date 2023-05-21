import sys
import os
from app.database import execute_query


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class Lead:
    def __init__(self, lead_id: int, course_id: int, name: str, phone: str,
                 email: str):
        self.lead_id = lead_id
        self.course_id = course_id
        self.name = name
        self.phone = phone
        self.email = email

    def create(course_id: str, name: str, phone: str, email: str):
        query = """
            INSERT INTO leads
            (course_id, name, phone, email)
            VALUES (?, ?, ?, ?)
        """
        params = [course_id, name, phone, email]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating lead: {str(e)}")

    def read():
        query = "SELECT lead_id, course_id, name, phone, email FROM leads"

        try:
            data_rows = execute_query(query)
            user_objects = [Lead(*data_row) for data_row in data_rows]
            return user_objects
        except Exception as e:
            print(f"Error occurred while retrieving leads: {str(e)}")
            return None

    def read_by(course_id: int = None):
        query = """
            SELECT lead_id, course_id, name, phone, email
            FROM leads
            WHERE course_id = ?
        """
        params = [course_id]

        try:
            data_rows = execute_query(query, tuple(params))
            lead_objects = [Lead(*data_row) for data_row in data_rows]
            return lead_objects
        except Exception as e:
            print(f"Error occurred while retrieving leads: {str(e)}")
            return None

    def delete(lead_id: int):
        query = "DELETE FROM leads WHERE lead_id = ?"
        params = [lead_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting lead: {str(e)}")
