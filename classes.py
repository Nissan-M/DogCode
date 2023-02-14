from setup_db import execute_query, executemany_query


class Course:
    def __init__(self, id=0) -> None:
        self.id = self.get_data(id, column="course_id")
        self.name = self.get_data(id, column="name")
        self.desc = self.get_data(id, column="desc")
        self.list = self.get_all()

    def get_data(self, id, column):
        try:
            data = execute_query(
                f"SELECT {column} FROM course WHERE course_id={id}")
            return data[0][0]
        except:
            pass

    def get_all(slef):
        return execute_query("SELECT * FROM course")

class User:
    def __init__(self) -> None:
        self.id = ""
        self.user_id = ""
        self.name = ""
        self.image = ""
        self.gender = ""
        self.birth_date = ""
        self.phone = ""
        self.address = ""
        self.email = ""
        self.password = ""

    def get_data(self, id):
        data = execute_query(f"""
            SELECT * 
            FROM user
        """)
        return

class Student(User):
    def __init__(self) -> None:
        self.courses = {"python": [90,100,50], "PHP": [40,60,100]}

class Teacher:
    def __init__(self) -> None:



class Class:
    def __init__(self) -> None:
        pass

