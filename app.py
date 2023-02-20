from flask import Flask, render_template, redirect, url_for, request, session, abort
from setup_db import execute_query


app = Flask(__name__)


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/home')
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if not email or not password:
            abort(400, 'Email and password are required')

        user_data = execute_query("""
            SELECT user_id, role
            FROM user
            WHERE email = %s AND password = %s
        """, (email, password))

        if not user_data:
            abort(403, 'Invalid email or password')

        session['username'] = email
        session['role'] = user_data[0]['role']
        session['id'] = user_data[0]['user_id']
        return render_template('home.html')

    return render_template('login.html')


@app.route('/guest')
def guest():
    return render_template("guest.html")


@app.route('/profile', methods=["GET", "POST"])
def profile():
    user_id = int(session["id"])
    stud_id = execute_query(f""" SELECT student_id FROM student
        JOIN user ON student.user_id = user.user_id
        WHERE student.user_id={user_id}""")
    if request.method == "POST":
        name = request.form["name"]
        image = request.form["image"]
        gender = request.form["gender"]
        birth_date = request.form["date"]
        phone = request.form["phone"]
        address = request.form["address"]
        execute_query(f"""
            UPDATE student SET
                name='{name}', image='{image}', gender='{gender}',
                birth_date='{birth_date}', phone='{phone}', address='{address}'
            WHERE student_id={stud_id}
            """)

        return redirect(url_for("profile"))

    student_info = execute_query(f"""
    SELECT * FROM user
    JOIN student ON user.user_id = student.user_id
    WHERE user.user_id = {user_id}""")

    return render_template("profile.html", student_info=student_info, x=user_id)


@app.route('/admin')
def admin():
    teachers = execute_query("""
        SELECT * FROM teacher
        """)
    courses = execute_query(f"""
        SELECT * FROM course
        """)
    active_courses = execute_query(f"""
        SELECT * FROM active_course
        """)
    students = execute_query(f"""
        SELECT * FROM student
        """)

    return render_template("admin.html", teachers=teachers,
                           courses=courses, active_courses=active_courses,
                           students=students,)


@app.route('/new_user', methods=["POST"])
def register():
    execute_query(f"""
        INSERT INTO user (
            email, password, role
        ) VALUES (
            '{request.form["email"]}'
          , '{request.form["password"]}'
          , '{request.form["role"]}'
        )
    """)
    execute_query(f"""
        INSERT INTO student (user_id)
        VALUES (
            (SELECT user_id FROM user WHERE email = '{request.form["email"]}')
        )
    """)
    return redirect(url_for("admin"))


@app.route('/new_course', methods=["POST"])
def create_course():
    crud.new_course(name=request.form['name'],
                    desc=request.form['desc'])

    return redirect(url_for("admin"))


@app.route('/add_active_course', methods=["POST"])
def teacher_course():
    execute_query(f"""
        INSERT INTO active_course (
            course_id,
            teacher_id,
            start_date,
            end_date
        ) VALUES (
            '{request.form['course_id']}',
            '{request.form['teacher_id']}',
            '{request.form['start_date']}',
            '{request.form['end_date']}',
        ) 
        """)

    return redirect(url_for("admin"))


@app.route('/add_student_to_active_course', methods=["POST"])
def method_name():
    execute_query(f"""
        INSERT INTO course_stud (
            active_course_id,
            student_id
        ) VALUES (
            '{request.form['student_id']}',
            '{request.form['course_id']}'
        )
    """)
    return redirect(url_for("admin"))


@app.route('/course')
def course():
    return render_template("course.html")


@app.route('/teacher')
def teacher():
    return render_template("teacher.html")


@app.route('/student')
def student():
    return render_template("student.html")


if __name__ == "__main__":
    app.run(debug=True)
