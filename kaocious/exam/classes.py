import datetime
import os

class Candicate:
    pass

class Paper:
    pass

class WorkSpace:
    def __init__(self, candicate, paper)
        self.candicate = candicate
        self.paper = paper

class Interview:
    def __init__(self, candicate, paper):
        self.start_at = datetime.datetime.now()
        self.workspace = WorkSpace(candicate,paper)

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
