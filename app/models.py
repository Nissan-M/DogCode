import sys
import os
from app.crud.crud_user import User
from app.crud.crud_student import Student
from app.crud.crud_teacher import Teacher
from app.crud.crud_course import Course
from app.crud.crud_teacher_course import TeacherCourse
from app.crud.crud_student_course import StudentCourse
from app.crud.crud_attendance import Attendance
from app.crud.crud_lead import Lead


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, parent_dir)


__all__ = [
    'User',
    'Student',
    'Teacher',
    'Course',
    'TeacherCourse',
    'StudentCourse',
    'Attendance',
    'Lead'
]
