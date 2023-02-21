from Models.setup_db import execute_query
from flask import (Flask, render_template, redirect, url_for, request,
                   session, abort)
import base64


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# @app.before_request
# def auth():
#     if "role" not in session.keys():
#         session["role"] = "anonymous"
#         session["username"] = "anonymous"

#     elif session["role"] != "Admin":
#         if '/admin' in request.full_path:
#             return abort(403, 'You do not have permissions')

#     elif session["role"] != "Student":
#         pass

#     elif session["role"] != "Teacher":
#         pass


@app.route('/')
def index():
    return render_template("home.html")

    ##  guest register info
# @app.route('/registration_details', methods="POST")
# def registration_details():
#     name = request.form["name"]
#     course_id = request.form["course_id"]
#     date = ""
#     phone = request.form[""]
#     return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user_data = execute_query(f"""
            SELECT role, user_id FROM user
            WHERE email = '{email}' AND password = '{password}'
        """)

        if not user_data:
            abort(403, 'Invalid email or password')

        session['username'] = email
        session['role'] = user_data[0][0]
        session['id'] = user_data[0][1]
        return render_template('home.html')

    return render_template('login.html')


@app.route('/admin')
def admin():
    teacher_list = execute_query("""
        SELECT teacher_id, name FROM teacher
    """)
    course_list = execute_query("""
        SELECT course_id, name FROM course
    """)
    student_list = execute_query("""
        SELECT student_id, name FROM student
    """)
    ac_list = execute_query("""
        SELECT ac_id, course.name, teacher.name FROM ac
        JOIN course ON ac.course_id=course.course_id
        JOIN teacher ON ac.teacher_id=teacher.teacher_id
    """)

    return render_template("admin.html", teacher_list=teacher_list,
                           course_list=course_list, ac_list=ac_list,
                           student_list=student_list)


@app.route('/create_new_user', methods=["POST"])
def create_new_user():
    email = request.form["user_email"]
    password = request.form["user_password"]
    role = request.form["role"]

    execute_query(f"""
        INSERT INTO user (
            email, password, role
        ) VALUES (
            '{email}', '{password}', '{role}'
        )
    """)

    user_id = execute_query(f"""
        SELECT user_id FROM user WHERE email = '{email}'
    """)[0]

    execute_query(f"""
        INSERT INTO student (
            user_id
        ) VALUES (
            '{user_id}'
        )
    """)

    return redirect(url_for("admin"))


@app.route('/create_new_course', methods=["POST"])
def create_new_course():
    course_name = request.form['course_name']
    course_desc = request.form['course_desc']

    execute_query(f"""
        INSERT INTO course (
            name, desc
        ) VALUES (
            '{course_name}', '{course_desc}'
        )
    """)

    return redirect(url_for("admin"))


@app.route('/create_active_course', methods=["POST"])
def create_active_course():
    course_id = request.form['course_id']
    teacher_id = request.form['teacher_id']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    execute_query(f"""
        INSERT INTO active_course (
            course_id, teacher_id, start_date, end_date
        ) VALUES (
            '{course_id}', '{teacher_id}', '{start_date}', '{end_date}'
        )
    """)

    return redirect(url_for("admin"))


@app.route('/add_student_to_active_course', methods=["POST"])
def method_name():
    student_id = request.form['student_id']
    ac_id = request.form['ac_id']
    execute_query(f"""
        INSERT INTO course_stud (
            active_course_id, student_id
        ) VALUES (
            '{student_id}', '{ac_id}'
        )
    """)
    return redirect(url_for("admin"))


@app.route('/profile', methods=["GET", "POST"])
def profile():
    user_id = int(session["id"])
    stud_id = execute_query(f"""
        SELECT student_id FROM student
        JOIN user ON student.user_id = user.user_id
        WHERE student.user_id={user_id}
        """)

    if request.method == "POST":
        name = request.form["name"]
        image = request.files["image"]
        blob_image = base64.b64encode(image.read())
        print(blob_image)
        gender = request.form["gender"]
        birth_date = request.form["date"]
        phone = request.form["phone"]
        address = request.form["address"]
        execute_query(f"""
            UPDATE student SET
                name = ?,
                image = ?,
                gender = ?,
                birth_date = ?,
                phone = ?,
                address = ?
            WHERE user_id = {user_id}
        """, params=(name, blob_image, gender, birth_date, phone, address))

        return redirect(url_for("profile"))

    student_info = execute_query(f"""
        SELECT * FROM user
        JOIN student ON user.user_id = student.user_id
        WHERE user.user_id = {user_id}
    """)

    return render_template("profile.html", student_info=student_info)


@app.route('/course')
def course():
    return render_template("course.html")


@app.route('/teacher')
def teacher():
    return render_template("teacher.html")


@app.route('/student')
def student():
    return render_template("student.html")


# @app.route('/profile/<name>')
# def show_profile(name):
#     teacher_list = execute_query(f"""
#         SELECT * FROM teacher
#         WHERE name LIKE '{name}'
#     """)

#     if teacher_list != 0:
#         return render_template("p.html", data=teacher_list)

#     course_list = execute_query(f"""
#         SELECT * FROM course
#         WHERE name LIKE '{name}'
#     """)

#     if course_list != 0:
#         return render_template("p.html", data=course_list)

#     student_list = execute_query(f"""
#         SELECT * FROM student
#         WHERE name LIKE '{name}'
#     """)

#     if student_list != 0:
#         return render_template("p.html", data=student_list)


# @app.route('/search')
# def x():
#     search = request.args["search"].title()
#     if len(search) != 0:
#         results = []
#         if request.form.get('student'):
#             student_data = execute_query(f"""
#                 SELECT name FROM student
#                 WHERE name LIKE '%{search}%'
#             """)
#             if len(student_data) != 0:
#                 results = list(map(list.__add__, [student for student in student_data], results))

#         if request.form.get('teacher'):
#             teacher_data = execute_query(f"""
#                 SELECT name FROM teacher
#                 WHERE name LIKE '%{search}%'
#             """)
#             if len(teacher_data) != 0:
#                 results = list(map(list.__add__, [teacher for teacher in teacher_data], results))

#         if request.form.get('course'): 
#             course_data = execute_query(f"""
#                 SELECT name FROM course
#                 WHERE name LIKE '%{search}%'
#             """)
#             if len(course_data) != 0:
#                 results = list(map(list.__add__, [course for course in course_data], results))

#         return render_template("search.html", results=results)

#         return redirect(url_for("index"))

#     return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
