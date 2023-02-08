from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)
from setup_db import query
from sqlite3 import IntegrityError

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = execute_query(
            f"SELECT role_id FROM user WHERE user_email='{email}' and user_password='{password}'")[0][0]
        if role is None:
            return render_template("login.html", err="The email or password is incorrect")
        if role == 1:
            pass
        if role == 2:
            pass
        if role == 3:
            return redirect(url_for("register"))

    return render_template("login.html")




@app.route('/admin')
def admin():

    teacher_db = query("""
    SELECT teacher_id, teacher.user_id, teacher_name, user_email, user_password FROM teacher
    JOIN user ON teacher.user_id=user.user_id
        """)
    teachers = [ teacher for teacher in teacher_db ]
    courses = [ course for course in query("SELECT * FROM course") ]
    courseNo_db = query("""
    SELECT courseNo_id, courseNo_sdate, courseNo_edate, courseNo.course_id, courseNo.teacher_id, course.course_name, teacher.teacher_name FROM courseNo
    LEFT JOIN course ON courseNo.course_id=course.course_id
    LEFT JOIN teacher ON courseNo.teacher_id=teacher.teacher_id
    """)
    course_nums = [ course for course in courseNo_db ]
    student_db = query("""
    SELECT student_id, student.user_id, student_name, user_email, user_password FROM student
    JOIN user ON student.user_id=user.user_id
    """)
    students = [ student for student in student_db ]
    roles = query("SELECT * FROM role")

    return render_template("admin.html", teachers=teachers, courses=courses, course_nums=course_nums, students=students, roles=roles)


@app.route('/create_course', methods=["POST"])
def create_course():

    query(f"""
    INSERT INTO course ('course_name', 'course_desc') 
    VALUES ('{request.form['course_name']}', '{request.form['course_desc']}')""")

    return redirect(url_for("admin"))


@app.route('/courseNo_teacher', methods=["POST"])
def teacher_course():

    query(f"""
    INSERT INTO courseNo ('course_id', 'teacher_id', 'courseNo_sdate', 'courseNo_edate')
    VALUES ('{request.form['course_id']}', '{request.form['teacher_id']}','{request.form['start_date']}', '{request.form['end_date']}')
    """)

    return redirect(url_for("admin"))


@app.route('/courseNo_student', methods=["POST"])
def method_name():

    query(f"""
    INSERT INTO courseNo ('student_id', 'courseNo_id') 
    VALUES ('{request.form['student_id']}', '{request.form['course_id']}')
    """)

    return redirect(url_for("admin"))


@app.route('/register', methods=["POST"])
def register():

    email = request.form["email"]
    password = request.form["password"]
    role = request.form["role"]
    query(f"INSERT INTO user (user_email, user_password, role_id) VALUES ('{email}','{password}', '{role}')")
    return redirect(url_for("admin"))
