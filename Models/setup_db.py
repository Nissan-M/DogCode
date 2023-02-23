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
        CREATE TABLE IF NOT EXISTS ac (
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
        CREATE TABLE IF NOT EXISTS ac_stud (
            ac_stud_id  INTEGER     PRIMARY KEY
          , ac_id       INTEGER     NOT NULL
          , student_id  INTEGER     NOT NULL
          , grade       INTEGER
          , FOREIGN KEY (ac_id) REFERENCES ac (ac_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """
    execute_query(create_course_stud_table_query)

    create_stud_lead_table_query = """
        CREATE TABLE IF NOT EXISTS sl (
            sl_id       INTEGER     PRIMARY KEY
          , course_id   INTEGER     NOT NULL
          , student_id  INTEGER     NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """
    execute_query(create_stud_lead_table_query)

    create_guest_lead_table_query = """
        CREATE TABLE IF NOT EXISTS lead (
            lead_id     INTEGER     PRIMARY KEY
          , name        TEXT        NOT NULL
          , email       TEXT        NOT NULL
          , phone       TEXT        NOT NULL
          , course_id   INTEGER     NOT NULL
          , date        DATE        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
        )
        """
    execute_query(create_guest_lead_table_query)


def admin_user():
    create_admin_user_query = """
        INSERT INTO user (
            role, email, password
        ) VALUES (
            'Admin', 'admin@admin.com', 'admin'
        )
        """
    execute_query(create_admin_user_query)


if __name__ == "__main__":
    create_tables()
    admin_user()
    conn.close()
