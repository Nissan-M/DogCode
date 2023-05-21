from flask import Blueprint, render_template
import sys
import os
from app.models import Course

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

courses = Blueprint('courses', __name__)


@courses.route("/courses")
def courses_route():
    courses = Course.read()
    return render_template("courses.html", courses=courses)
