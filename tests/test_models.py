import sys
import os
import pytest
from app.models import (User, Student, Teacher, Course, TeacherCourse,
                        StudentCourse)


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)


@pytest.fixture
def user_data():
    return {
        'user_id': 1,
        'role': 'Admin',
        'email': 'admin@test.com',
        'password': 'admin123'
    }


def test_create_user(user_data):
    User.create(
        role=user_data['role'],
        email=user_data['email'],
        password=user_data['password']
    )

    users = User.read()

    assert users is not None
    assert len(users) == 1

    user_by_email = User.read_by(email=user_data['email'])

    assert user_by_email.role == user_data['role']
    assert user_by_email.email == user_data['email']

    user_by_id = User.read_by(user_by_email.user_id)

    assert user_by_id.user_id == user_data['user_id']


def test_user_authentication(user_data):
    user = User.auth(email=user_data['email'], password=user_data['password'])

    assert user is not None
    assert user['role'] == user_data['role']
    assert user['email'] == user_data['email']


def test_update_user(user_data):
    new_role = 'Role'
    new_email = 'test@test.com'
    new_password = '123123'

    User.update(
        user_id=user_data['user_id'],
        role=new_role,
        email=new_email,
        password=new_password
    )

    user = User.read_by(user_id=user_data['user_id'])

    assert user.role == new_role
    assert user.email == new_email
    assert user.password == new_password


def test_delete_user(user_data):
    User.delete(
        user_id=user_data['user_id']
    )

    user = User.read()
    assert len(user) == 0


@pytest.fixture
def student_data():
    return {
        'student_id': 1,
        'user_id': 1,
        'email': 'Kawasaki@test.com',
        'password': 'kawasaki123',
        'name': 'Kawasaki Ninja',
        'image': 'NULL',
        'gender': 'Male',
        'birth_date': '2000-01-01',
        'phone': '000-0000000',
        'address': 'eifo shehu sam',
    }


def test_create_student(student_data):
    Student.create(
        email=student_data['email'],
        password=student_data['password'],
        name=student_data['name'],
        image=student_data['image'],
        gender=student_data['gender'],
        birth_date=student_data['birth_date'],
        phone=student_data['phone'],
        address=student_data['address']
    )

    students = Student.read()
    assert students is not None
    assert len(students) == 1

    student = Student.read_by_id(student_id=student_data['student_id'])
    assert student.student_id == student_data['student_id']
    assert student.user_id == student_data['user_id']
    assert student.name == student_data['name']
    assert student.image == student_data['image']
    assert student.gender == student_data['gender']
    assert student.birth_date == student_data['birth_date']
    assert student.phone == student_data['phone']
    assert student.address == student_data['address']


def test_update_student(student_data):
    new_name = 'test name'
    new_image = 'test image'
    new_gender = 'test gender'
    new_birth_date = 'test birth date'
    new_phone = 'test phone'
    new_address = 'test address'
    new_email = 'test@test.com'
    new_password = 'test password'

    Student.update(
        student_id=student_data['student_id'],
        name=new_name,
        image=new_image,
        gender=new_gender,
        birth_date=new_birth_date,
        phone=new_phone,
        address=new_address,
        email=new_email,
        password=new_password
    )

    student = Student.read_by_id(student_data['student_id'])

    assert student.name == new_name
    assert student.image == new_image
    assert student.gender == new_gender
    assert student.birth_date == new_birth_date
    assert student.phone == new_phone
    assert student.address == new_address
    assert student.email == new_email
    assert student.password == new_password


def test_delete_student(student_data):
    Student.delete(student_data['student_id'])

    user = User.read()

    assert len(user) == 0

    student = Student.read()
    assert len(student) == 0


@pytest.fixture
def teacher_data():
    return {
        'teacher_id': 1,
        'user_id': 1,
        'email': 'Kawasaki@test.com',
        'password': 'kawasaki123',
        'name': 'Kawasaki Ninja',
        'image': 'NULL',
        'gender': 'Male',
        'birth_date': '2000-01-01',
        'phone': '000-0000000',
        'address': 'eifo shehu sam',
    }


def test_create_teacher(teacher_data):
    Teacher.create(
        email=teacher_data['email'],
        password=teacher_data['password'],
        name=teacher_data['name'],
        image=teacher_data['image'],
        gender=teacher_data['gender'],
        birth_date=teacher_data['birth_date'],
        phone=teacher_data['phone'],
        address=teacher_data['address']
    )

    teacher = Teacher.read()
    assert teacher is not None
    assert len(teacher) == 1

    teacher = Teacher.read_by_id(teacher_id=teacher_data['teacher_id'])
    assert teacher.teacher_id == teacher_data['teacher_id']
    assert teacher.user_id == teacher_data['user_id']
    assert teacher.name == teacher_data['name']
    assert teacher.image == teacher_data['image']
    assert teacher.gender == teacher_data['gender']
    assert teacher.birth_date == teacher_data['birth_date']
    assert teacher.phone == teacher_data['phone']
    assert teacher.address == teacher_data['address']


def test_update_teacher(teacher_data):
    new_name = 'test name'
    new_image = 'test image'
    new_gender = 'test gender'
    new_birth_date = 'test birth date'
    new_phone = 'test phone'
    new_address = 'test address'
    new_email = 'test@test.com'
    new_password = 'test password'

    Teacher.update(
        teacher_id=teacher_data['teacher_id'],
        name=new_name,
        image=new_image,
        gender=new_gender,
        birth_date=new_birth_date,
        phone=new_phone,
        address=new_address,
        email=new_email,
        password=new_password
    )

    teacher = Teacher.read_by_id(teacher_data['teacher_id'])

    assert teacher.name == new_name
    assert teacher.image == new_image
    assert teacher.gender == new_gender
    assert teacher.birth_date == new_birth_date
    assert teacher.phone == new_phone
    assert teacher.address == new_address
    assert teacher.email == new_email
    assert teacher.password == new_password


def test_delete_teacher(teacher_data):
    Teacher.delete(teacher_data['teacher_id'])

    user = User.read()
    assert len(user) == 0

    teacher = Teacher.read()
    assert len(teacher) == 0


@pytest.fixture
def course_data():
    return {
        'course_id': 1,
        'name': 'NULL',
        'image': 'NULL',
        'desc': 'NULL'
    }


def test_create_course(course_data):
    Course.create(
        name=course_data['name'],
        image=course_data['image'],
        desc=course_data['desc']
    )

    courses = Course.read()

    assert len(courses) == 1

    course = Course.read_by_id(course_data['course_id'])

    assert course.course_id == course_data['course_id']
    assert course.name == course_data['name']
    assert course.image == course_data['image']
    assert course.desc == course_data['desc']


def test_update_course(course_data):
    new_name = 'test name'
    new_image = 'test image'
    new_desc = 'test desc'
    Course.update(
        course_id=course_data['course_id'],
        name=new_name,
        image=new_image,
        desc=new_desc
        )

    course = Course.read_by_id(course_data['course_id'])

    assert course.name == new_name
    assert course.image == new_image
    assert course.desc == new_desc


def test_delete_course(course_data):
    Course.delete(course_data['course_id'])

    courses = Course.read()
    assert len(courses) == 0


@pytest.fixture
def teacher_course_data():
    return {
        'teacher_course_id': 1,
        'course_id': 1,
        'teacher_id': 1,
        'name': 'course_1',
        'start_date': '2023-01-01',
        'end_date': '2023-12-12'
    }


def test_create_teacher_course(teacher_course_data):
    Course.create(name='test', image='test', desc='test')
    Teacher.create(email='test', password='test', name='test')
    TeacherCourse.create(
        course_id=teacher_course_data['course_id'],
        teacher_id=teacher_course_data['teacher_id'],
        name=teacher_course_data['name'],
        start_date=teacher_course_data['start_date'],
        end_date=teacher_course_data['end_date']
    )

    teacher_courses = TeacherCourse.read()

    assert len(teacher_courses) == 1

    teacher_course = TeacherCourse.read_by(
        teacher_course_id=teacher_course_data['teacher_course_id']
    )

    teacher_course_id = teacher_course_data['teacher_course_id']

    assert teacher_course.teacher_course_id == teacher_course_id
    assert teacher_course.course_id == teacher_course_data['course_id']
    assert teacher_course.teacher_id == teacher_course_data['teacher_id']
    assert teacher_course.name == teacher_course_data['name']
    assert teacher_course.start_date == teacher_course_data['start_date']
    assert teacher_course.end_date == teacher_course_data['end_date']


def test_update_teacher_course(teacher_course_data):
    new_name = 'test name'
    new_start_date = 'test start date'
    new_end_date = 'test end date'

    TeacherCourse.update(
        teacher_course_id=teacher_course_data['teacher_course_id'],
        name=new_name,
        start_date=new_start_date,
        end_date=new_end_date
    )

    teacher_course = TeacherCourse.read_by(
        teacher_course_id=teacher_course_data['teacher_course_id']
    )

    assert teacher_course.name == new_name
    assert teacher_course.start_date == new_start_date
    assert teacher_course.end_date == new_end_date


def test_delete_teacher_course():
    TeacherCourse.delete(teacher_course_id=1)
    Teacher.delete(teacher_id=1)
    Course.delete(course_id=1)

    teacher_course = TeacherCourse.read()

    assert len(teacher_course) == 0


def test_create_student_course():
    Course.create(name='test', image='test', desc='test')
    Teacher.create(email='test2', password='test2', name='test2')
    TeacherCourse.create(
        course_id=1,
        teacher_id=1,
        name='test',
        start_date='test',
        end_date='test'
    )
    Student.create(email='test1', password='test1', name='test1')
    StudentCourse.create(teacher_course_id=1, student_id=1)

    student_courses = StudentCourse.read()

    assert len(student_courses) == 1

    student_course = StudentCourse.read_by(student_course_id=1)

    assert student_course.student_course_id == 1
    assert student_course.teacher_course_id == 1
    assert len(student_course.grades) == 0


def test_update_student_course_1():
    project_name, grade = 'test', 100

    StudentCourse.update(
        student_course_id=1,
        project_name=project_name,
        grade=grade
    )

    student_course = StudentCourse.read_by(student_course_id=1)

    assert student_course.student_course_id == 1


def test_update_student_course_2():
    project_name = 'project_1'
    new_grade = 90

    StudentCourse.update(
        student_course_id=1,
        project_name=project_name,
        grade=new_grade
    )

    student_course = StudentCourse.read_by(student_course_id=1).grades

    assert len(student_course) == 2


def test_delete_student_course():
    StudentCourse.delete(student_course_id=1)
    Student.delete(student_id=1)
    TeacherCourse.delete(teacher_course_id=1)
    Teacher.delete(teacher_id=1)
    Course.delete(course_id=1)

    student_course = StudentCourse.read()

    assert len(student_course) == 0
