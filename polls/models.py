from django.db import models
import datetime
from django.utils import timezone
#Modelos de Prueba los vi en un tutorial xd
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
       return self.choice_text

#Creando los modelos que si usaremos (preeliminares)
class respuestas(models.Model):
    #Datos personales
    cuenta=models.CharField(max_length=9)
    email=models.CharField(max_length=50,default="no ingreso correo")
    nombre=models.CharField(max_length=50)
    materno=models.CharField(max_length=50)
    paterno=models.CharField(max_length=50)
    carrera=models.CharField(max_length=3,default="000")
    #primer reactivo de la encuesta
    trabaja=models.BooleanField()


