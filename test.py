def convert_pic():
    files = "./images/avatar_male.jpg"
    picture = open(files, "rb").read()
    return picture


print(convert_pic())