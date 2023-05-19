from flask import (Blueprint, abort, session, request, render_template,
                   redirect, url_for)
from .models import User, Teacher, Student
import datetime


bp = Blueprint('routes', __name__)


def greetings():
    current_time = datetime.datetime.now()
    current_hour = current_time.hour

    if current_hour < 12:
        message = "Good morning"

    elif current_hour < 18:
        message = "Good afternoon"

    else:
        message = "Good evening"

    return message


@bp.before_request
def auth():
    admin_path_list = ['/admin', '/admin_new_user', '/admin_new_course',
                       '/admin_new_active_course', '/admin_attendance']
    teacher_path_list = ['/teacher_work_place', '/teacher_add_grade',
                         '/teacher_attendance']

    if "role" not in session.keys():
        session["role"] = "anonymous"
        session["username"] = "anonymous"

    if any(route in request.full_path for route in admin_path_list):
        if session['role'] != 'Admin':
            message = 'You do not have permissions'
            abort(403, message)

    if any(route in request.full_path for route in teacher_path_list):
        if session['role'] != 'Teacher':
            message = 'You do not have permissions'
            abort(403, message)

    # elif any(route in request.full_path for route in student_path_list):
    #     if session['role'] != 'Student':
    #         message = 'You do not have permissions'
    #         return render_template('login.html', message=message)


@bp.route('/')
def home():

    return render_template("home.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            message = 'Please provide both email and password.'
            return render_template('login.html', message=message)

        user = User.auth(email=email, password=password)

        if user is None:
            message = 'Invalid email or password'
            return render_template('login.html', message=message)

        session['role'] = user['user_id']
        session['user_id'] = user['user_id']

        if user.role == 'Admin':
            return redirect(url_for('admin_dashboard'))

        elif user.role == 'Teacher':
            teacher = Teacher.read_by(user_id=session['user_id'])
            session['name'] = teacher.name
            session['teacher_id'] = teacher.teacher_id
            return redirect(url_for('teacher_dashboard'))

        else:
            student = Student.read_by(user_id=session['user_id'])
            session['name'] = student.name
            session['student_id'] = student.student_id
            return redirect(url_for('student_dashboard'))

    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


def create_routes():
    return bp
