from setup_db import execute_query


class Teacher():
    def __init__(self, teacher_id) -> None:
        self.teacher_id = self.get_teacher(teacher_id)[0]
        self.user_id = self.get_teacher(teacher_id)[1]
        self.name = self.get_teacher(teacher_id)[2]
        self.image = self.get_teacher(teacher_id)[3]
        self.gender = self.get_teacher(teacher_id)[4]
        self.birth_date = self.get_teacher(teacher_id)[5]
        self.phone = self.get_teacher(teacher_id)[6]
        self.address = self.get_teacher(teacher_id)[7]
        self.email = self.get_teacher(teacher_id)[8]
        self.pasword = self.get_teacher(teacher_id)[9]
        self.courses = self.get_courses(teacher_id)

    def get_teacher(self, teacher_id):
        query = f"""
            SELECT
                teacher.student_id,
                teacher.user_id,
                teacher.name,
                teacher.image,
                teacher.gender,
                teacher.birth_date,
                teacher.phone,
                teacher.address,
                user.email,
                user.password
            FROM teacher
            JOIN user ON teacher.user_id = user.user_id
            WHERE teacher_id = {teacher_id}
            """
        return execute_query(query)[0]

    def get_courses(self, teacher_id):
        query = f"""
            SELECT course.name FROM ac
            JOIN course ON ac.course_id = course_course_id
            WHERE teacher_id = {teacher_id}
            """
        courses = execute_query(query)
        return [course[0] for course in courses]

    def get_all_ids():
        query = "SELECT teacher_id FROM teacher"
        teacher_ids = execute_query(query)
        return [teacher_id[0] for teacher_id in teacher_ids]

    def update_profile(teacher_id, name=None, image=None, gender=None,
                       birth_date=None, phone=None, address=None, email=None,
                       password=None):
        if email or password:
            query = f"""
                SELECT user_id FROM teacher
                WHERE teacher_id = {teacher_id}
            """
            user_id = execute_query(query)[0][0]
            query = "UPDATE user SET"
            if email:
                query += f"\nemail = '{email}',"
            if password:
                query += f"\npassword = '{password}',"
            query = query.rstrip(',') + f"\nWHERE user_id = {user_id}"
            execute_query(query)

        query = "UPDATE teacher SET"
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
        query = query.rstrip(',') + f"\nWHERE teacher_id = {teacher_id}"
