from django.http import HttpResponse

def home(req):
    from django.shortcuts import redirect
    return redirect('/static/index.html')

def answer(req, question_id):
    if req.method == "GET":
        pass
    elif req.method == "POST":
        
