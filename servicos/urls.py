from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculos/', views.calculos, name='calculos'),
    path('legislacao/', views.legislacao, name='legislacao'),
    path('contraordenacao/', views.contraordenacao, name='contraordenacao'),
    path('lei-geral/', views.lei_geral, name='lei_geral'),

]
