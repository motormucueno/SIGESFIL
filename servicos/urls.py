from django.urls import path
from .views import home, calculos, legislacao, contraordenacao, lei_geral

urlpatterns = [
    path('', home, name='home'),
    path('calculos/', calculos, name='calculos'),
    path('legislacao/', legislacao, name='legislacao'),
path('legislacao/contraordenacao/', contraordenacao, name='contraordenacao'),
    path('legislacao/lei-geral/', lei_geral, name='lei_geral'),
]
