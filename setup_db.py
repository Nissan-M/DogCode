import sqlite3


DATABASE_NAME = "database.db"
conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)


def execute_query(schema, params=None):
    cursor = conn.cursor()
    if params:
        cursor.execute(schema, params)
    cursor.execute(schema)
    conn.commit()
    return cursor.fetchall()


def executemany_query(schema, value):
    cursor = conn.cursor()
    cursor.executemany(schema, value)
    return conn.commit()


def create_tables():
    create_user_table_query = """
        CREATE TABLE IF NOT EXISTS user (
            user_id     INTEGER     PRIMARY KEY
          , role        TEXT        NOT NULL
          , email       TEXT        NOT NULL        UNIQUE
          , password    TEXT        NOT NULL
        )
        """
    execute_query(create_user_table_query)

    create_student_table_query = """
        CREATE TABLE IF NOT EXISTS student (
            student_id  INTEGER     PRIMARY KEY
          , user_id     INTEGER     NOT NULL        UNIQUE
          , name        TEXT        NOT NULL
          , image       BLOB
          , gender      TEXT
          , birth_date  DATE
          , phone       TEXT
          , address     TEXT
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """
    execute_query(create_student_table_query)

    create_teacher_table_query = """
        CREATE TABLE IF NOT EXISTS teacher (
            teacher_id  INTEGER     PRIMARY KEY
          , user_id     INTEGER     NOT NULL        UNIQUE
          , name        TEXT        NOT NULL
          , image       BLOB
          , gender      TEXT
          , birth_date  DATE
          , phone       TEXT
          , address     TEXT
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """
    execute_query(create_teacher_table_query)

    create_course_table_query = """
        CREATE TABLE IF NOT EXISTS course (
            course_id   INTEGER     PRIMARY KEY
          , name        TEXT        NOT NULL        UNIQUE
          , desc        TEXT        NOT NULL
        )
        """
    execute_query(create_course_table_query)

    create_active_course_table_query = """
        CREATE TABLE IF NOT EXISTS active_course (
            ac_id       INTEGER     PRIMARY KEY
          , course_id   INTEGER     NOT NULL
          , teacher_id  INTEGER     NOT NULL
          , start_date  DATE        NOT NULL
          , end_date    DATE        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id)
        )
        """
    execute_query(create_active_course_table_query)

    create_course_stud_table_query = """
        CREATE TABLE IF NOT EXISTS class (
            class_id  INTEGER     PRIMARY KEY
          , ac_id       INTEGER     NOT NULL
          , student_id  INTEGER     NOT NULL
          , grade       INTEGER
          , FOREIGN KEY (ac_id) REFERENCES active_course (ac_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """
    execute_query(create_course_stud_table_query)

    create_stud_lead_table_query = """
        CREATE TABLE IF NOT EXISTS student_register (
            sr_id       INTEGER     PRIMARY KEY
          , course_id   INTEGER     NOT NULL
          , student_id  INTEGER     NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """
    execute_query(create_stud_lead_table_query)

    create_register_table_query = """
        CREATE TABLE IF NOT EXISTS register (
            register_id INTEGER     PRIMARY KEY
          , course_id   INTEGER     NOT NULL
          , name        TEXT        NOT NULL
          , phone       TEXT        NOT NULL
          , email       TEXT        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
        )
        """
    execute_query(create_register_table_query)


def admin_user():
    create_admin_user_query = """
        INSERT INTO user (
            role, email, password
        ) VALUES (
            'Admin', 'admin@admin.com', 'admin'
        )
        """
    execute_query(create_admin_user_query)

    create_attendance_table_query = """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id   INTEGER     PRIMARY KEY
          , class_id          INTEGER     NOT NULL
          , date            TEXT        NOT NULL
          , status           TEXT
          , FOREIGN KEY (class_id) REFERENCES class (class_id)
          , UNIQUE(class_id, date)
        )
        """
    execute_query(create_attendance_table_query)


if __name__ == "__main__":
    create_tables()
    admin_user()
    conn.close()
