from main import *

DEFAULT_PASSWORD = '123456'
DEFAULT_CAPACITY = 1

def add_random(item, amount):
    for i in range(amount):
        if item == 'student':
            name = 'Student-' + str(i)
            students[name] = Student(name, DEFAULT_PASSWORD)
        elif item == 'course':
            name = 'Course-' + str(i)
            courses[name.lower()] = Course(name, DEFAULT_CAPACITY)

students = {
    'Ronnie': Student('Ronnie', 'iloveluyi'),
    'Simon': Student('Simon', 'ilovejiaxi'),
    'Rita': Student('Rita', 'iloveprogramming'),
    'Tim': Student('Tim', 'ilovealice'),
}
add_random('student', 1000)

courses = {
    'cs 61a': Course('CS 61A', 2),
    'cs 61b': Course('CS 61B', 3),
    'cs 61c': Course('CS 61C', 4),
}
add_random('course', 1000)

save_students(students)
save_courses(courses)