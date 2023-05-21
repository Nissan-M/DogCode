from flask import Blueprint, session, request, abort
import sys
import os


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

auth = Blueprint('auth', __name__)


@auth.before_app_request
def authenticate():
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
