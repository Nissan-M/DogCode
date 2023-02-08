from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)
from setup_db import execute_query


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


@app.route('/register', methods=["POST", "GET"])
def register():
    roles = execute_query("SELECT * FROM role")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]
        execute_query(f"INSERT INTO user (user_email, user_password, role_id) VALUES ('{email}','{password}', '{role}')")
        return render_template("register.html", roles=roles, text = "Registration is complete")
    return render_template("register.html", roles=roles)


@app.route('/new_course')
def new_course():
    pass


@app.route('/add_student')
def add_student():
    pass
