from unittest.util import _MAX_LENGTH
from django.forms import ModelForm
from .models import respuestas
from django.forms import Form
from django import forms
class respForm(ModelForm):
    class Meta:
        model = respuestas
        fields = '__all__'

class buscarNum(Form):
    cuenta=forms.CharField( widget=forms.TextInput(attrs={'class': 'outlinenone',
                                                        'placeholder':"Ingresa un numero de cuenta",                    
                                                         }),
                                                   max_length=20)
class actualizar(Form):
    cuenta=forms.CharField( widget=forms.TextInput(attrs={'class': 'outlinenone',
                                                        'placeholder':"Ingresa un numero de cuenta",                    
                                                         }),
                                                   max_length=20)