import sys
import os
from app.database import execute_query
from app.crud.crud_user import User

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class Student():
    def __init__(self, student_id: int, user_id: int, name: str, image: str,
                 gender: str, birth_date: str, phone: str, address: str,
                 email: str, password: str):
        self.student_id = student_id
        self.user_id = user_id
        self.name = name
        self.image = image
        self.gender = gender
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
        self.email = email
        self.password = password

    def create(email: str, password: str,  name: str,
               image: str = 'Null', gender: str = 'Null',
               birth_date: str = 'Null', phone: str = 'Null',
               address: str = 'Null'):
        role = 'Student'
        User.create(role=role, email=email, password=password)

        user_id = User.read_by(email=email).user_id
        query = """
            INSERT INTO students
            (user_id, name, image, gender, birth_date, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = [user_id, name, image, gender, birth_date, phone, address]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating student: {str(e)}")

    def read():
        query = """
            SELECT stud.student_id, stud.user_id, stud.name, stud.image,
                   stud.gender, stud.birth_date, stud.phone, stud.address,
                   users.email, users.password
            FROM students AS stud
            JOIN users ON stud.user_id = users.user_id
        """

        try:
            data_rows = execute_query(query)
            student_objects = [Student(*data_row) for data_row in data_rows]
            return student_objects
        except Exception as e:
            print(f"Error occurred while retrieving students: {str(e)}")
            return None

    def read_by_id(student_id: int = None):
        query = """
            SELECT stud.student_id, stud.user_id, stud.name, stud.image,
                   stud.gender, stud.birth_date, stud.phone, stud.address,
                   users.email, users.password
            FROM students AS stud
            JOIN users ON stud.user_id = users.user_id
            WHERE student_id = ?
        """
        params = [student_id]

        try:
            data_row = execute_query(query, tuple(params))[0]
            student_object = Student(*data_row)
            return student_object
        except Exception as e:
            print(f"Error occurred while retrieving student: {str(e)}")
            return None

    def update(student_id: int, name: str = None, image: str = None,
               gender: str = None, birth_date: str = None, phone: str = None,
               address: str = None, email: str = None, password: str = None):
        user_id = Student.read_by_id(student_id).user_id
        if email:
            User.update(user_id=user_id, email=email)
        if password:
            User.update(user_id=user_id, password=password)

        query = "UPDATE students SET"
        params = []

        if name:
            query += " name = ?,"
            params.append(name)

        if image:
            query += " image = ?,"
            params.append(image)

        if gender:
            query += " gender = ?,"
            params.append(gender)

        if birth_date:
            query += " birth_date = ?,"
            params.append(birth_date)

        if phone:
            query += " phone = ?,"
            params.append(phone)

        if address:
            query += " address = ?,"
            params.append(address)

        query = (query.rstrip(',') + " WHERE student_id = ?")
        params.append(student_id)
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while update student: {str(e)}")

    def delete(student_id: int):
        query = "DELETE FROM students WHERE student_id = ?"
        params = [student_id]

        try:
            User.delete(Student.read_by_id(student_id).user_id)
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting student: {str(e)}")
