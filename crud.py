from setup_db import execute_query


def convert_pic():
    files = ["./images/avatar_male.jpg", "./images/avatar_female.jpg"]
    picture = [open(file, "rb").read() for file in files]
    return picture


def show_all(table):
    return execute_query(f"SELECT * FROM {table}")


def show_all_by_id(table, id):
    return execute_query(f"SELECT * FORM {table} WHERE {table}_id={id}")


def new_user(email, password, role):
    execute_query(f"""
        INSERT INTO user (email, password, role_id)
        VLAUES ({email},{password}, {role})
        """)


def new_profile(table, user_id, name, gender, birth_date, phone, address):
    image_list = convert_pic()
    if gender == "Female":
        image = image_list[1]
    else:
        image = image_list[0]
    execute_query(f"""
        INSERT INTO {table} (
            user_id, name, image, gender,
            birth_date, phone, address
        ) VALUES (
            {user_id}, {name}, {image}, {gender},
            {birth_date}, {phone}, {address}
        )
        """)


def update_profile(table, name, image, gender, birth_date, phone, address, id):
    execute_query(f"""
        UPDATE {table} SET
            name={name}, image={image}, gender={gender},
            birth_date={birth_date}, phone={phone}, address={address}
        WHERE {table}_id={id}
        """)


def delete(table, id):
    execute_query(f"DELETE FROM {table} WHERE {table}_id={id}")


def new_course(name, desc):
    execute_query(f"""
        INSERT INTO course (
            name, desc
        ) VALUES (
            {name}, {desc}
        )
        """)


def update_course(id, name, desc):
    execute_query(f"""
        UPDATE course SET
            name={name}, desc={desc}
        WHERE course_id={id}
        """)


def add_active_course(course_id, teacher_id, start_date, end_date):
    execute_query(f"""
        INSERT INTO active_course (
            course_id, teacher_id, start_date, end_date
        ) VALUES (
            {course_id}, {teacher_id}, {start_date}, {end_date}
        )
        """)


def update_active_course(teacher_id, start_date, end_date, id):
    execute_query(f"""
        UPDATE active_course SET
            teacher_id={teacher_id}, start_date={start_date},
            end_date={end_date}
        WHERE active_course_id={id}
        """)


def add_active_course_student(active_course_id, student_id):
    execute_query(f"""
        INSERT INTO course_stud (
            active_course_id, student_id
        ) VALUE (
            {active_course_id}, {student_id}
        )
        """)


def update_active_course_student(active_course_id, grade, student_id):
    execute_query(f"""
        UPDATE course_stud SET
            active_course_id={active_course_id}, grade={grade}
        WHERE student_id={student_id}
        """)


def login(email, password):
    role = execute_query(f"""
        SELECT role_id FROM user
        WHERE email={email} and password={password}
        """)
    return role
