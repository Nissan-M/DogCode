import sys
import os
from app.database import execute_query


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)


class User:
    def __init__(self, user_id: int, role: str, email: str, password: str):
        self.user_id = user_id
        self.role = role
        self.email = email
        self.password = password

    def create(role: str, email: str, password: str):
        query = """
            INSERT INTO user
            (role, email, password)
            VALUES (?, ?, ?)
        """
        params = [role, email, password]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating user: {str(e)}")

    def read():
        query = "SELECT * FROM user"
        try:
            users_db = execute_query(query)
            users = [User(*user_data) for user_data in users_db]
            return users
        except Exception as e:
            print(f"Error occurred while retrieving users: {str(e)}")

    def update(user_id: int, role: str = None, email: str = None,
               password: str = None):
        query = "UPDATE user SET"
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
            execute_query(query, params)
        except Exception as e:
            print(f"Error occurred while updating user: {str(e)}")

    def delete(user_id: int):
        query = "DELETE FROM user WHERE user_id = ?"
        params = [user_id]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting user: {str(e)}")

    def auth(email: str, psw: str):
        query = """
            SELECT role, email
            FROM user
            WHERE email = ? AND password = ?
        """
        params = [email, psw]
        try:
            result = execute_query(query, tuple(params))
            if result:
                return result[0]
        except Exception as e:
            print(f"Error occurred while authenticating user: {str(e)}")

        return None


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

    def create(user_id: int, name: str, image: str = 'Null',
               gender: str = 'Null', birth_date: str = 'Null',
               phone: str = 'Null', address: str = 'Null'):
        query = """
            INSERT INTO student (
                user_id, name, image, gender, birth_date, phone, address
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
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
                   user.email, user.password
            FROM student AS stud
            JOIN user ON stud.user_id = user.user_id
        """
        try:
            students_db = execute_query(query)
            students = [Student(*student_data) for student_data in students_db]
            return students
        except Exception as e:
            print(f"Error occurred while retrieving students: {str(e)}")

    def read_by_id(student_id):
        query = """
            SELECT stud.student_id, stud.user_id, stud.name, stud.image,
                   stud.gender, stud.birth_date, stud.phone, stud.address,
                   user.email, user.password
            FROM student AS stud
            JOIN user ON stud.user_id = user.user_id
            WHERE student_id = ?
        """
        params = [student_id]
        try:
            students_db = execute_query(query, tuple(params))[0]
            student = Student(*students_db)
            return student
        except Exception as e:
            print(f"Error occurred while retrieving student: {str(e)}")

    def update(user_id, name=None, image=None, gender=None, birth_date=None,
               phone=None, address=None, email=None, password=None):
        update_user_query = "UPDATE user SET"
        user_params = []
        if email:
            update_user_query += " email = ?,"
            user_params.append(email)
        if password:
            update_user_query += " password = ?,"
            user_params.append(password)
        update_user_query = (
            update_user_query.rstrip(',')
            + " WHERE user_id = ?"
        )
        user_params.append(user_id)
        try:
            execute_query(update_user_query, tuple(user_params))
        except Exception as e:
            print(f"Error occurred while update student: {str(e)}")

        update_student_query = "UPDATE student SET"
        student_params = []
        if name:
            update_student_query += " name = ?,"
            student_params.append(name)
        if image:
            update_student_query += " image = ?,"
            student_params.append(image)
        if gender:
            update_student_query += " gender = ?,"
            student_params.append(gender)
        if birth_date:
            update_student_query += " birth_date = ?,"
            student_params.append(birth_date)
        if phone:
            update_student_query += " phone = ?,"
            student_params.append(phone)
        if address:
            update_student_query += " address = ?,"
            student_params.append(address)
        update_student_query = (
            update_student_query.rstrip(',')
            + " WHERE user_id = ?"
        )
        student_params.append(user_id)
        try:
            execute_query(update_student_query, tuple(student_params))
        except Exception as e:
            print(f"Error occurred while update student: {str(e)}")

    def delete(student_id):
        query = "DELETE FROM student WHERE student_id = ?"
        params = [student_id]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting student: {str(e)}")


class Teacher():
    def __init__(self, teacher_id, user_id, name, image, gender, birth_date,
                 phone, address, email, password):
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

    def create(user_id, name='Default', image='Default', gender='Default',
               birth_date='Default', phone='Default', address='Default'):
        create_query = """
            INSERT INTO teacher (
                user_id,
                name,
                image,
                gender,
                birth_date,
                phone,
                address
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        params = [user_id, name, image, gender, birth_date, phone, address]
        try:
            execute_query(create_query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating student: {str(e)}")

    def read():
        query = """
            SELECT teach.teacher_id, teach.user_id, teach.name, teach.image,
                   teach.gender, teach.birth_date, teach.phone, teach.address,
                   user.email, user.password
            FROM teacher AS teach
            JOIN user ON teach.user_id = user.user_id
        """
        try:
            teachers_db = execute_query(query)
            teachers = [Teacher(*teacher_data) for teacher_data in teachers_db]
            return teachers
        except Exception as e:
            print(f"Error occurred while retrieving teachers: {str(e)}")

    def read_by_id(teacher_id):
        query = """
            SELECT teach.teacher_id, teach.user_id, teach.name, teach.image,
                   teach.gender, teach.birth_date, teach.phone, teach.address,
                   user.email, user.password
            FROM teacher AS teach
            JOIN user ON teach.user_id = user.user_id
            WHERE teacher_id = ?
        """
        params = [teacher_id]
        try:
            teacher_db = execute_query(query, tuple(params))[0]
            teacher = Student(*teacher_db)
            return teacher
        except Exception as e:
            print(f"Error occurred while retrieving teacher: {str(e)}")

    def update(user_id, name=None, image=None, gender=None, birth_date=None,
               phone=None, address=None, email=None, password=None):
        update_user_query = "UPDATE user SET"
        user_params = []
        if email:
            update_user_query += " email = ?,"
            user_params.append(email)
        if password:
            update_user_query += " password = ?,"
            user_params.append(password)
        update_user_query = (
            update_user_query.rstrip(',')
            + " WHERE user_id = ?"
        )
        user_params.append(user_id)
        try:
            execute_query(update_user_query, tuple(user_params))
        except Exception as e:
            print(f"Error occurred while update Teacher: {str(e)}")

        update_teacher_query = "UPDATE teacher SET"
        teacher_params = []
        if name:
            update_teacher_query += " name = ?,"
            teacher_params.append(name)
        if image:
            update_teacher_query += " image = ?,"
            teacher_params.append(image)
        if gender:
            update_teacher_query += " gender = ?,"
            teacher_params.append(gender)
        if birth_date:
            update_teacher_query += " birth_date = ?,"
            teacher_params.append(birth_date)
        if phone:
            update_teacher_query += " phone = ?,"
            teacher_params.append(phone)
        if address:
            update_teacher_query += " address = ?,"
            teacher_params.append(address)
        update_teacher_query = (
            update_teacher_query.rstrip(',')
            + " WHERE user_id = ?"
        )
        teacher_params.append(user_id)
        try:
            execute_query(update_teacher_query, tuple(teacher_params))
        except Exception as e:
            print(f"Error occurred while update Teacher: {str(e)}")

    def delete(teacher_id):
        query = "DELETE FROM teacher WHERE teacher_id = ?"
        params = [teacher_id]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting teacher: {str(e)}")


class Course():
    def __init__(self, course_id, name, image, desc) -> None:
        self.course_id = course_id
        self.name = name
        self.image = image
        self.desc = desc

    def create(name, image, desc):
        query = """
            INSERT INTO course
            (name, image, desc)
            VALUES (?, ?, ?)
        """
        params = [name, image, desc]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating course: {str(e)}")

    def read():
        query = "SELECT * FROM course"
        try:
            courses_db = execute_query(query)
            courses = [Course(*course_data) for course_data in courses_db]
            return courses
        except Exception as e:
            print(f"Error occurred while retrieving courses: {str(e)}")

    def read_by_id(course_id):
        query = "SELECT * FROM course WHERE course_id = ?"
        params = [course_id]
        try:
            course_data = execute_query(query, tuple(params))[0]
            course = Student(*course_data)
            return course
        except Exception as e:
            print(f"Error occurred while retrieving course: {str(e)}")

    def update(course_id, name=None, image=None, desc=None):
        query = "UPDATE course SET"
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

    def delete(course_id):
        query = "DELETE FROM course WHERE course_id = ?"
        params = [course_id]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting course: {str(e)}")


class ActiveCourse():
    def __init__(self, activeCourse_id: int, course_id: int, teacher_id: int,
                 name: str, start_date: str, end_date: str):
        self.activeCourse_id = activeCourse_id
        self.course_id = course_id
        self.teacher_id = teacher_id
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def create(course_id: int, teacher_id: int, name: str, start_date: str,
               end_date: str):
        query = """
            INSERT INTO active_course
            (course_id, teacher_id, name, start_date, end_date)
            VALUES (?, ?, ?, ?, ?)
        """
        params = [course_id, teacher_id, name, start_date, end_date]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating activeCourse: {str(e)}")

    def read():
        query = "SELECT * FROM active_course"
        try:
            data_base = execute_query(query)
            activeCourses = [Student(*data) for data in data_base]
            return activeCourses
        except Exception as e:
            print(f"Error occurred while retrieving activeCourses: {str(e)}")

    def read_by_id(activeCourse_id: int):
        query = "SELECT * FROM active_course WHERE ac_id = ?"
        params = [activeCourse_id]
        try:
            data = execute_query(query, tuple(params))[0]
            activeCourse = Student(*data)
            return activeCourse
        except Exception as e:
            print(f"Error occurred while retrieving activeCourse: {str(e)}")

    def update(activeCourse_id: int, course_id: int = None,
               teacher_id: int = None, name: str = None,
               start_date: str = None, end_date: str = None):
        query = "UPDATE active_course SET"
        params = []
        if course_id:
            query += " course_id = ?,"
            params.append(course_id)
        if teacher_id:
            query += " teacher_id = ?,"
            params.append(teacher_id)
        if name:
            query += " name = ?,"
            params.append(name)
        if start_date:
            query += " start_date = ?,"
            params.append(start_date)
        if end_date:
            query += " end_date = ?,"
            params.append(end_date)
        query = query.rstrip(',') + " WHERE ac_id = ?"
        params.append(activeCourse_id)
        try:
            execute_query(query, params)
        except Exception as e:
            print(f"Error occurred while updating activeCourse: {str(e)}")

    def delete(activeCourse_id: int):
        query = "DELETE FROM active_course WHERE ac_id = ?"
        params = [activeCourse_id]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting activeCourse: {str(e)}")


class Class():
    def __init__(self, class_id: int, activeCourse_id: int, student_id: int,
                 grades: list):
        self.class_id = class_id
        self.activeCourse_id = activeCourse_id
        self.student_id = student_id
        self.grades = grades

    def create(activeCourse_id: int, student_id: int, grades: list = 'NULL'):
        query = """
            INSERT INTO class
            (ac_id, student_id, grades)
            VALUES (?, ?, ?)
        """
        params = [activeCourse_id, student_id, grades]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while creating activeCourse: {str(e)}")

    def read():
        query = "SELECT * FROM active_course"
        try:
            data_base = execute_query(query)
            activeCourses = [Student(*data) for data in data_base]
            return activeCourses
        except Exception as e:
            print(f"Error occurred while retrieving activeCourses: {str(e)}")

    def read_by_id(activeCourse_id: int):
        query = "SELECT * FROM active_course WHERE ac_id = ?"
        params = [activeCourse_id]
        try:
            data = execute_query(query, tuple(params))[0]
            activeCourse = Student(*data)
            return activeCourse
        except Exception as e:
            print(f"Error occurred while retrieving activeCourse: {str(e)}")

    def update(activeCourse_id: int, course_id: int = None,
               teacher_id: int = None, name: str = None,
               start_date: str = None, end_date: str = None):
        query = "UPDATE active_course SET"
        params = []
        if course_id:
            query += " course_id = ?,"
            params.append(course_id)
        if teacher_id:
            query += " teacher_id = ?,"
            params.append(teacher_id)
        if name:
            query += " name = ?,"
            params.append(name)
        if start_date:
            query += " start_date = ?,"
            params.append(start_date)
        if end_date:
            query += " end_date = ?,"
            params.append(end_date)
        query = query.rstrip(',') + " WHERE ac_id = ?"
        params.append(activeCourse_id)
        try:
            execute_query(query, params)
        except Exception as e:
            print(f"Error occurred while updating activeCourse: {str(e)}")

    def delete(activeCourse_id: int):
        query = "DELETE FROM active_course WHERE ac_id = ?"
        params = [activeCourse_id]
        try:
            execute_query(query, tuple(params))
        except Exception as e:
            print(f"Error occurred while deleting activeCourse: {str(e)}")
