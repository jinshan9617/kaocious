from django.http import HttpResponse
from classes import *
def home(req):
    from django.shortcuts import redirect
    return redirect('/static/index.html')

def answer(req, question_id):
    if req.method == "GET":
        pass
    elif req.method == "POST":
        reqdata = req.POST
        # answer of select quesion
        if reqdata['type'] == 'select_question':
            new_answer = SelectAnswer(
                question_id=question_id,
                type=reqdata['type'],
                selectoptions=reqdata['options[]']
            )
        # answer of program quesion
        elif reqdata['type'] == 'program_question':
            new_answer = ProgramAnswer()
        
        # save answer to workspace

        from django.shortcuts import redirect
        return redirect('/static/index.html')

        
