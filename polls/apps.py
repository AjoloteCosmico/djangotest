from re import X
from django.apps import AppConfig
import os
import pandas as pd
from django.shortcuts import render,redirect

class PollsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
    def ready(self):
        BASE = os.path.dirname(os.path.abspath(__file__))
        global dgae,faltantes
        dgae= pd.read_parquet(os.path.join(BASE, "modules/files/dgae.parquet"), engine="fastparquet")
        faltantes=pd.read_excel(os.path.join(BASE,"modules/files/NuevasMuestras2.xlsx"))
        print("base dgae cargada ")