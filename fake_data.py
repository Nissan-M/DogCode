from setup_db import execute_query, executemany_query
from faker import Faker
from random import choice, randint

fake = Faker()


def convert_pic():
    files = ["./images/avatar_male.jpg", "./images/avatar_female.jpg"]
    picture = [open(file, "rb").read() for file in files]
    return picture


def add_fake_user(role, num, faker_seed):
    Faker.seed(faker_seed)
    users = [(role, fake.email(), fake.password()) for i in range(num)]
    executemany_query("""
        INSERT INTO user (role, email, password)
        VALUES (?, ?, ?)
        """, users)


def add_fake_profile(table, role, num, faker_seed, slice, max, min):
    add_fake_user(role, num, faker_seed)
    Faker.seed(faker_seed)
    m_img, f_img = convert_pic()
    user_db = execute_query(f"SELECT user_id FROM user WHERE role='{role}'")
    user_ids = [int(user_id[0]) for user_id in user_db]
    male_profiles = [
        (user_id, fake.first_name_male(), m_img, "Male",
         fake.date_of_birth(minimum_age=min, maximum_age=max), "0", "x", )
        for user_id in user_ids[:slice]
    ]
    female_profiles = [
        (user_id, fake.first_name_female(), f_img, "Female",
         fake.date_of_birth(minimum_age=min, maximum_age=max), "0", "x", )
        for user_id in user_ids[slice:]
    ]
    executemany_query(f"""
        INSERT INTO {table} (
            user_id, name, image, gender, birth_date, phone, address
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, male_profiles + female_profiles)


def add_course():
    course_names = ["Python", "Java", "PHP", "C#", "C++"]
    course_desc = [
        """Python is a computer programming language often used to build websites and software, automate tasks, and conduct data analysis. Python is a general-purpose language, meaning it can be used to create a variety of different programs and isn't specialized for any specific problems.""",
        """Java is a widely used object-oriented programming language and software platform that runs on billions of devices, including notebook computers, mobile devices, gaming consoles, medical devices and many others. The rules and syntax of Java are based on the C and C++ languages.""",
        """PHP is an open-source server-side scripting language that many devs use for web development. It is also a general-purpose language that you can use to make lots of projects, including Graphical User Interfaces (GUIs).
        """,
        """C# is an object-oriented, component-oriented programming language. C# provides language constructs to directly support these concepts, making C# a natural language in which to create and use software components. Since its origin, C# has added features to support new workloads and emerging software design practices.""",
        """C++ is an object-oriented programming language which gives a clear structure to programs and allows code to be reused, lowering development costs. C++ is portable and can be used to develop applications that can be adapted to multiple platforms."""
    ]
    courses = dict(zip(course_names, course_desc))
    course_list = [(course, courses[course]) for course in courses]
    executemany_query("""
        INSERT INTO course (name, desc)
        VALUES (?, ?)
        """, course_list)


def create_active_course():
    teacher_db = execute_query("SELECT teacher_id FROM teacher")
    teacher_ids = [int(teacher[0]) for teacher in teacher_db]
    course_db = execute_query("SELECT course_id FROM course")
    course_ids = [int(course[0]) for course in course_db]
    teacher_course_ids = [
        (teacher, choice(course_ids), "2023-02-13", "2023-08-15", )
        for teacher in teacher_ids
    ]
    executemany_query("""
        INSERT INTO ac (
            teacher_id, course_id, start_date, end_date
        )
        VALUES (?, ?, ?, ?)
    """, teacher_course_ids)


def add_studet_to_active_course():
    student_db = execute_query("SELECT student_id FROM student")
    student_ids = [student[0] for student in student_db]
    courseNo_db = execute_query("SELECT ac_id FROM ac")
    courseNo_ids = [course[0] for course in courseNo_db]
    student_course_ids = [
        (teacher, choice(courseNo_ids), randint(70, 100))
        for teacher in student_ids
    ]
    executemany_query("""
        INSERT INTO ac_stud (
            student_id, ac_id, grade
        )
        VALUES (?, ?, ?)
    """, student_course_ids)


if __name__ == "__main__":
    add_fake_profile(
        table="student", role="Student", num=40,
        faker_seed=0, slice=15, min=21, max=40
    )
    add_fake_profile(
        table="teacher", role="Teacher", num=10,
        faker_seed=1, slice=3, min=35, max=70
    )
    add_course()
    create_active_course()
    add_studet_to_active_course()
