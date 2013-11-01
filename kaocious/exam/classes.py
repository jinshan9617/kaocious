import datetime
import os
import cPickle as pickle

INTERVIEW_PATH = '/home/jinshan/tmp/interview/'

class Candicate:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Paper:
    pass

class WorkSpace:

    def __init__(self, candicate):
        self.candicate = candicate

    def create_interview(interview):
        self.interview = interview
        self.interview_path = os.path.join(INTERVIEW_PATH,
            '-'.join(self.candicate.name, self.interview.start_at))
        os.makedirs(interview_path)

    def save_answer(self, answer):
        data = {}
        #filename = os.path.join(self.interview_path, "answer")
        filename = os.path.join("/home/jinshan/tmp/interview/0001", "answer")
        if os.path.exists(filename):
            with open(filename) as fp:
                data = pickle.load(fp)

        data[answer.question_id] = answer
        with open(filename, 'w') as fp:
            pickle.dump(data, fp)


class Interview:
    def __init__(self, candicate):
        now = datetime.datetime.now()
        self.start_at = str(now)
        this.candicate = candicate

class Question:
    pass

class Answer:
    def __init__(self, question_id):
        self.question_id = question_id

class Tester:
    pass

class SelectAnswer(Answer):
    def __init__(self, question_id, type, selectoptions):
        self.question_id = question_id
        self.type = type
        self.selectoptions = selectoptions
