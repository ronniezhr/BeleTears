from course import *
from error import *
import hashlib

DEFAULT_BALANCE = 1000

class Student:
    def __init__(self, name, password, balance=DEFAULT_BALANCE):
        self.name = name
        self.password = hashlib.sha224(password.encode('utf-8')).hexdigest()
        self.balance = balance
        self.bids = {}

    def bid(self, course, price):
        if type(price) is not int:
            raise BTError('Bid must be integer.')
        elif price <= 0:
            raise BTError('Bid must be at least 1.')
        else:
            if course.name in self.bids:
                big_again = input('You have aleady bid for {0}. \
                    Do you want to bid again? (Y/N)'.format(course_name))
                if bid_again:
                    self.drop(course)
                else:
                    return 'You have cancelled the current bid.'
            if price > self.balance:
                raise BTError('Bid exceeds current balance {0}.'.format(self.balance))
            self.balance -= price
            self.bids[course.name.lower()] = price
            course.bid(self, price)
            return 'You have bid {0}.'.format(course.name)

    def drop(self, course):
        course.drop(self)
        del self.bids[course.name.lower()]
        return 'You have dropped {0}.'.format(course.name)

    def check_password(self, password):
        if self.password != hashlib.sha224(password.encode('utf-8')).hexdigest():
            raise BTError('Wrong password!')
        return True

    def bids_info(self, courses):
        if len(self.bids) == 0:
            return 'You have no bid.'
        bids_list = []
        for course_name, price in self.bids.items():
            course = get_course(course_name, courses)
            if course.overbid(self):
                status = '(overbid)'
            else:
                status = '(underbid)'
            item = '\n    Bid {0} for {1} {2}'.format(price, course.name, status)
            bids_list.append(item)
        bids_list.sort()
        return ''.join(bids_list)

def get_student(name, students):
    if name not in students:
        raise BTError('no such student {0}'.format(name))
    return students[name]
