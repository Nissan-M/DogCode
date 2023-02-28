from setup_db import execute_query
from flask import (Flask, render_template, redirect, url_for, request,
                   session)


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
        session['id'] = user_data[0][1]

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
    user_id = session["id"]

    get_teacher_info_query = f"""
        SELECT
            teacher_id,
            name
        FROM teacher
        WHERE user_id = {user_id}
        """
    teacher = execute_query(get_teacher_info_query)[0]

    get_courses_query = f"""
        SELECT
            active_course.ac_id,
            course.name
        FROM active_course
        JOIN course
            ON active_course.course_id = course.course_id
        WHERE teacher_id = {teacher[0]}
        """
    courses = execute_query(get_courses_query)

    if request.method == "POST":
        active_course_id = request.form["active_course_id"]

        get_student_grade_query = f"""
            SELECT
                active_course_student.acs_id,
                active_course_student.grade,
                student.student_id,
                student.name,
                course.name
            FROM active_course_student
            JOIN student
                ON active_course_student.student_id = student.student_id
            JOIN active_course
                ON active_course_student.ac_id = active_course.ac_id
            JOIN course
                ON active_course.course_id = course.course_id
            WHERE active_course.ac_id = {active_course_id}
        """
        students = execute_query(get_student_grade_query)

        return render_template("teacher-work-place.html", students=students,
                               courses=courses, teacher_name=teacher[1])

    return render_template("teacher-work-place.html", courses=courses,
                           teacher_name=teacher[1])


@app.route('/add_student_grade', methods=["POST"])
def add_student_grade():
    student_id = request.form["student_id"]
    grade = request.form["grade"]

    update_grade_query = f"""
        UPDATE active_course_student SET
            grade = '{grade}'
        WHERE student_id = {student_id}
        """
    execute_query(update_grade_query)

    return redirect(request.referrer)


@app.route('/student_view/<student_id>')
def student_view(student_id):

    return render_template("student.html")







if __name__ == "__main__":
    app.run(debug=True)
