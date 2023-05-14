import sqlite3


DATABASE_NAME = "database.db"


def execute_query(query, params=None):
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    cursor = conn.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        conn.commit()
        result = cursor.fetchall()

    except sqlite3.Error as e:
        print(f"Error occurred while executing query: {str(e)}")
        result = []

    finally:
        conn.close()

    return result


def create_tables():
    table_queries = [
        """
        CREATE TABLE IF NOT EXISTS user (
            user_id     INTEGER     PRIMARY KEY
          , role        TEXT        NOT NULL
          , email       TEXT        NOT NULL        UNIQUE
          , password    TEXT        NOT NULL
        )
        """, """
        CREATE TABLE IF NOT EXISTS student (
            student_id  INTEGER     PRIMARY KEY
          , user_id     INTEGER     NOT NULL        UNIQUE
          , name        TEXT        NOT NULL
          , image       TEXT
          , gender      TEXT
          , birth_date  DATE
          , phone       TEXT
          , address     TEXT
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS teacher (
            teacher_id  INTEGER     PRIMARY KEY
          , user_id     INTEGER     NOT NULL        UNIQUE
          , name        TEXT        NOT NULL
          , image       TEXT
          , gender      TEXT
          , birth_date  DATE
          , phone       TEXT
          , address     TEXT
          , FOREIGN KEY (user_id) REFERENCES user (user_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS course (
            course_id   INTEGER     PRIMARY KEY
          , name        TEXT        NOT NULL        UNIQUE
          , image       TEXT
          , desc        TEXT
        )
        """, """
        CREATE TABLE IF NOT EXISTS active_course (
            ac_id       INTEGER     PRIMARY KEY
          , course_id   INTEGER     NOT NULL
          , teacher_id  INTEGER     NOT NULL
          , start_date  DATE        NOT NULL
          , end_date    DATE        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (teacher_id) REFERENCES teacher (teacher_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS class (
            class_id  INTEGER     PRIMARY KEY
          , ac_id       INTEGER     NOT NULL
          , student_id  INTEGER     NOT NULL
          , grade       INTEGER
          , FOREIGN KEY (ac_id) REFERENCES active_course (ac_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS student_register (
            sr_id       INTEGER     PRIMARY KEY
          , course_id   INTEGER     NOT NULL
          , student_id  INTEGER     NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
          , FOREIGN KEY (student_id) REFERENCES student (student_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS register (
            register_id INTEGER     PRIMARY KEY
          , course_id   INTEGER     NOT NULL
          , name        TEXT        NOT NULL
          , phone       TEXT        NOT NULL
          , email       TEXT        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES course (course_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id   INTEGER     PRIMARY KEY
          , class_id        INTEGER     NOT NULL
          , date            TEXT        NOT NULL
          , status          TEXT
          , FOREIGN KEY (class_id) REFERENCES class (class_id)
          , UNIQUE(class_id, date)
        )
        """]
    for i, query in enumerate(table_queries, start=1):
        try:
            execute_query(query)
        except sqlite3.Error as e:
            print(f"Error occurred while creating table {i}: {str(e)}")


def admin_user():
    create_query = """
        INSERT INTO user (
            role, email, password
        ) VALUES (
            'Admin', 'admin@admin.com', 'admin'
        )
        """
    try:
        execute_query(create_query)
    except sqlite3.Error as e:
        print(f"Error occurred while creating admin user: {str(e)}")


if __name__ == "__main__":
    create_tables()
    admin_user()
