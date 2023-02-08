DB:

Tables :
    role
    user
    student
    teacher
    course
    courseNo

Relathioships :
    user - role : Many to One
    student - user : One to One
    teacher - user : Oner to One 
    courseNo - course : Many to One
    courseNo - tacher : Many to One
    courseNo - student : Many to Many
    course - student : Many to Many