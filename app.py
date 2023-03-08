from setup_db import execute_query
from flask import (Flask, render_template, redirect, url_for, request,
                   session)
import datetime


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


def greetings():
    current_time = datetime.datetime.now()
    current_hour = current_time.hour

    if current_hour < 12:
        message = "Good morning"

    elif current_hour < 18:
        message = "Good afternoon"

    else:
        message = "Good evening"

    return message


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
    courses_query = """
        SELECT
            course_id,
            name
        FROM
            course
        """
    courses = execute_query(courses_query)

    top_5_courses_query = """
        SELECT
            name
        FROM
            course
        ORDER BY course_id DESC
        LIMIT 5
        """
    top_5_courses = execute_query(top_5_courses_query)

    return render_template("home.html",
                           courses=courses,
                           new_courses=top_5_courses)


@app.route('/register', methods=["POST"])
def register():
    name = request.form["name"]
    course_id = request.form["course_id"]
    phone = request.form["phone"]
    email = request.form["email"]

    register_query = f"""
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
    execute_query(register_query)

    return redirect(request.referrer)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user_data_query = f"""
            SELECT
                role,
                user_id
            FROM
                user
            WHERE email = '{email}'
            AND password = '{password}'
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


@app.route('/admin_attendance', methods=["GET", "POST"])
def admin_attendance():
    students_query = """
        SELECT DISTINCT
			stud.student_id,
			stud.name
        FROM student stud
        JOIN class ON stud.student_id = class.student_id
        JOIN attendance att ON class.class_id = att.class_id
        """
    students = execute_query(students_query)

    if 'student' in request.args:
        student = request.args.get("student")

        if student == '':
            return redirect(request.referrer)

        student_courses_query = f"""
            SELECT
                class.class_id,
                crs.name,
                stud.name
            FROM
                class
                JOIN active_course ac ON class.ac_id = ac.ac_id
                JOIN course crs ON ac.course_id = crs.course_id
                JOIN student stud ON class.student_id = stud.student_id
                JOIN attendance att ON class.class_id = att.class_id
            WHERE class.student_id = {student}
            """
        courses = execute_query(student_courses_query)
        student_name = courses[0][2]

    else:
        student_name = None
        courses = None

    if 'course' in request.args:
        course = request.args.get("course")

        if course == '':
            return redirect(request.referrer)

        date_attendance_query = f"""
            SELECT
                att.status,
                att.date,
                crs.name,
                ac.ac_id,
                stud.name
            FROM
                attendance att
                JOIN class ON att.class_id = class.class_id
                JOIN active_course ac ON class.ac_id = ac.ac_id
                JOIN course crs ON ac.course_id = crs.course_id
                JOIN student stud on class.student_id = stud.student_id
            WHERE class.class_id = {course}
            """
        attendance = execute_query(date_attendance_query)
        course_name = attendance[0][2]
        student_name = attendance[0][4]

    else:
        course_name = None
        attendance = None

    return render_template("admin-attendance.html",
                           students=students,
                           student=student_name,
                           courses=courses,
                           course=course_name,
                           attendance=attendance)


@app.route('/teacher_work_place', methods=["GET", "POST"])
def teacher_work_place():
    user_id = session["user_id"]

    get_teacher_name_query = f"""
        SELECT name FROM teacher
        WHERE user_id = {user_id}
        """
    teacher_name = execute_query(get_teacher_name_query)[0][0]

    message = greetings()

    if request.method == "POST":
        pass

    return render_template("teacher-work-place.html",
                           name=teacher_name,
                           message=message)


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

    message = greetings()

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
    date = ""
    if "course_id" in request.args:
        active_course = int(request.args.get("course_id"))

        if active_course == 0:
            return redirect(request.referrer)

        date = request.args.get("date")
        get_studend_attendance_query = f"""
            SELECT
                class.class_id,
                stud.name,
                stud.student_id,
                att.status,
                crs.name
            FROM
                class
                INNER JOIN student stud
                    ON class.student_id = stud.student_id
                LEFT JOIN attendance att
                    ON class.class_id = att.class_id AND att.date = '{date}'
                INNER JOIN active_course ac
                    ON class.ac_id = ac.ac_id
                INNER JOIN course crs
                    ON ac.course_id = crs.course_id
            WHERE
                ac.ac_id = {active_course};
            """
        student_attendance = execute_query(get_studend_attendance_query)
        course_name = student_attendance[0][4]

    else:
        student_attendance = []
        course_name = ''

    if request.method == "POST":
        if "att_status" in request.form:
            class_id = request.form["class_id"]
            att_date = request.form["att_date"]
            att_status = request.form["att_status"]

        else:
            return redirect(request.referrer)

        att_check_query = f"""
            SELECT attendance_id
            FROM attendance
            WHERE class_id = {class_id}
            AND date = '{att_date}'
            """
        att_check = execute_query(att_check_query)

        if att_check != []:
            update_attendance_query = f"""
                UPDATE attendance SET
                    status = '{att_status}'
                WHERE date = '{att_date}'
                AND class_id = {class_id}
                """
            execute_query(update_attendance_query)

        else:
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

        return redirect(request.referrer)

    return render_template("teacher-attendance.html",
                           name=teacher[1],
                           message=message,
                           courses=teacher_courses,
                           student_attendance=student_attendance,
                           current_date=current_date,
                           date=date,
                           course=course_name)


@app.route('/student_view/<student_id>')
def student_view(student_id):

    return render_template("student-view.html")


if __name__ == "__main__":
    app.run(debug=True)
