import pickle
import re
import getpass
from ucb import main
from student import *
from course import *
from error import *

def welcome():
    WELCOME_MESSAGE = """
-------------------------------------------------------------------------------
                              WELCOME TO BELETEARS
-------------------------------------------------------------------------------"""
    print(WELCOME_MESSAGE)

def home(students):
    HELP_MESSAGE = """
Commands:
    login                   Login your account.
    register                Register a new account.
    help                    Display help message.
    exit/quit/<Control>-D   Exit this system."""

    def help():
        print(HELP_MESSAGE)

    def register(students):
        name = input('Name: ')
        if name in students:
            raise BTError('You have already registered.')
        password = getpass.getpass('Password: ')
        confirm_password = getpass.getpass('Confirm Password: ')
        if password != confirm_password:
            raise BTError('The password does not match the confirm password.')
        student = Student(name, password)
        students[name] = student
        print('Register Successful.')
        save_students(students)
        return student

    def login(students):
        name = input('Name: ')
        password = getpass.getpass('Password: ')
        student = get_student(name, students)
        if student.check_password(password):
            print('Login Successful.')
            return student

    help()
    while True:
        string = input('\n> ')
        if string == '':
            help()
            continue
        cmds = string.split()
        cmd = cmds[0]
        args = cmds[1:]
        if cmd == 'help':
            check_args('help', args, 0, 0)
            help()
        elif cmd == 'login':
            check_args('login', args, 0, 0)
            return login(students)
        elif cmd == 'register':
            check_args('register', args, 0, 0)
            return register(students)
        elif cmd == 'exit' or cmd == 'quit':
            raise EOFError
        else:
            raise BTError('illegal command {0}'.format(cmd))

def read_eval_print_loop(student, students, courses):
    HELP_MESSAGE = """
Commands:
    bid [course] [price]    Bid PRICE on course.
    drop [course]           Drop COURSE, return your bid to your balance.
    info                    Display your current bids and balance.
    list                    List all courses.
    search [keywords...]    List courses that matches the KEYWORDS.
    help                    Display help message.
    logout                  Log out the current user account.
    exit/quit/<Control>-D   Exit this system."""

    def help():
        print(HELP_MESSAGE)

    def bid(student, args, courses):
        course_name = ' '.join(args[:-1])
        price = eval(args[-1])
        course = get_course(course_name, courses)
        print(student.bid(course, price))

    def drop(student, args, courses):
        course_name = ' '.join(args)
        course = get_course(course_name, courses)
        print(student.drop(course))

    def info(student, courses):
        bids_info = student.bids_info(courses)
        print('Name: {0}\nBalance: {1}\nBids: {2}' \
            .format(student.name, student.balance, bids_info))

    def lst(courses):
        for course_name, course in sorted(courses.items(), key=lambda x: x[0]):
            print(course.info())

    def search(args, courses):
        total_result = {}
        for arg in args:
            result = {}
            for course_name, course in courses.items():
                if arg.lower() in course_name:
                    result[course_name] = course
            if result == {}:
                total_result = {}
                break
            else:
                if total_result == {}:
                    total_result = result.copy()
                else:
                    total_result = {course_name: course for course_name, course \
                        in total_result.items() if course_name in result}
        if total_result == {}:
            print('No course matches the keywords.')
        else:
            lst(total_result)

    help()
    while True:
        save_students(students)
        save_courses(courses)
        string = input('\n> ')
        if string == '':
            help()
            continue
        cmds = string.split()
        cmd = cmds[0]
        args = cmds[1:]
        if cmd == 'bid':
            check_args('bid', args, 2)
            bid(student, args, courses)
        elif cmd == 'drop':
            check_args('drop', args, 1)
            drop(student, args, courses)
        elif cmd == 'help':
            check_args('help', args, 0, 0)
            help()
        elif cmd == 'info':
            check_args('info', args, 0, 0)
            info(student, courses)
        elif cmd == 'list':
            check_args('list', args, 0, 0)
            lst(courses)
        elif cmd == 'search':
            check_args('search', args, 1)
            search(args, courses)
        elif cmd == 'logout':
            return True
        elif cmd == 'exit' or cmd == 'quit':
            raise EOFError
        else:
            raise BTError('illegal command {0}'.format(cmd))

def check_args(cmd, args, min, max=None):
    length = len(args)
    if len(args) < min:
        raise BTError('too few arguments for {0}'.format(cmd))
    elif max is not None and length > max:
        raise BTError('too many arguments for {0}'.format(cmd))

def save_students(students):
    f = open('students.pickle', 'wb')
    pickle.dump(students, f)
    f.close()

def save_courses(courses):
    f = open('courses.pickle', 'wb')
    pickle.dump(courses, f)
    f.close()

def load_students():
    f = open('students.pickle', 'rb')
    students = pickle.load(f)
    f.close()
    return students

def load_courses():
    f = open('courses.pickle', 'rb')
    courses = pickle.load(f)
    f.close()
    return courses

@main
def run():
    students = load_students()
    courses = load_courses()
    student = None
    welcome()
    while True:
        try:
            if student is None:
                student = home(students)
            if read_eval_print_loop(student, students, courses):
                student = None
            else:
                break
        except (BTError, SyntaxError, ValueError, RuntimeError) as e:
            print('Error:', e)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
        except EOFError:
            print()
            break
    save_students(students)
    save_courses(courses)
    print('Byebye~')
