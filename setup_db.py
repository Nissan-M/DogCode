import sqlite3
from faker import Faker


def query(sql):
    with sqlite3.connect("database.db") as conn:
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()


def create_table():
    # role table
    query("""
    CREATE TABLE IF NOT EXISTS role (
        role_id INTEGER PRIMARY KEY AUTOINCREMENT,
        role_name TEXT NOT NULL UNIQUE
    )
    """)
    # user table
    query("""
    CREATE TABLE IF NOT EXISTS user (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_email TEXT NOT NULL UNIQUE,
        user_password TEXT NOT NULL,
        role_id INTEGER,
        FOREIGN KEY (role_id) REFERENCES role (role_id)
    )
    """)
    # student table
    query("""
    CREATE TABLE IF NOT EXISTS student (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        student_name TEXT NOT NULL,
        student_gender TEXT NOT NULL,
        student_bdate DATE NOT NULL,
        student_phone TEXT NOT NULL,
        student_address TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (user_id)
    )
    """)
    # teacher table
    query("""
    CREATE TABLE IF NOT EXISTS teacher (
        teacher_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE,
        teacher_name TEXT NOT NULL,
        teacher_gender TEXT NOT NULL,
        teacher_bdate DATE NOT NULL,
        teacher_phone TEXT NOT NULL,
        teacher_address TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (user_id)
    )
    """)
    # course table
    query("""
    CREATE TABLE IF NOT EXISTS course (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT NOT NULL UNIQUE,
        course_desc TEXT NOT NULL UNIQUE
    )
    """)
    # courseNo table
    query("""
    CREATE TABLE IF NOT EXISTS courseNo (
        courseNo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        courseNo_sdate DATE NOT NULL,
        courseNo_edate DATE NOT NULL,
        course_id INTEGER NOT NULL,
        teacher_id INTEGER NOT NULL,
        FOREIGN KEY (course_id) REFERENCES course (course_id),
        FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id)        
    )
    """)
    # courseNo - student table
    query("""
    CREATE TABLE IF NOT EXISTS courseNo_student (
        courseNo_student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        courseNo_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY (courseNo_id) REFERENCES courseNo (courseNo_id),
        FOREIGN KEY (student_id) REFERENCES student (student_id)
    )
    """)
    # course - student table
    query("""
    CREATE TABLE IF NOT EXISTS course_student (
        course_student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY (course_id) REFERENCES course (course_id),
        FOREIGN KEY (student_id) REFERENCES student (student_id)
    )
    """)


def generate_data():
    for role in ["student", "teacher", "admin"]:
        query(f"INSERT INTO role (role_name) VALUES ('{role}')")
    query("INSERT INTO user (user_email, user_password, role_id) VALUES ('admin@admin.com', 'admin', '3')")


def fake_data():
    fake = Faker()

    for user in range(10):
        query(f"INSERT INTO user ('user_email', 'user_password', 'role_id') VALUES ('{fake.email()}', '{fake.password()}', '2')")
    teachers = query("SELECT user_id FROM user WHERE role_id='2'")
    for teacher in teachers:
        query(f"""
        INSERT INTO teacher ('user_id', 'teacher_name', 'teacher_gender', 'teacher_bdate', 'teacher_phone', 'teacher_address')
        VALUES ('{teacher[0]}', '{fake.name()}', 'X', '0', '0', 'X')
        """)

    for user in range(30):
        query(f"INSERT INTO user ('user_email', 'user_password', 'role_id') VALUES ('{fake.email()}', '{fake.password()}', '3')")
    students = query("SELECT user_id FROM user WHERE role_id='3'")
    for student in students:
        query(f"""INSERT INTO student ('user_id', 'student_name', 'student_gender', 'student_bdate', 'student_phone', 'student_address')
        VALUES ('{student[0]}', '{fake.name()}', 'X', '0', '0', 'X')""")


if __name__ == "__main__":
    create_table()
    generate_data()
    fake_data()
