import sqlite3


with sqlite3.connect("database.db", check_same_thread=False) as conn:
    cur = conn.cursor()


def execute_query(schema):
    cur.execute(schema)
    conn.commit()
    return cur.fetchall()


def executemany_query(schema, value):
    cur.executemany(schema, value)
    conn.commit()
    return cur.fetchall()


def create_table():
    execute_query("""
        CREATE TABLE IF NOT EXISTS role (
            role_id             INTEGER     PRIMARY KEY
          , name                TEXT        NOT NULL        UNIQUE
        )
        """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS user (
            user_id             INTEGER     PRIMARY KEY
          , role_id             INTEGER     NOT NULL
          , email               TEXT        NOT NULL        UNIQUE
          , password            TEXT        NOT NULL
          , FOREIGN KEY (role_id) REFERENCES role (role_id)
        )
        """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS student (
            student_id          INTEGER     PRIMARY KEY
          , user_id             INTEGER     NOT NULL        UNIQUE
          , name                TEXT        NOT NULL
          , image               BLOB        NOT NULL
          , gender              TEXT        NOT NULL
          , birth_date          TEXT        NOT NULL
          , phone               TEXT        NOT NULL
          , address             TEXT        NOT NULL
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS teacher (
            teacher_id          INTEGER     PRIMARY KEY
          , user_id             INTEGER     NOT NULL        UNIQUE
          , name                TEXT        NOT NULL
          , image               BLOB        NOT NULL
          , gender              TEXT        NOT NULL
          , birth_date          TEXT        NOT NULL
          , phone               TEXT        NOT NULL
          , address             TEXT        NOT NULL
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS course (
            course_id           INTEGER     PRIMARY KEY
          , name                TEXT        NOT NULL        UNIQUE
          , desc                TEXT        NOT NULL
        )
        """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS active_course (
            active_course_id    INTEGER     PRIMARY KEY
          , course_id           INTEGER     NOT NULL
          , teacher_id          INTEGER     NOT NULL
          , start_date          DATE        NOT NULL
          , end_date            DATE        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id)
        )
        """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS course_stud (
            course_stud_id      INTEGER     PRIMARY KEY
          , active_course_id    INTEGER     NOT NULL
          , student_id          INTEGER     NOT NULL
          , grade               INTEGER
          , FOREIGN KEY (active_course_id) REFERENCES active_course (active_course_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """)
    execute_query("""
        CREATE TABLE IF NOT EXISTS stud_lead (
            stud_lead_id        INTEGER     PRIMARY KEY
          , course_id           INTEGER     NOT NULL
          , student_id          INTEGER     NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """)


def add_roles():
    role_list = [
        ("Student", ),
        ("Teacher", ),
        ("Admin", ),
    ]
    executemany_query("""
        INSERT INTO role (name) VALUES (?)
        """, role_list)


def add_admin_user():
    execute_query("""
        INSERT INTO user (role_id, email, password)
        VALUES ('3', 'admin@admin.com', 'admin')
        """)


if __name__ == "__main__":
    create_table()
    add_roles()
    add_admin_user()
