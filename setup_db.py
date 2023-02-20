import sqlite3


DATABASE_NAME = "database.db"


def execute_query(schema, conn, fetchall=False):
    cursor = conn.cursor()
    cursor.execute(schema)
    if fetchall:
        return cursor.fetchall()
    return conn.commit()


def executemany_query(schema, value, conn):
    cursor = conn.cursor()
    cursor.executemany(schema, value)
    return conn.commit()


def create_tables(conn):
    create_user_table_query = """
        CREATE TABLE IF NOT EXISTS user (
            user_id             INTEGER     PRIMARY KEY
          , role                TEXT        NOT NULL
          , email               TEXT        NOT NULL        UNIQUE
          , password            TEXT        NOT NULL
        )
        """
    execute_query(create_user_table_query, conn)

    create_student_table_query = """
        CREATE TABLE IF NOT EXISTS student (
            student_id          INTEGER     PRIMARY KEY
          , user_id             INTEGER     NOT NULL        UNIQUE
          , name                TEXT        NOT NULL
          , image               BLOB
          , gender              TEXT
          , birth_date          DATE
          , phone               TEXT
          , address             TEXT
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """
    execute_query(create_student_table_query, conn)

    create_teacher_table_query = """
        CREATE TABLE IF NOT EXISTS teacher (
            teacher_id          INTEGER     PRIMARY KEY
          , user_id             INTEGER     NOT NULL        UNIQUE
          , name                TEXT        NOT NULL
          , image               BLOB
          , gender              TEXT
          , birth_date          DATE
          , phone               TEXT
          , address             TEXT
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """
    execute_query(create_teacher_table_query, conn)

    create_course_table_query = """
        CREATE TABLE IF NOT EXISTS course (
            course_id           INTEGER     PRIMARY KEY
          , name                TEXT        NOT NULL        UNIQUE
          , desc                TEXT        NOT NULL
        )
        """
    execute_query(create_course_table_query, conn)

    create_active_course_table_query = """
        CREATE TABLE IF NOT EXISTS active_course (
            active_course_id    INTEGER     PRIMARY KEY
          , course_id           INTEGER     NOT NULL
          , teacher_id          INTEGER     NOT NULL
          , start_date          DATE        NOT NULL
          , end_date            DATE        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id)
        )
        """
    execute_query(create_active_course_table_query, conn)

    create_course_stud_table_query = """
        CREATE TABLE IF NOT EXISTS course_stud (
            course_stud_id      INTEGER     PRIMARY KEY
          , active_course_id    INTEGER     NOT NULL
          , student_id          INTEGER     NOT NULL
          , grade               INTEGER
          , FOREIGN KEY (active_course_id) REFERENCES active_course (active_course_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """
    execute_query(create_course_stud_table_query, conn)

    create_stud_lead_table_query = """
        CREATE TABLE IF NOT EXISTS stud_lead (
            stud_lead_id        INTEGER     PRIMARY KEY
          , course_id           INTEGER     NOT NULL
          , student_id          INTEGER     NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """
    execute_query(create_stud_lead_table_query, conn)


def admin_user(conn):
    create_admin_user_query = """
        INSERT INTO user (
            role, email, password
        ) VALUES (
            'admin', 'admin@test.com', 'Admin
        )
        """
    execute_query(create_admin_user_query, conn)


if __name__ == "__main__":
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    create_tables(conn)
    admin_user(conn)
    conn.close()
