from setup_db import execute_query
from flask import (Flask, render_template, redirect, url_for, request,
                   session)
import datetime


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.before_request
def auth():
    if "role" not in session.keys():
        session["role"] = "anonymous"
        session["username"] = "anonymous"

    elif session["role"] != "Admin":
        if '/control_panel' in request.full_path:
            message = "You do not have permissions"

            return render_template('login.html', message=message)

    elif session["role"] != "Student":
        pass

    elif session["role"] != "Teacher":
        pass


@app.route('/')
def index():
    get_courses_query = """
        SELECT course_id, name FROM course
    """
    courses = execute_query(get_courses_query)

    get_top_5_courses_query = """
        SELECT name FROM course ORDER BY course_id DESC LIMIT 5
    """
    top_5_courses = execute_query(get_top_5_courses_query)

    return render_template("home.html", courses=courses,
                           new_courses=top_5_courses)


@app.route('/register', methods=["POST"])
def register():
    name = request.form["name"]
    course_id = request.form["course_id"]
    phone = request.form["phone"]
    email = request.form["email"]

    query = f"""
        INSERT INTO register (
            course_id,
            name,
            phone,
            email
        ) VALUES (
            '{course_id}',
            '{name}',
            '{phone}',
            '{email}'
        )
    """
    execute_query(query)

    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data_query = f"""
            SELECT
                role,
                user_id
            FROM user
            WHERE email = '{email}' AND password = '{password}'
        """
        user_data = execute_query(user_data_query)

        if not user_data:
            message = 'Invalid email or password'

            return render_template('login.html', message=message)

        session['username'] = email
        session['role'] = user_data[0][0]
        session['user_id'] = user_data[0][1]

        return render_template('home.html')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()

    return redirect(url_for("login"))


@app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        pass

    return render_template("admin.html")


@app.route('/admin_new_user', methods=["GET", "POST"])
def admin_new_user():
    if request.method == "POST":
        pass

    return render_template("admin-user.html")


@app.route('/admin_new_course', methods=["GET", "POST"])
def admin_new_course():
    if request.method == "POST":
        if "add_course":
            course_name = request.form["course_name"]
            course_desc = request.form["course_desc"]

            add_new_course_query = f"""
                INSERT INTO course (
                    name,
                    desc
                ) VALUES (
                    '{course_name}',
                    '{course_desc}'
                )
            """
            execute_query(add_new_course_query)

            return redirect("admin_new_course")

    return render_template("admin-course.html")


@app.route('/admin_new_active_course', methods=["GET", "POST"])
def admin_new_active_course():
    if request.method == "POST":
        pass

    return render_template("admin-active-course.html")


@app.route('/teacher_work_place', methods=["GET", "POST"])
def teacher_work_place():
    user_id = session["user_id"]

    get_teacher_name_query = f"""
        SELECT name FROM teacher
        WHERE user_id = {user_id}
        """
    teacher_name = execute_query(get_teacher_name_query)[0][0]

    if request.method == "POST":
        pass

    return render_template("teacher-work-place.html",
                           name=teacher_name)


@app.route('/teacher_add_grade', methods=["GET", "POST"])
def teacher_add_grade():
    user_id = session["user_id"]

    get_teacher_name_query = f"""
        SELECT name FROM teacher
        WHERE user_id = {user_id}
        """
    teacher_name = execute_query(get_teacher_name_query)[0][0]

    get_teacher_courses_query = f"""
        SELECT
            active_course.ac_id,
            course.name
        FROM active_course
        JOIN course
            ON active_course.course_id = course.course_id
        JOIN teacher
            ON active_course.teacher_id = teacher.teacher_id
        WHERE teacher.user_id = {user_id}
        """
    teacher_courses = execute_query(get_teacher_courses_query)

    active_course_id = request.form["active_course_id"]

    get_student_grade_query = f"""
        SELECT
            active_course_student.acs_id,
            active_course_student.grade,
            student.student_id,
            student.name
        FROM active_course_student
        JOIN student
            ON active_course_student.student_id = student.student_id
        JOIN active_course
            ON active_course_student.ac_id = active_course.ac_id
        JOIN course
            ON active_course.course_id = course.course_id
        WHERE active_course.ac_id = {active_course_id}
    """
    students_grade = execute_query(get_student_grade_query)

    if request.method == "POST":

        return render_template("teacher-work-place-add-grade.html",
                               name=teacher_name,
                               courses=teacher_courses,
                               students_grade=students_grade)

    return render_template("teacher-work-place-add-grade.html",
                           name=teacher_name,
                           courses=teacher_courses)


@app.route('/teacher_attendance', methods=["GET", "POST"])
def teacher_attendance():
    user_id = session["user_id"]

    get_teacher_query = f"""
        SELECT teacher_id, name FROM teacher
        WHERE user_id = {user_id}
        """
    teacher = execute_query(get_teacher_query)[0]

    current_date = datetime.date.today()

    get_teacher_courses_query = f"""
        SELECT
            course.name,
            active_course.ac_id
        FROM
            course
        JOIN active_course
            ON course.course_id = active_course.course_id
        WHERE active_course.teacher_id = {teacher[0]}
        """
    teacher_courses = execute_query(get_teacher_courses_query)

    active_course = ""
    if "course_id" in request.args:
        active_course = request.args.get("course_id")

        get_studend_attendance_query = f"""
            SELECT
                class.class_id,
                student.name,
                student.student_id,
                attendance.status,
                course.name
            FROM class
            JOIN student
                ON class.student_id = student.student_id
            LEFT JOIN attendance
                ON class.class_id = attendance.class_id
            JOIN active_course
                ON class.ac_id = active_course.ac_id
            JOIN course
                ON active_course.course_id = course.course_id
            WHERE active_course.ac_id = {active_course}
            """
        student_attendance = execute_query(get_studend_attendance_query)
        course_name = student_attendance[0][4]

    else:
        student_attendance = []
        course_name = ''

    if request.method == "POST":
        class_id = request.form["class_id"]
        att_date = request.form["att_date"]
        att_status = request.form["att_status"]

        att_check_query = f"""
            SELECT attendance_id FROM attendance
            WHERE class_id = {class_id}
            """
        att_check = execute_query(att_check_query)

        if att_check == []:
            add_attendance_query = f"""
                INSERT INTO attendance (
                    class_id,
                    date,
                    status
                ) VALUES (
                    '{class_id}',
                    '{att_date}',
                    '{att_status}'
                )
                """
            execute_query(add_attendance_query)

        else:
            update_attendance_query = f"""
                UPDATE attendance SET
                    status = '{att_status}'
                WHERE attendance_id = {att_check[0][0]}
                """
            execute_query(update_attendance_query)

        return redirect(request.referrer)

    return render_template("teacher-attendance.html",
                           name=teacher[1],
                           courses=teacher_courses,
                           student_attendance=student_attendance,
                           current_date=current_date,
                           course=course_name)


@app.route('/student_view/<student_id>')
def student_view(student_id):

    return render_template("student-view.html")


if __name__ == "__main__":
    app.run(debug=True)
