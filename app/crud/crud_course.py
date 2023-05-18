import sys
import os
from app.database import execute_query


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class Course():
    def __init__(self, course_id: int, name: str, image: str, desc: str):
        self.course_id = course_id
        self.name = name
        self.image = image
        self.desc = desc

    def create(name: str, image: str, desc: str):
        query = "INSERT INTO courses (name, image, desc) VALUES (?, ?, ?)"
        params = [name, image, desc]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating course: {str(e)}")

    def read():
        query = "SELECT course_id, name, image, desc FROM courses"

        try:
            data_rows = execute_query(query)
            course_objects = [Course(*data_row) for data_row in data_rows]
            return course_objects
        except Exception as e:
            print(f"Error occurred while retrieving courses: {str(e)}")
            return None

    def read_by_id(course_id: int):
        query = """
            SELECT course_id, name, image, desc
            FROM courses WHERE course_id = ?
        """
        params = [course_id]

        try:
            data_row = execute_query(query, tuple(params))[0]
            course_object = Course(*data_row)
            return course_object
        except Exception as e:
            print(f"Error occurred while retrieving course: {str(e)}")
            return None

    def update(course_id: int, name: str = None, image: str = None,
               desc: str = None):
        query = "UPDATE courses SET"
        params = []

        if name:
            query += " name = ?,"
            params.append(name)

        if image:
            query += " image = ?,"
            params.append(image)

        if desc:
            query += " desc = ?,"
            params.append(desc)

        query = query.rstrip(',') + " WHERE course_id = ?"
        params.append(course_id)

        try:
            execute_query(query, params)
        except Exception as e:
            print(f"Error occurred while updating course: {str(e)}")

    def delete(course_id: int):
        query = "DELETE FROM courses WHERE course_id = ?"
        params = [course_id]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting course: {str(e)}")
