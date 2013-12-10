import datetime
import os
import shutil
import tempfile
import cPickle as pickle
from subprocess import call

INTERVIEW_PATH = '/home/jinshan/exam/interview/'
QUESTION_PATH = '/home/jinshan/exam/questions/'
TESTER_PATH = '/home/jinshan/exam/tester/'

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
        
        question_path = os.path.join(QUESTION_PATH, question.id)
        if not os.path.isdir(question_path):
            os.makedirs(question_path)
        
        if isinstance(question, ProgramQuestion):
            testers = question.testers
            tester_path = os.path.join(question_path, "testers")
            if not os.path.isdir(tester_path):
                os.makedirs(tester_path)
            for tester in testers:
                code_path = os.path.join(tester_path, testers[tester].name)
                with open(code_path, 'w') as code:
                    code.write(testers[tester].read())
                    
            question.testers = './testers'
        print question_path
        with open(os.path.join(question_path, 'question'), "w") as fp:
            pickle.dump(question, fp)

    def create_paper(self):
        paper = []
        questions = os.listdir(QUESTION_PATH)
        for qfile in questions:
            paper.append(pickle.load(
                open(os.path.join(QUESTION_PATH, qfile, 'question'))))
        #with open(os.path.join(self.interview_path, "paper"), "w") as fp:
        with open(os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id, "paper"), "w") as fp:
            pickle.dump(paper, fp)

        return paper

    def save_answer(self, answer):
        answer_path = os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id,
            'answer', answer.question_id)
        if not os.path.exists(answer_path):
            os.makedirs(answer_path)
        filename = os.path.join(answer_path, 'answer')
        history_path = os.path.join(answer_path, 'history')
        if not os.path.isdir(history_path):
            os.makedirs(history_path)
        filelist = os.listdir(answer_path)
        filelist.remove('history')
        if len(filelist):
            print filelist
            old_file = os.path.join(history_path, str(datetime.datetime.now()))
            os.makedirs(old_file)
            for oflie in filelist:
                shutil.move(os.path.join(answer_path, oflie),
                    os.path.join(old_file, oflie))

        if answer.type == "program_answer":
            program_dir = os.path.join(answer_path, 'code')

            if not os.path.isdir(program_dir):
                os.makedirs(program_dir)
            files = answer.answer_files
            for answer_file in files:
                file_path = os.path.join(program_dir, files[answer_file].name)
                with open(file_path, 'w') as code:
                    code.write(files[answer_file].read())
            answer.answer_files = './code'
        
        with open(filename, "w") as fp:
            pickle.dump(answer, fp)

    def get_question(self, question_id):
        question_file = os.path.join(QUESTION_PATH, question_id, 'question')
        return pickle.load(open(question_file))

    def get_report(self):
        answer_path = os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id, "answer")
        report = []

        paperfile = os.path.join(
            INTERVIEW_PATH, self.interview.candicate.id, "paper")
        with open(paperfile) as fp:
            paper = pickle.load(fp)

        for question in paper:
            answerfile = os.path.join(answer_path, question.id, 'answer')
            if not os.path.exists(answerfile):
                report.append({
                    "question_id":question.id,
                    "result":"answer is empty!"})
                continue
            with open(answerfile) as fp:
                answer = pickle.load(fp)
            if isinstance(answer, SelectAnswer):
                result = answer.equals(question)
                report.append({
                    "question_id":answer.question_id,
                    "result":result})
            elif isinstance(answer, ProgramAnswer):
                result = answer.equals(question, self.interview)
                report.append({
                    "question_id":answer.question_id,
                    "result":result})

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
        self.type = "select_question"
        self.description = description
        self.correct_answer = correct_answer
        self.options = options


class ProgramQuestion:
    
    def __init__(self, question_id, description, testers):
        self.id = question_id
        self.type = "program_question"
        self.description = description
        self.testers=testers

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
        correct_answer = [ int(answer) for answer in question.correct_answer ]

        return sorted(self.selectoptions)==sorted(correct_answer)

class ProgramAnswer(Answer):
    
    def __init__(self, question_id, type, answer_files):
        self.question_id = question_id
        self.type = type
        self.answer_files = answer_files

    def equals(self, question, interview):
        tester_path = os.path.join(QUESTION_PATH, self.question_id, 'testers')
        code_path = os.path.join(INTERVIEW_PATH,
            interview.candicate.id, self.question_id, 'code')
        tmp4test_path = tempfile.mkdtemp(prefix="examtest-")
        code_files = os.listdir(code_path)
        
        for code in code_files:
            shutil.copy(os.path.join(
                code_path, code), os.path.join(tmp4test_path, code))
        
        test_files = os.listdir(tester_path)

        for tester in test_files:
            shutil.copy(os.path.join(
                tester_path, tester), os.path.join(tmp4test_path, tester))

        cmd = " ".join(["cd", tmp4test_path, "&&", "nosetests"])
        result = call(cmd)
        return result
