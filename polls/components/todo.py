from django_unicorn.components import UnicornView
from django import forms


class TodoView(UnicornView):

    def busca(self):
        print("buscando")