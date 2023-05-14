from app.database import execute_query


class User:
    def __init__(self, _id, role, email, password) -> None:
        self._id = _id
        self.role = role
        self.email = email
        self.password = password

    def create(role, email, password):
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
        query = "SELECT user_id, role, email, password FROM user"
        try:
            users_db = execute_query(query)
            users = [User(*user_data) for user_data in users_db]
            return users
        except Exception as e:
            print(f"Error occurred while retrieving users: {str(e)}")

    def update(_id, role=None, email=None, password=None):
        update_query = "UPDATE user SET"
        params = []
        if role is not None:
            update_query += " role = ?,"
            params.append(role)
        if email is not None:
            update_query += " email = ?,"
            params.append(email)
        if password is not None:
            update_query += " password = ?,"
            params.append(password)
        update_query = update_query.rstrip(',') + " WHERE user_id = ?"
        params.append(_id)
        try:
            execute_query(update_query, params)
        except Exception as e:
            print(f"Error occurred while updating user: {str(e)}")

    def delete(_id):
        delete_query = "DELETE FROM user WHERE user_id = ?"
        try:
            execute_query(delete_query, (_id,))
        except Exception as e:
            print(f"Error occurred while deleting user: {str(e)}")

    def auth(email, psw):
        auth_query = """
            SELECT role, email
            FROM user
            WHERE email = ? AND password = ?
        """
        try:
            result = execute_query(auth_query, (email, psw))
            if result:
                return result[0]
        except Exception as e:
            print(f"Error occurred while authenticating user: {str(e)}")

        return None


class Student():
    def __init__(self, student_id, user_id, name, image, gender, birth_date,
                 phone, address, email, password, courses=None):
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
        self.courses = courses

    def create(user_id, name='Default', image='Default', gender='Default',
               birth_date='Default', phone='Default', address='Default'):
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

    def delete():
        pass


class Teacher():
    def __init__(self, _id, user_id, name, image, gender, birth_date, phone,
                 address, email, password, courses):
        self._id = _id
        self.user_id = user_id
        self.name = name
        self.image = image
        self.gender = gender
        self.birth_date = birth_date
        self.phone = phone
        self.address = address
        self.email = email
        self.password = password
        self.courses = courses

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
            teachers = [Student(*teacher_data) for teacher_data in teachers_db]
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

    def delete():
        pass


class Course():
    def __init__(self, _id, name, image, desc) -> None:
        self._id = _id
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
        pass

    def update():
        pass

    def delete():
        pass


class Class():
    def __init__(self) -> None:
        pass


class register():
    def __init__(self) -> None:
        pass
