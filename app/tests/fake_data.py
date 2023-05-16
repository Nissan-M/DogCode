import sys
import os
from faker import Faker
from random import choice
from datetime import datetime, timedelta
from app.models import User, Student, Teacher, Course, ActiveCourse


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

fake = Faker()


def add_fake_user(role: str, num: int, faker_seed: int):
    Faker.seed(faker_seed)
    users = [(role, fake.email(), fake.password()) for _ in range(num)]
    try:
        for user in users:
            User.create(*user)
    except Exception as e:
        print(f"Error occurred while adding fake users: {str(e)}")


def add_fake_profile(role: str, num: int, faker_seed: int,
                     student: bool = False, teacher: bool = False):
    add_fake_user(role, num, faker_seed)
    Faker.seed(faker_seed)
    user_list = User.read()

    for user in user_list:
        gender = choice(["Male", "Female"])
        name = (
            fake.name_male()
            if gender == "Male"
            else fake.name_female()
        )
        image = os.path.join(
            "app/static/images",
            "male.jpg" if gender == "Male" else "female.jpg"
        )
        phone = '000-0000000'
        address = 'TEST'
        if student is True and user.role == 'Student':
            birth_date = fake.date_of_birth(
                minimum_age=18,
                maximum_age=30
            ).strftime("%Y-%m-%d")
            Student.create(
                user_id=user.user_id,
                name=name,
                image=image,
                gender=gender,
                birth_date=birth_date,
                phone=phone,
                address=address
            )
        if teacher is True and user.role == 'Teacher':
            birth_date = fake.date_of_birth(
                minimum_age=30,
                maximum_age=55
            ).strftime("%Y-%m-%d")
            Teacher.create(
                user_id=user.user_id,
                name=name,
                image=image,
                gender=gender,
                birth_date=birth_date,
                phone=phone,
                address=address
            )


def add_course():
    course_names = ["Python", "Java", "PHP", "C#", "C++"]
    images = [
         os.path.join("app/static/images", "Python.jpg"),
         os.path.join("app/static/images", "Java.jpg"),
         os.path.join("app/static/images", "PHP.jpg"),
         os.path.join("app/static/images", "C#.jpg"),
         os.path.join("app/static/images", "C++.jpg")
    ]
    course_desc = [
        """
            Python is a computer programming language often used to build
            websites and software, automate tasks, and conduct data analysis.
            Python is a general-purpose language, meaning it can be used to
            create a variety of different programs and isn't specialized for
            any specific problems.
        """, """
            Java is a widely used object-oriented programming language and
            software platform that runs on billions of devices, including
            notebook computers, mobile devices, gaming consoles, medical
            devices and many others. The rules and syntax of Java are based on
            the C and C++ languages.
        """, """
            PHP is an open-source server-side scripting language that many devs
            use for web development. It is also a general-purpose language that
            you can use to make lots of projects, including Graphical User
            Interfaces (GUIs).
        """, """
            C# is an object-oriented, component-oriented programming language.
            C# provides language constructs to directly support these concepts,
            making C# a natural language in which to create and use software
            components. Since its origin, C# has added features to support new
            workloads and emerging software design practices.
        """, """
            C++ is an object-oriented programming language which gives a clear
            structure to programs and allows code to be reused, lowering
            development costs. C++ is portable and can be used to develop
            applications that can be adapted to multiple platforms.
        """
    ]
    courses = list(zip(course_names, images, course_desc))
    for course in courses:
        Course.create(*course)


def create_activeCourse():
    courses = Course.read()
    teachers = Teacher.read()

    for teacher in teachers:
        course = choice(courses)
        name = f"{course.name} - {teacher.name}"
        today = datetime.now().date()
        start_date = fake.date_between_dates(
            date_start=today,
            date_end=today + timedelta(days=30)
        )
        end_date = start_date + timedelta(days=7)

        ActiveCourse.create(
            course_id=course.course_id,
            teacher_id=teacher.teacher_id,
            name=name,
            start_date=start_date,
            end_date=end_date
        )


if __name__ == "__main__":
    add_fake_profile(
        role="Student",
        num=30,
        faker_seed=0,
        student=True
    )
    add_fake_profile(
        role="Teacher",
        num=10,
        faker_seed=1,
        teacher=True
    )
    add_course()
    create_activeCourse()
