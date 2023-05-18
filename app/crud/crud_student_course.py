import sys
import os
import json
from app.database import execute_query


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class StudentCourse():
    def __init__(self, student_course_id: int, teacher_course_id: int,
                 student_id: int, grades: list):
        self.student_course_id = student_course_id
        self.teacher_course_id = teacher_course_id
        self.student_id = student_id
        self.grades = grades

    def create(teacher_course_id: int, student_id: int):
        query = """
            INSERT INTO students_courses
            (teacher_course_id, student_id)
            VALUES (?, ?)
        """
        params = [teacher_course_id, student_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error creating student course: {e}")

    def read():
        query = """
            SELECT student_course_id, teacher_course_id, student_id, grades
            FROM students_courses
        """

        try:
            data_rows = execute_query(query)
            sc_objects = [
                StudentCourse(
                    student_course_id=row[0],
                    teacher_course_id=row[1],
                    student_id=row[2],
                    grades=json.loads(row[3]) if row[3] else {})
                for row in data_rows
            ]
            return sc_objects
        except Exception as e:
            print(f"Error occurred while retrieving student course: {str(e)}")
            return None

    def read_by(student_course_id: int = None, teacher_course_id: int = None,
                student_id: int = None):
        query = """
            SELECT student_course_id, teacher_course_id, student_id, grades
            FROM students_courses
        """

        if student_course_id:
            query += "WHERE student_course_id = ?"
            params = [student_course_id]

        if teacher_course_id:
            query += "WHERE teacher_course_id = ?"
            params = [teacher_course_id]

        if student_id:
            query += "WHERE student_id = ?"
            params = [student_id]

        try:
            data_row = execute_query(query, tuple(params))[0]
            sc_object = StudentCourse(
                student_course_id=data_row[0],
                teacher_course_id=data_row[1],
                student_id=data_row[2],
                grades=json.loads(data_row[3]) if data_row[3] else {}
            )
            return sc_object
        except Exception as e:
            print(f"Error occurred while retrieving student course: {str(e)}")
            return None

    def update(student_course_id: int, project_name: str = None,
               grade: int = None):
        query = "UPDATE students_courses SET"
        params = []

        if project_name and grade:
            query += f" grades = JSON_SET(grades, '$.{project_name}', ?),"
            params.append(grade)

        query = query.rstrip(',') + " WHERE student_course_id = ?"
        params.append(student_course_id)

        try:
            execute_query(query, params)
        except Exception as e:
            print(f"Error occurred while updating student course: {str(e)}")

    def delete(student_course_id: int):
        query = "DELETE FROM students_courses WHERE student_course_id = ?"
        params = [student_course_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting class: {str(e)}")
