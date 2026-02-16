
from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.db.models import Count, Q

from django.http import JsonResponse
from django.template.loader import render_to_string
from empresas.models import ContraOrdenacao


def home(request):
    return render(request, 'servicos/home.html')

def calculos(request):
    return render(request, 'servicos/calculos.html')

def legislacao(request):
    #query = request.GET.get('q')
    #leis = Legislacao.objects.all()

    #if query:
        #leis = leis.filter(titulo__icontains=query)
    leis = ["A", "B", "C"]

    return render(request, 'servicos/legislacao.html', {'leis': leis})

# NOVAS VIEWS
def contraordenacao(request):
    termo = request.GET.get('q', '')
    resultados = []

    if termo:
        resultados = ContraOrdenacao.objects.filter(
            nome__icontains=termo
        ).order_by('artigo')
    context = {
        'termo': termo,
        'resultados': resultados
    }
    return render(request, 'servicos/contraordenacao.html', context)


def lei_geral(request):
    # Aqui podes buscar artigos da Lei Geral do Trabalho
    #artigos = Legislacao.objects.filter(tipo='lei_geral')
    artigos = "Artigos"
    return render(request, 'servicos/lei_geral.html', {'artigos': artigos})



