import sys
import os
from app.database import execute_query


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class Attendance():
    def __init__(self, attendance_id: int, student_course_id: int, date: str,
                 presence: str):
        self.attendance_id = attendance_id
        self.student_course_id = student_course_id
        self.date = date
        self.presence = presence

    def create(student_course_id: str, date: str, presence: str):
        query = """
            INSERT INTO attendance
            (student_course_id, date, presence)
            VALUES (?, ?, ?)
        """
        params = [student_course_id, date, presence]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating attendance: {str(e)}")

    def read():
        query = """
            SELECT attendance_id, student_course_id, date, presence
            FROM attendance
        """

        try:
            data_rows = execute_query(query)
            attendance_objects = [Attendance(*data_row) for data_row in data_rows]
            return attendance_objects
        except Exception as e:
            print(f"Error occurred while retrieving attendance: {str(e)}")
            return None

    def read_by(attendance_id: int = None, student_course_id: str = None,
                date: str = None):
        query = """
            SELECT attendance_id, student_course_id, date, presence
            FROM attendance
        """

        if attendance_id:
            query += " WHERE attendance_id = ?"
            params = [attendance_id]

        if student_course_id and date:
            query += " WHERE student_course_id = ? AND date = ?"
            params = [student_course_id, date]

        try:
            data_row = execute_query(query, tuple(params))[0]
            attendance_object = Attendance(*data_row)
            return attendance_object
        except Exception as e:
            print(f"Error occurred while retrieving attendance: {str(e)}")
            return None

    def update(attendance_id: int, presence: str = None):
        query = "UPDATE attendances SET presence = ? WHERE attendance_id = ?"
        params = [presence, attendance_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while updating attendance: {str(e)}")

    def delete(attendance_id: int):
        query = "DELETE FROM user WHERE attendance_id = ?"
        params = [attendance_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting attendance: {str(e)}")
