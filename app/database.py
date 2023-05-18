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
        CREATE TABLE IF NOT EXISTS users (
            user_id                 INTEGER     PRIMARY KEY
          , role                    TEXT        NOT NULL
          , email                   TEXT        NOT NULL
          , password                TEXT        NOT NULL
          , UNIQUE(email)
        )
        """, """
        CREATE TABLE IF NOT EXISTS students (
            student_id              INTEGER     PRIMARY KEY
          , user_id                 INTEGER     NOT NULL
          , name                    TEXT        NOT NULL
          , image                   TEXT
          , gender                  TEXT
          , birth_date              DATE
          , phone                   TEXT
          , address                 TEXT
          , FOREIGN KEY (user_id) REFERENCES users (user_id)
          , UNIQUE(user_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS teachers (
            teacher_id              INTEGER     PRIMARY KEY
          , user_id                 INTEGER     NOT NULL
          , name                    TEXT        NOT NULL
          , image                   TEXT
          , gender                  TEXT
          , birth_date              DATE
          , phone                   TEXT
          , address                 TEXT
          , FOREIGN KEY (user_id) REFERENCES users (user_id)
          , UNIQUE(user_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS courses (
            course_id               INTEGER     PRIMARY KEY
          , name                    TEXT        NOT NULL
          , image                   TEXT
          , desc                    TEXT
          , UNIQUE(name)
        )
        """, """
        CREATE TABLE IF NOT EXISTS teachers_courses (
            teacher_course_id       INTEGER     PRIMARY KEY
          , course_id               INTEGER     NOT NULL
          , teacher_id              INTEGER     NOT NULL
          , name                    TEXT        NOT NULL
          , start_date              DATE        NOT NULL
          , end_date                DATE        NOT NULL
          , FOREIGN KEY (course_id) REFERENCES courses (course_id)
          , FOREIGN KEY (teacher_id) REFERENCES teachers (teacher_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS students_courses (
            student_course_id       INTEGER     PRIMARY KEY
          , teacher_course_id       INTEGER     NOT NULL
          , student_id              INTEGER     NOT NULL
          , grades                  TEXT        DEFAULT '{}'
          , FOREIGN KEY (teacher_course_id) REFERENCES teachers_courses (teacher_course_id)
          , FOREIGN KEY (student_id) REFERENCES students (student_id)
        )
        """, """
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id           INTEGER     PRIMARY KEY
          , student_course_id       INTEGER     NOT NULL
          , date                    TEXT        NOT NULL
          , presence                TEXT
          , FOREIGN KEY (student_course_id) REFERENCES students_courses (student_course_id)
          , UNIQUE(student_course_id, date)
        )
        """, """
        CREATE TABLE IF NOT EXISTS leads (
            lead_id                 INTEGER     PRIMARY KEY
          , course_id               INTEGER     NOT NULL
          , name                    TEXT
          , phone                   TEXT
          , email                   TEXT
          , FOREIGN KEY (course_id) REFERENCES courses (course_id)
        )
        """]
    for i, query in enumerate(table_queries, start=1):
        try:
            execute_query(query)
        except sqlite3.Error as e:
            print(f"Error occurred while creating table {i}: {str(e)}")


if __name__ == "__main__":
    create_tables()
