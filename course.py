from error import *

class Course:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.bidders = {}

    def bid(self, student, amount):
        self.bidders[student.name] = amount

    def drop(self, student):
        if student.name not in self.bidders:
            raise BTError('{0} has not bid for {1}'.format(student.name, self.name))
        student.balance += self.bidders[student.name]
        del self.bidders[student.name]

    def overbid(self, student):
        return student.name in self.overbidders

    @property
    def overbidders(self):
        if len(self.bidders) < self.capacity:
            return self.bidders
        else:
            rank = sorted(self.bidders.items(), key=lambda x: x[1], reverse=True)
            return dict(rank[:self.capacity])

    @property
    def lowest_overbidding(self):
        if len(self.bidders) < self.capacity:
            return 0
        else:
            rank = sorted(self.overbidders.values(), reverse=True)
            return rank[self.capacity - 1]

    @property
    def avaiable(self):
        if len(self.bidders) < self.capacity:
            return self.capacity - len(self.bidders)
        else:
            return 0

    def info(self):
        return """{0}:
    Limit: {1}
    Number of Bidders: {2}
    Availble Seats: {3}
    Lowest Bidding: {4}""".format(self.name, self.capacity, len(self.bidders), \
        self.avaiable, self.lowest_overbidding)

def get_course(name, courses):
    if name not in courses:
        raise BTError('no such course {0}'.format(name))
    return courses[name]
