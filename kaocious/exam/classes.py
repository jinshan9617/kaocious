import datetime
import os
import cPickle as pickle

INTERVIEW_PATH = '/home/jinshan/exam/interview/'
QUESTION_PATH = '/home/jinshan/exam/questions/'

class Candicate:
    def __init__(self, id):
        self.id = id

class Paper:
    pass

class WorkSpace:

    def __init__(self):
        pass

    def set_interview(self, interview):
        self.interview = interview

    def create_space(self):
        self.interview_path = os.path.join(INTERVIEW_PATH,
            self.candicate.id)
        if os.path.exists(self.interview_path):
            os.makedirs(interview_path)

    def create_question(self, question):
        print question.id
        question_file = os.path.join(QUESTION_PATH, question.id)
        print question_file
        with open(question_file, "w") as fp:
            pickle.dump(question, fp)

    def create_paper(self):
        paper = []
        for _, _, question_files in os.walk(QUESTION_PATH):
            for qfile in question_files:
                paper.append(pickle.load(
                    open(os.path.join(QUESTION_PATH, qfile))))
        #with open(os.path.join(self.interview_path, "paper"), "w") as fp:
        with open(os.path.join('/home/jinshan/exam/interview/0001', "paper"), "w") as fp:
            pickle.dump(paper, fp)

        return paper

    def save_answer(self, answer):
        data = {}
        #filename = os.path.join(self.interview_path, "answer")
        filename = os.path.join("/home/jinshan/exam/interview/0001", "answer")
        if os.path.exists(filename):
            with open(filename) as fp:
                data = pickle.load(fp)

        data[answer.question_id] = answer
        with open(filename, 'w') as fp:
            pickle.dump(data, fp)

    def get_question(self, question_id):
        question_file = os.path.join(QUESTION_PATH, question_id)
        return pickle.load(open(question_file))


class Interview:
    def __init__(self, candicate):
        now = datetime.datetime.now()
        self.start_at = str(now)
        self.candicate = candicate

class SelectQuestion:
    
    def __init__(self, question_id, description, options, correct_answer):
        self.id = question_id
        self.description = description
        self.correct_answer = correct_answer
        self.options = options


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

    def equals(self, question):
        return sorted(self.selectoptions)==sorted(question.correct_answer)

class ProgramAnswer(Answer):
    
    def __init__(self, question_id, type, answer_file):
        pass

    def equals(self, answer):
        pass
