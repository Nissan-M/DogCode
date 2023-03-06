# NEED IMPROVMENTS :
# @app.route('/profile', methods=["GET", "POST"])
# def profile():
#     user_id = int(session["id"])
#     stud_id = execute_query(f"""
#         SELECT student_id FROM student
#         JOIN user ON student.user_id = user.user_id
#         WHERE student.user_id={user_id}
#         """)

#     if request.method == "POST":
#         name = request.form["name"]
#         image = request.files["image"]
#         blob_image = base64.b64encode(image.read())
#         print(blob_image)
#         gender = request.form["gender"]
#         birth_date = request.form["date"]
#         phone = request.form["phone"]
#         address = request.form["address"]
#         execute_query(f"""
#             UPDATE student SET
#                 name = ?,
#                 image = ?,
#                 gender = ?,
#                 birth_date = ?,
#                 phone = ?,
#                 address = ?
#             WHERE user_id = {user_id}
#         """, params=(name, blob_image, gender, birth_date, phone, address))

#         return redirect(url_for("profile"))

    # student_info = execute_query(f"""
    #     SELECT * FROM user
    #     JOIN student ON user.user_id = student.user_id
    #     WHERE user.user_id = {user_id}
    # """)

    # return render_template("profile.html", student_info=student_info)



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




@app.route('/teacher_work_place', methods=["GET", "POST"])
def teacher_work_place():
    user_id = session["id"]

    teacher_courses_data_query = f"""
        SELECT
            active_course.ac_id,
            course.name,
            teacher.name
        FROM active_course
        JOIN course
            ON active_course.course_id = course.course_id
        JOIN teacher
            ON active_course.teacher_id = teacher.teacher_id
        WHERE teacher.user_id = {user_id}
        """
    teacher_courses_data = execute_query(teacher_courses_data_query)

    if request.method == "POST":
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

        return render_template("teacher-work-place.html",
                               students_grade=students_grade,
                               teacher_courses_data=teacher_courses_data)

    return render_template("teacher-work-place.html",
                           teacher_courses_data=teacher_courses_data)


@app.route('/teacher_attendance', methods=["POST"])
def teacher_attendance():
    return redirect(url_for(teacher_work_place))


@app.route('/add_student_grade', methods=["POST"])
def add_student_grade():
    course_id = request.form["course_id"]
    grade = request.form["grade"]

    update_grade_query = f"""
        UPDATE active_course_student SET
            grade = '{grade}'
        WHERE active_course_student.acs_id = {course_id}
        """
    execute_query(update_grade_query)

    return redirect(request.referrer)