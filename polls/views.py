from ctypes import sizeof
import http
from pickle import TRUE
from re import T
from turtle import width
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
import plotly.graph_objects as go
import polls.apps
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
    #BASE = os.path.dirname(os.path.abspath(__file__))
    template = loader.get_template('polls/index.html')

    print("index: yo tengo tengo el anillo" )
    context = {
        'context': "ahi andamos, al 100"
    }
    return HttpResponse(template.render(context, request))
def consutarNumero(request):
    template = loader.get_template('polls/consultarNumero.html')

    print("consulta: yo tengo tengo el anillo" )
    context = {
        'enc12': True
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
 
    #Obteniendo archivos previamete cargados
    dgae=polls.apps.dgae
    faltan=polls.apps.faltantes
    #Estableciendo conexion a la base mysql
    conexion = EncuestasDB(dgae)
    
    # Prámetros comunes de gráficas
    fig_params = {'autosize':False,
    'paper_bgcolor':'rgba(0,0,0,0)',
    'plot_bgcolor':'rgba(0,0,0,0)',
    'font':dict(
        size=19,
        color ='rgb(200,200,200)'),
        
    'showlegend':False}

    # Gráfica por encuestador
    porEncuestador =  conexion.cuentaPorEncuestador()
    porEncuestador_fig = px.bar(porEncuestador,
                                x='Encuestador',
                                y='Realizadas',
                                color='Encuestador',
                                title='Conteo por Encuestador',
                                labels={"Realizadas": "Encuestas Realizadas"})
    porEncuestador_fig.update_layout(fig_params)
    porEncuestador_fig.update_layout({'width':1000,
                                      'height':600})
    porEncuestador_fig = porEncuestador_fig.to_html()
    
    # Gráfica por Mes
    porMes = conexion.cuentaPorMes()
    porMes_fig = px.bar(porMes,
             y='Mes',
             x='realizadas',
             color='Mes',
             title='Conteo por Mes',
             labels={"realizadas": "Encuestas realizadas"},
             orientation='h')
    porMes_fig.update_layout(fig_params)
    porMes_fig.update_layout({'width':1000,
                              'height':1000})
    porMes_fig = porMes_fig.to_html()
    
    # Gráfica por Carrera
    porCarrera = conexion.cuentaPorCarrera()
    porCarrera=porCarrera.merge(faltan[["ClaveCarrera","ClavePlantel","Faltan"]],on=["ClaveCarrera","ClavePlantel"])
    porCarrera_fig = go.Figure(
        data = [go.Table(
            header = dict(
                    values = ['Plantel', 'Carrera', 'Internet', 'Telefonicas','Faltan'], 
                    fill_color='#0A0A0A', 
                    align='left',
                    font=dict(color='rgb(190,190,190)',size=20)),
            cells = dict(
                    values=[ porCarrera.Plantel, porCarrera.Carrera, porCarrera.Internet, porCarrera.Telefonicas, porCarrera.Faltan], 
                    align='left', 
                    fill_color= ['rgba(0,0,0,0)','rgba(0,0,0,0)','rgba(0,0,0,0)','rgba(0,0,0,0)','rgba(50,15,14,0.5)'],
                    #line_color=['rgba(0,0,0,0)','rgba(0,0,0,0)','rgba(0,0,0,0)','rgba(0,0,0,0)','rgba(100,0,0,30)'],
                    height=25,
                    font=dict(color='rgb(190,190,190)',size=18)))],
            layout_title_text ='Conteo por Carrera',
            layout_title_font = go.layout.title.Font(color = 'rgb(200,200,200)',family='Georgia',size=25)
            )

    fig_params_c = {'autosize':False,
                  'width':900,
                  'height': 900,
                  'paper_bgcolor':"rgba(0,0,0,0)",
                  'margin' : dict(l=30, r=30, t=80, b=50)}
    porCarrera_fig.update_layout(fig_params_c)
    porCarrera_fig = porCarrera_fig.to_html()

    context={
    'porEncuestador' : porEncuestador_fig,
    'porMes': porMes_fig,
    'porCarrera': porCarrera_fig
    }
        
    return HttpResponse(template.render(context,request))





def estado12(request):
    template=loader.get_template('polls/estado12.html')
    #dgae=pd.DataFrame(request.session.get('dgae'))
    #cargando archivo de dgae, en futuras versiones se deve cargar previamente
    dgae=polls.apps.dgae
    #dgae=pd.read_excel(os.path.join(BASE, "modules/files/dgae.xlsx"))
    conexion = EncuestasDB(dgae)
    
    # Prámetros comunes de gráficas
    fig_params = {'autosize':False,
    'paper_bgcolor':'rgba(0,0,0,0)',
    'plot_bgcolor':'rgba(0,0,0,0)',
    'font':dict(
        size=19,
        color ='rgb(200,200,200)'),
        
    'showlegend':False}

    # Gráfica por encuestador
    porEncuestador =  conexion.cuentaPorEncuestador2012()
    porEncuestador_fig = px.bar(porEncuestador,
                                x='Encuestador',
                                y='Realizadas',
                                color='Encuestador',
                                title='Conteo por Encuestador',
                                labels={"Realizadas": "Encuestas Realizadas"})
    porEncuestador_fig.update_layout(fig_params)
    porEncuestador_fig.update_layout({'width':1000,
                                      'height':600})
    porEncuestador_fig = porEncuestador_fig.to_html()

      # Gráfica por Mes
    porMes = conexion.cuentaPorMes2012()
    porMes_fig = px.bar(porMes,
             y='Mes',
             x='realizadas',
             color='Mes',
             title='Conteo por Mes',
             labels={"realizadas": "Encuestas realizadas"},
             orientation='h')
    porMes_fig.update_layout(fig_params)
    porMes_fig.update_layout({'width':1000,
                              'height':1000})
    porMes_fig = porMes_fig.to_html()
    context={
    'porEncuestador' : porEncuestador_fig,
    'porMes': porMes_fig,
    #'porCarrera': porCarrera_fig
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
    