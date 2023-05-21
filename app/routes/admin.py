from flask import Blueprint, render_template
import sys
import os

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..."))
sys.path.insert(0, parent_dir)

admin = Blueprint('admin', __name__)


@admin.route("/admin")
def admin_wp_route():
    return render_template("admin.html")
