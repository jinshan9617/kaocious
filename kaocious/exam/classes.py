import datetime
import os

INTERVIEW_PATH = '/srv/interview/'

class Candicate:
    def __init__(self, id):
        self.id = id
    pass

class Paper:
    pass

class WorkSpace:
    def __init__(self, candicate, interview):
        self.candicate = candicate
        self.interview = interview

    def create_interview():
        interview_path = os.path.join(INTERVIEW_PATH,
            '-'.join(self.candicate.name, self.interview.start_at))
        os.makedirs(interview_path)
        

class Interview:
    def __init__(self, candicate):
        now = datetime.datetime.now()
        self.start_at = str(now)

class Question:
    pass

class Answer:
    def __init__(self, question_id):
        self.question_id = question_id

class Tester:
    pass

class SelectAnswer(Answer):
    def __init__(self, question_id, type, selectoptions):
        self.type = type
        self.selectoptions = selectoptions
