yourapp/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── database.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   └── ...
│   └── static/
│       ├── css/
│       ├── js/
│       ├── images/
│       └── ...
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── ...
├── config.py
├── run.py
└── README.md


data structure : 

    tables : 

        courses                     :   id, name, description

        users                       :   id, role, email, password
        
        students                    :   id, user_id, name, image, birth_date, phone, address

        teachers                    :   id, user_id, name, image, birth_date, phone, address

        active_courses              :   id, teacher_id, start_date, end_date

        classes                     :   id, active_course_id, student_id


    relationships : 

        students - users            :   one to many

        teachers - users            :   one to many

        teachers - active-courses   :   one to many

        courses - active-courses    :   one to many

        active_courses - classes    :   one to many

        students - classes          :   many to many


    classes : CRUD

        USER                        :   ID, EMAIL, PASSWORD, ROLE
            def get data
            def change email
            def change password
            def change role
            def delete user

        USERS                       :   GROUP BY ID {ID:[EMAIL, PASSWORD, ROLE]}
            def get all
            def group by id

        TEACHER(USER)               :   ID, USER_ID, NAME, USER{EMAIL:PASSWORD}, IMAGE, BIRTH DATE, AGE, PHONE, ADDRESS, COURSES
            def get teacher data
            def get email and password
            def change name
            def change image
            def change birth_date
            def age
            def change phone
            def change address
            def get courses
            def get all ids

        STUDENT(USER)               :   ID, USER_ID, NAME, EMAIL, PASSWORD, IMAGE, BIRTH DATE, AGE, PHONE, ADDRESS, COURSES(DICT - COURSE : TEACHER_NAME)
            def get teacher data
            def get email and password
            def change name
            def change image
            def change birth_date
            def age
            def change phone
            def change address
            def get courses
            def get all ids

        course                      :   INSERT, UPDATE, DELETE, SHOW ALL, SHOW ONE BY ID

        active_course               :   INSERT, UPDATE, DELETE, SHOW ALL, SHOW ALL BY COURSE_ID

        class                       :   INSERT, UPDATE, DELETE, SHOW ALL, SHOW ALL BY ACTIVE_COURSE_ID



app routes : 

    admin
        user_manipulate             :   add, update, dalete     user + student / teacher
        course_manipulate           :   add, update, delete
        active_course_manipulate    :   add, update, delete     active_course + teacher
        class_manipulate            :   add, update, delete     class + active_course + teacher + student


connections :

    home page :
        login : after login
            admin_workplace : """can manipulate all data """
                add course : name, description
                update course
                delete course

                add user : email, password, role
                update user
                delete user

                add active course : teacher, course, duration
                update active course
                delete active course

                add student to active course student : student, active course
                update active course student
                delete active course student

            teacher_workplace
            student_work_place
        course_list
            course_card
        teacher_list
            teacher_card
        student_list
            student_card
    

improvments : 

    admin - control Panel
        html, css
        routes

todo : 

    course list
        html, css, route

    profile for courses
        html, css, route
    
    teacher list
        html, css, route
    
    profile for teacher
        html, css, route

    student list
        html, css, route

    profile for student
        html, css, route
