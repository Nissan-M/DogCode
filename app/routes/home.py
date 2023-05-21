from flask import Blueprint, render_template, request, redirect
import sys
import os
from app.models import Course, Lead

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

home = Blueprint('home', __name__)


@home.route('/')
def home_route():
    courses = Course.read()
    return render_template("home.html", courses=courses)


@home.route('/lead', methods=["POST"])
def leads():
    course = request.form.get('course_id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')

    if all([course, name, phone, email]):
        Lead.create(
            course_id=course,
            name=name,
            phone=phone,
            email=email,
        )
    return redirect('/')
