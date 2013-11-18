from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import base64
from classes import *
def home(req):
    from django.shortcuts import redirect
    return redirect('/static/index.html')

@csrf_exempt
def upload(req):
    print req.FILES['file'].read()

    return HttpResponse('success')


def login(req):
    reqdata = req.POST
    candicate = Candicate(id=reqdata['user_id'])
    interview = Interview(candicate=candicate)
    workspace = WorkSpace()
    workspace.set_interview(interview)
    workspace.create_space()
    res = HttpResponse('success')
    res.set_cookie('userid', candicate.id)
    return res


def get_questions(req):
    if not req.COOKIES.get('userid'):
        return HttpResponse('')
    candicate = Candicate(id=req.COOKIES.get('userid'))
    interview = Interview(candicate=candicate)
    workspace = WorkSpace()
    workspace.set_interview(interview)
    paper = workspace.create_paper()
    resdata = []
    for question in paper:
        question_dict = {}
        question_dict['id'] = question.id
        question_dict['description'] = question.description
        print question.options
        if isinstance(question, SelectQuestion):
            question_dict['options'] = question.options
        resdata.append(question_dict)
    return HttpResponse(json.dumps(resdata), content_type="application/json")


def question(req, question_id):
    print question_id
    #if not req.COOKIES.get('userid'):
    #    return HttpResponse('')
    reqdata = json.loads(req.POST['data'])
    who = req.COOKIES.get('userid')
    print reqdata
    if reqdata['type'] == 'select_qustion':
        new_question = SelectQuestion(
            question_id=question_id,
            description=reqdata['description'],
            options=reqdata['options'],
            correct_answer=reqdata['correct_answer']
        )
    elif reqdata['type'] == 'program_question':
        new_question = ProgramQuestion(
            question_id=question_id,
            description=reqdata['description'],
            testers=req.FILES
        )
    
    candicate = Candicate(id=who)
    interview = Interview(candicate)
    workspace = WorkSpace()
    workspace.set_interview(interview)
    workspace.create_question(new_question)
    return HttpResponse('success')


def answer(req, question_id):
    if req.method == "GET":
        pass
    elif req.method == "POST":
        if not req.COOKIES.get('userid'):
            return HttpResponse('')
        reqdata = json.loads(req.POST['data'])
        who = req.COOKIES.get('userid')
        # answer of select quesion
        print 'data', reqdata
        if reqdata['type'] == 'select_question':
            new_answer = SelectAnswer(
                question_id=question_id,
                type='select_answer',
                selectoptions=reqdata['options']
            )

        # answer of program quesion
        elif reqdata['type'] == 'program_question':
            new_answer = ProgramAnswer(
                question_id=question_id,
                type='program_answer',
                answer_files = req.FILES
                )
        
        # save answer to workspace
        candicate = Candicate(id=who)
        interview = Interview(candicate)
        workspace = WorkSpace()
        workspace.set_interview(interview)
        workspace.save_answer(new_answer)

        return HttpResponse(
            'ok', content_type="application/json")


def complete(req):
    if not req.COOKIES.get('userid'):
        return HttpResponse('')
    who = req.COOKIES.get('userid')
    candicate = Candicate(id=who)
    interview = Interview(candicate)
    workspace = WorkSpace()
    workspace.set_interview(interview)
    report = workspace.get_report()
    return HttpResponse(json.dumps(report),
        content_type="application/json")


def mkquestion4test(req):
    options = [
        {'id':1, 'txt':'AAA'},
        {'id':2, 'txt':'BBB'},
        {'id':3, 'txt':'CCC'},
        {'id':4, 'txt':'DDD'},
        ]
    question = SelectQuestion(
        question_id='q0001',
        description='aaaaaaaaaa?',
        correct_answer=[3],
        options=options
        )
    workspace = WorkSpace()
    workspace.create_question(question)
    return HttpResponse(
        'ok', content_type="application/json")
