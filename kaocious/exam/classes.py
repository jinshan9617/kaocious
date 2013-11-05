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
            self.interview.candicate.id)
        if not os.path.exists(self.interview_path):
            os.makedirs(self.interview_path)

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
        with open(os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id, "paper"), "w") as fp:
            pickle.dump(paper, fp)

        return paper

    def save_answer(self, answer):
        data = {}
        #filename = os.path.join(self.interview_path, "answer")
        filename = os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id, "answer")
        if os.path.exists(filename):
            with open(filename) as fp:
                data = pickle.load(fp)

        print 'answer', answer.question_id

        data[answer.question_id] = answer
        print data
        with open(filename, 'w') as fp:
            pickle.dump(data, fp)

    def get_question(self, question_id):
        question_file = os.path.join(QUESTION_PATH, question_id)
        return pickle.load(open(question_file))

    def get_report(self):
        answer_file = os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id, "answer")
        answers = [];
        with open(answer_file) as fp:
            answers = pickle.load(fp)
        report = []
        print 'answer : ', type(answers['q0001'])
        for n in answers:
            answer = answers[n]
            if isinstance(answer, SelectAnswer):
                result = answer.equals(self.get_question(answer.question_id))
                report.append({
                    "question_id":answer.question_id,
                    "resualt":result})

        report_file = os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id, "report")
        with open(report_file, 'w') as fp:
            pickle.dump(report, fp)

        return report


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
