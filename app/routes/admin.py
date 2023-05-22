from flask import Blueprint, render_template, request, redirect
import sys
import os
from app.models import Course, Teacher, TeacherCourse, Student, StudentCourse

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

admin = Blueprint('admin', __name__)


@admin.route("/admin")
def admin_wp_route():
    courses = Course.read()
    teachers = Teacher.read()
    teachers_courses = TeacherCourse.read()
    students = Student.read()
    template_data = {
        'courses': courses,
        'teachers': teachers,
        'teachers_courses': teachers_courses,
        'students': students
    }
    return render_template("admin.html", **template_data)


@admin.route("/admin_teacher_course", methods=["POST"])
def admin_teacher_course():
    course_id = request.form.get("tc_course_id")
    teacher_id = request.form.get("tc_teacher_id")
    start_date = request.form.get("tc_start_date")
    end_date = request.form.get("tc_end_date")
    if all([course_id, teacher_id, start_date, end_date]):
        TeacherCourse.create(
            course_id=course_id,
            teacher_id=teacher_id,
            start_date=start_date,
            end_date=end_date
        )
    return redirect("/admin")


@admin.route("/admin_student_course", methods=["POST"])
def admin_student_course():
    teacer_course_id = request.form.get("tc_id")
    student_id = request.form.get("studnet_id")
    if all([teacer_course_id, student_id]):
        StudentCourse.create(
            teacher_course_id=teacer_course_id,
            student_id=student_id
        )
    return redirect("/admin")
