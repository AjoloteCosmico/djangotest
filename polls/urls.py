from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
     #ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('encuesta01', views.encuesta01, name='encuesta01'),
    path('estado', views.estado, name='estado'),
    path('estado12', views.estado12, name='estado12'),
    path('consultarNumero', views.consutarNumero, name='consultarNumero'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    path('add-resp', views.addresp, name="add-resp")
    ]

    