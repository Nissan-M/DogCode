from flask import (Blueprint, render_template, redirect, url_for, request,
                   session)
import sys
import os
from app.models import User, Student, Teacher

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

login = Blueprint('login', __name__)


@login.route("/login", methods=["GET", "POST"])
def login_route():
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

        session['role'] = user['role']
        session['user_id'] = user['user_id']

        if session['role'] == 'Admin':
            return redirect(url_for('home.home_route'))

        elif session['role'] == 'Teacher':
            teacher = Teacher.read_by(user_id=session['user_id'])
            session['name'] = teacher.name
            session['teacher_id'] = teacher.teacher_id
            return redirect(url_for('home.home_route'))

        elif session['role'] == 'Student':
            user_id = session['user_id']
            student = Student.read_by(user_id=user_id)
            session['name'] = student.name
            session['student_id'] = student.student_id
            return redirect(url_for('home.home_route'))

    return render_template('login.html')


@login.route('/logout')
def logout():
    session.clear()
    return redirect(request.referrer)
