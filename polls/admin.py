from django.contrib import admin
from .models import Question,Choice,respuestas

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(respuestas)
# Register your models here.
