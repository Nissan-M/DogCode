@app.route('/students', methods=["POST", "GET"])
def students():
    student_db = execute_query("SELECT * FROM student")
    if request.method == "POST":
        student_id = request.form["student_id"].split(" - ")[0]
        student_info = execute_query(f"""
            SELECT
                student.name, student.gender, student.birth_date,
                student.phone, student.address
            FROM student
            WHERE student.student_id={student_id}
            """)
        return render_template("students.html", students=student_db, student_info=student_info)
    return render_template("students.html", students=student_db, student_info="")


@app.route('/student/<student_id>', methods=["POST", "GET"])
def student(student_id):
    student_db = execute_query(f"""
        SELECT
            name, image, gender, birth_date, phone, address, user.email,
            user.password, user.user_id
        FROM student
        JOIN user ON student.user_id=user.user_id
        WHERE student_id={student_id}
        """)

    if request.method == "POST":
        name = request.form["name"]
        image = request.form["image"]
        gender = request.form["gender"]
        birth_date = request.form["birth_date"]
        phone = request.form["phone"]
        address = request.form["address"]
        email = request.form["email"]
        password = request.form["password"]
        execute_query(f"""
            UPDATE student SET
                name='{name}', image='{image}', gender='{gender}', birth_date='{birth_date}',
                phone='{phone}', address='{address}'
            WHERE student_id={student_id}
            """)
        execute_query(f"""
            UPDATE user SET
                email='{email}', password='{password}'
            WHERE user_id={student_db[0][8]}
            """)
        return redirect(url_for("student"))

    return render_template("student.html", student_db=student_db)
