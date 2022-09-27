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
        global dgae
        dgae= pd.read_parquet(os.path.join(BASE, "modules/files/dgae.parquet"), engine="fastparquet")
        print("base dgae cargada putos")