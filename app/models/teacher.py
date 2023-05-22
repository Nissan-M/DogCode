import sys
import os
from app.database import execute_query
from app.models import User


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)


class Teacher():
    def __init__(self, teacher_id: int, user_id: int, name: str, image: str,
                 gender: str, birth_date: str, phone: str, address: str,
                 email: str, password: str):
        self.teacher_id = teacher_id
        self.user_id = user_id
        self.name = name
        self.image = image
        self.gender = gender
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
        self.email = email
        self.password = password

    def create(email: str, password: str,  name: str, image: str = 'Null',
               gender: str = 'Null', birth_date: str = 'Null',
               phone: str = 'Null', address: str = 'Null'):
        role = 'Teacher'
        User.create(role=role, email=email, password=password)

        user_id = User.read_by(email=email).user_id
        query = """
            INSERT INTO teachers
            (user_id, name, image, gender, birth_date, phone, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = [user_id, name, image, gender, birth_date, phone, address]

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating teacher: {str(e)}")

    def read():
        query = """
            SELECT teach.teacher_id, teach.user_id, teach.name, teach.image,
                   teach.gender, teach.birth_date, teach.phone, teach.address,
                   users.email, users.password
            FROM teachers AS teach
            JOIN users ON teach.user_id = users.user_id
        """

        try:
            data_rows = execute_query(query)
            teacher_objects = [Teacher(*data_row) for data_row in data_rows]
            return teacher_objects
        except Exception as e:
            print(f"Error occurred while retrieving teachers: {str(e)}")
            return None

    def read_by(teacher_id: int = None, user_id: int = None):
        query = """
            SELECT teach.teacher_id, teach.user_id, teach.name, teach.image,
                   teach.gender, teach.birth_date, teach.phone, teach.address,
                   users.email, users.password
            FROM teachers AS teach
            JOIN users ON teach.user_id = users.user_id
            WHERE
        """

        if teacher_id:
            query += " teach.teacher_id = ?"
            params = [teacher_id]

        if user_id:
            query += " teach.user_id = ?"
            params = [user_id]

        try:
            data_row = execute_query(query, tuple(params))[0]
            teacher_object = Teacher(*data_row)
            return teacher_object
        except Exception as e:
            print(f"Error occurred while retrieving teacher: {str(e)}")
            return None

    def update(teacher_id: int, name: str = None, image: str = None,
               gender: str = None, birth_date: str = None, phone: str = None,
               address: str = None, email: str = None, password: str = None):
        user_id = Teacher.read_by_id(teacher_id).user_id

        if email:
            User.update(user_id=user_id, email=email)

        if password:
            User.update(user_id=user_id, password=password)

        query = "UPDATE teachers SET"
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

        query = (query.rstrip(',') + " WHERE teacher_id = ?")
        params.append(teacher_id)

        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while update teacher: {str(e)}")

    def delete(teacher_id: int):
        query = "DELETE FROM teachers WHERE teacher_id = ?"
        params = [teacher_id]

        try:
            User.delete(Teacher.read_by_id(teacher_id).user_id)
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting teacher: {str(e)}")
