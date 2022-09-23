import http
from pickle import TRUE
from django.http import HttpResponse
from django.template import loader
from .forms import respForm
from .models import Question
from .models import respuestas
from django.shortcuts import render,redirect
from .modules.EncuestasSQL import EncuestasDB
import pandas as pd
import os
import plotly.express as px

def createpost(request):

        if request.method == "POST":
            #if request.respuestas.get('nombre') and request.POST.get('numero'):
            post=respuestas()
            print("guardando?")
            post.nombre= request.POST.get('nombre')
            post.cuenta= request.POST.get('numero')
            post.paterno= "x"
            post.materno= "x"
            post.email= request.POST.get('email')
            post.save()
            print("toy haciendo algo")
            return render(request, 'encuesta01.html')  

        else:
                print ("nostoy haciendo nada")
                return render(request,'polls/index.html')


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
    #TODO: cargar aqui todos los files nescesarios, puede ser usando cahcé, o sessions
    #request.session['dgae']=pd.read_excel(os.path.join(BASE, "modules/files/dgae.xlsx"))
    
    context = {
        'context': "ahi andamos, al 100"
    }
    return HttpResponse(template.render(context, request))

def encuesta01(request):
    template=loader.get_template('polls/encuesta01.html')
    context={
        'contexto' : "ando rolando el contexto" 
    }
    if request.method == "POST":
    
            post=respuestas()
            post.nombre= request.POST.get('nombre')
            print(request.POST.get('nombre'))
            post.cuenta= request.POST.get('cuenta')
            
            post.paterno= "x"
            post.materno= "x"
            post.email= request.POST.get('email')
            post.trabaja=False
            print(request.POST.get('cuenta'))
            print("")
            print("guardando?")
            post.save()
            return HttpResponse(template.render(context,request))

        
    return HttpResponse(template.render(context,request))

def estado(request):
    template=loader.get_template('polls/estado.html')
    #dgae=pd.DataFrame(request.session.get('dgae'))
    #cargando archivo de dgae, en futuras versiones se deve cargar previamente
    BASE = os.path.dirname(os.path.abspath(__file__))
    dgae=pd.read_excel(os.path.join(BASE, "modules/files/dgae.xlsx"))
    conexion = EncuestasDB(dgae)
    
    # Prámetros comunes de gráficas
    fig_params = {'autosize':False,
    'paper_bgcolor':"SlateGray",
    'font':dict(color ='Ivory'),
    'showlegend':False}

    # Gráfica por encuestador
    porEncuestador =  conexion.cuentaPorEncuestador()
    porEncuestador_fig = px.bar(porEncuestador,
                                x='Encuestador',
                                y='Realizadas',
                                color='Encuestador',
                                title='Conteo por Encuestador',
                                labels={"Realizadas": "Conteo"})
    porEncuestador_fig.update_layout(fig_params)
    porEncuestador_fig.update_layout({'width':800,
                                      'height':400})
    porEncuestador_fig = porEncuestador_fig.to_html()
    
    # Gráfica por Mes
    porMes = conexion.cuentaPorMes()
    porMes_fig = px.bar(porMes,
             y='Mes',
             x='realizadas',
             color='Mes',
             title='Conteo por Mes',
             labels={"realizadas": "Conteo"},
             orientation='h')
    porMes_fig.update_layout(fig_params)
    porMes_fig.update_layout({'width':600,
                              'height':1000})
    porMes_fig = porMes_fig.to_html()
    
    # Gráfica por Carrera

    context={
    'porEncuestador' : porEncuestador_fig,
    'porMes': porMes_fig,
    'porCarrera' : conexion.cuentaPorCarrera().to_html()
    }
        
    return HttpResponse(template.render(context,request))

def addresp(request):
    form = respForm
    if request.method == 'POST':
        form = respForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'polls/add-resp.html', context)
    