import http
from django.http import HttpResponse
from django.template import loader
from .models import Question
from .models import respuestas
from django.shortcuts import render

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def encuesta01(request):
    template=loader.get_template('polls/encuesta01.html')
    context={
        'contexto' : "ando rolando el contexto" 
    }
    return HttpResponse(template.render(context,request))


def createpost(request):
        if request.method == 'POST':
            if request.POST.get('nombre') and request.POST.get('numero'):
                post=respuestas()
                post.nombre= request.POST.get('nombre')
                post.cuenta= request.POST.get('numero')
                post.save()
                
                return render(request, 'polls/index.html')  

        else:
                return render(request,'polls/index.html')

