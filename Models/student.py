from setup_db import execute_query


class Student():
    def __init__(self, student_id) -> None:
        self.student_id = self.get_student(student_id)[0]
        self.user_id = self.get_student(student_id)[1]
        self.name = self.get_student(student_id)[2]
        self.image = self.get_student(student_id)[3]
        self.gender = self.get_student(student_id)[4]
        self.birth_date = self.get_student(student_id)[5]
        self.phone = self.get_student(student_id)[6]
        self.address = self.get_student(student_id)[7]
        self.email = self.get_student(student_id)[8]
        self.pasword = self.get_student(student_id)[9]
        self.courses = self.get_courses(student_id)

    def get_student(self, student_id):
        query = f"""
            SELECT
                student.student_id,
                student.user_id,
                student.name,
                student.image,
                student.gender,
                student.birth_date,
                student.phone,
                student.address,
                user.email,
                user.password
            FROM student
            JOIN user ON student.user_id = user.user_id
            WHERE student_id = {student_id}
            """
        return execute_query(query)[0]

    def get_courses(self, student_id):
        query = f"""
            SELECT course.name FROM ac_stud
            JOIN ac ON ac_stud.ac_id = ac.ac_id
            JOIN course ON ac.course_id = course.course_id
            WHERE student_id = {student_id}
            """
        courses = execute_query(query)
        return [course[0] for course in courses]

    def get_all_ids():
        query = "SELECT student_id FROM student"
        student_ids = execute_query(query)
        return [student_id[0] for student_id in student_ids]

    def update_profile(student_id, name=None, image=None, gender=None,
                       birth_date=None, phone=None, address=None, email=None,
                       password=None):
        if email or password:
            query = f"""
                SELECT user_id FROM student
                WHERE student_id = {student_id}
            """
            user_id = execute_query(query)[0][0]
            query = "UPDATE user SET"
            if email:
                query += f"\nemail = '{email}',"
            if password:
                query += f"\npassword = '{password}',"
            query = query.rstrip(',') + f"\nWHERE user_id = {user_id}"
            execute_query(query)

        query = "UPDATE student SET"
        if name:
            query += f"\nname = '{name}',"
        if image:
            query += f"\nimage = '{image}',"
        if gender:
            query += f"\ngender = '{gender}',"
        if birth_date:
            query += f"\nbirth_date = '{birth_date}',"
        if phone:
            query += f"\nphone = '{phone}',"
        if address:
            query += f"\naddress = '{address}',"
        query = query.rstrip(',') + f"\nWHERE student_id = {student_id}"
        execute_query(query)
