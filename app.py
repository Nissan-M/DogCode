from flask import Flask, render_template, redirect, url_for, request
import crud

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'thisisasecretkey'


# @app.before_request
# def before_request_func():
#     return render_template("login.html")


@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        indeficate = crud.login(email=request.form["email"],
                                password=request.form["password"])
    return render_template("login.html")


@app.route('/guest')
def guest():
    return render_template("guest.html")


@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/admin')
def admin():
    roles = crud.show_all("role")
    teachers = crud.show_all(table="teacher")
    courses = crud.show_all(table="course")
    active_courses = crud.show_all(table="active_course")
    students = crud.show_all(table="student")
    
    return render_template("admin.html", roles=roles, teachers=teachers,
                           courses=courses, active_courses=active_courses,
                           students=students,)


@app.route('/new_user', methods=["POST"])
def register():
    crud.new_user(email=request.form["email"],
                  password=request.form["password"],
                  role=request.form["role"])

    return redirect(url_for("admin"))


@app.route('/new_course', methods=["POST"])
def create_course():
    crud.new_course(name=request.form['name'],
                    desc=request.form['desc'])

    return redirect(url_for("admin"))


@app.route('/add_active_course', methods=["POST"])
def teacher_course():
    crud.add_active_course(course_id=request.form['course_id'],
                           teacher_id=request.form['teacher_id'],
                           start_date=request.form['start_date'],
                           end_date=request.form['end_date'])

    return redirect(url_for("admin"))


@app.route('/add_student_to_active_course', methods=["POST"])
def method_name():
    crud.add_active_course_student(active_course_id=request.form['student_id'],
                                   student_id=request.form['course_id'])

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
