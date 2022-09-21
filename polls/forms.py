from django.forms import ModelForm
from .models import respuestas

class respForm(ModelForm):
    class Meta:
        model = respuestas
        fields = '__all__'