from flask import Blueprint, render_template
import sys
import os
from app.models import Teacher

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

teachers = Blueprint('teachers', __name__)


@teachers.route("/teachers")
def teachers_route():
    teachers = Teacher.read()
    return render_template("teachers.html", teachers=teachers)
