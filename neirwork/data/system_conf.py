with open('neirwork/data/course.json') as file:
    courses = file.readlines()

SYS_MSG = f"""Ты робот который помогает человеку выбрать курсы по программированию. отвечай четко и ясно. 
Используй только русский язык"""