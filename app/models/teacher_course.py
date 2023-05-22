import sys
import os
from app.database import execute_query


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class TeacherCourse():
    def __init__(self, teacher_course_id: int, course_id: int,
                 course_name: str, teacher_id: int, teacher_name: str,
                 start_date: str, end_date: str):
        self.teacher_course_id = teacher_course_id
        self.course_id = course_id
        self.course_name = course_name
        self.teacher_id = teacher_id
        self.teacher_name = teacher_name
        self.start_date = start_date
        self.end_date = end_date

    def create(course_id: int, teacher_id: int, start_date: str,
               end_date: str):
        query = """
            INSERT INTO teachers_courses
            (course_id, teacher_id, start_date, end_date)
            VALUES (?, ?, ?, ?)
        """
        params = [course_id, teacher_id, start_date, end_date]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating teacher course: {str(e)}")

    def read():
        query = """
            SELECT tc.teacher_course_id,
                   tc.course_id,
                   courses.name,
                   tc.teacher_id,
                   teach.name,
                   tc.start_date,
                   tc.end_date
            FROM teachers_courses AS tc
            JOIN courses ON tc.course_id = courses.course_id
            JOIN teachers AS teach ON tc.teacher_id = teach.teacher_id
        """

        try:
            data_rows = execute_query(query)
            tc_objects = [TeacherCourse(*data_row) for data_row in data_rows]
            return tc_objects
        except Exception as e:
            print(f"Error occurred while retrieving teacher courses: {str(e)}")
            return None

    def read_by(teacher_course_id: int = None, course_id: int = None,
                teacher_id: int = None):
        query = """
            SELECT tc.teacher_course_id,
                   tc.course_id,
                   courses.name,
                   tc.teacher_id,
                   teach.name,
                   tc.start_date,
                   tc.end_date
            FROM teachers_courses AS tc
            JOIN courses ON tc.course_id = courses.course_id
            JOIN teachers AS teach ON tc.teacher_id = teach.teacher_id
        """

        if teacher_course_id:
            query += " WHERE teacher_course_id = ?"
            params = [teacher_course_id]

        if course_id:
            query += " WHERE course_id = ?"
            params = [course_id]

        if teacher_id:
            query += " WHERE teacher_id = ?"
            params = [teacher_id]

        try:
            data_row = execute_query(query, tuple(params))[0]
            tc_object = TeacherCourse(*data_row)
            return tc_object
        except Exception as e:
            print(f"Error occurred while retrieving teacher course: {str(e)}")
            return None

    def update(teacher_course_id: int, start_date: str = None,
               end_date: str = None):
        query = "UPDATE teachers_courses SET"
        params = []

        if start_date:
            query += " start_date = ?,"
            params.append(start_date)

        if end_date:
            query += " end_date = ?,"
            params.append(end_date)

        query = query.rstrip(',') + " WHERE teacher_course_id = ?"
        params.append(teacher_course_id)

        try:
            execute_query(query, params)
        except Exception as e:
            print(f"Error occurred while updating teacher course: {str(e)}")

    def delete(teacher_course_id: int):
        query = "DELETE FROM teachers_courses WHERE teacher_course_id = ?"
        params = [teacher_course_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting teacher course: {str(e)}")
