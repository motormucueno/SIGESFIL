from django.shortcuts import render, redirect
from django.db import transaction
from django.contrib import messages
from django.db.models import Count, Q

from trabalhadores.models import Trabalhador
from .models import Empresa
from .forms import EmpresaForm, TrabalhadorFormSet

from django.http import JsonResponse
from trabalhadores.models import Trabalhador, Incapacidade
from .models import Empresa, ContraOrdenacao  # Ajuste conforme o nome do seu modelo de contra-ordenações
from django.template.loader import render_to_string



# Listas para selecção no template
lista_incapacidades = Incapacidade.objects.all()

# =========================
# AJAX: CONTRA-ORDENAÇÕES
# =========================
def ajax_contraordenacoes(request):
    empresa_id = request.GET.get("empresa_id")
    contra_list = []

    if empresa_id:
        empresa = Empresa.objects.filter(id=empresa_id).first()
        if empresa:
            contra_list = empresa.contra_ordenacoes.all()  # ajuste conforme seu related_name

    html = render_to_string("empresas/partials/contraordenacoes_list.html", {"contraordenacoes": contra_list})
    return JsonResponse(html, safe=False)


# =========================
# AJAX: TRABALHADORES
# =========================
def ajax_trabalhadores(request):
    empresa_id = request.GET.get("empresa_id")
    trabalhadores = []

    if empresa_id:
        empresa = Empresa.objects.filter(id=empresa_id).first()
        if empresa:
            trabalhadores = empresa.trabalhadores.all()  # ajuste conforme seu related_name

    html = render_to_string("empresas/partials/trabalhadores_list.html", {"trabalhadores": trabalhadores})
    return JsonResponse(html, safe=False)



# =====================================================
# VIEW PRINCIPAL (Dashboard + Abas)
# =====================================================
@transaction.atomic
def empresa_view(request):

    # ======================
    # POST – CADASTRO
    # ======================
    if request.method == "POST":
        empresa_form = EmpresaForm(request.POST, request.FILES)
        trabalhador_formset = TrabalhadorFormSet(
            request.POST,
            prefix="trabalhadores"
        )

        if empresa_form.is_valid() and trabalhador_formset.is_valid():
            empresa = empresa_form.save()

            trabalhadores = trabalhador_formset.save(commit=False)
            for trabalhador in trabalhadores:
                trabalhador.empresa = empresa
                trabalhador.save()


            messages.success(request, "Empresa cadastrada com sucesso.")
            return redirect("empresa_view")

        else:
            messages.error(request, "Existem erros no formulário.")

    # ======================
    # GET – FORMULÁRIOS
    # ======================
    else:
        empresa_form = EmpresaForm()
        trabalhador_formset = TrabalhadorFormSet(prefix="trabalhadores")

    # ======================
    # QUERYSET BASE
    # ======================
    empresas = (
        Empresa.objects
        .annotate(
            total_trabalhadores=Count("trabalhadores", distinct=True),
            total_contraordenacoes=Count("contra_ordenacoes", distinct=True)
        )
        .order_by("-data_inspeccao")
    )
    sectores = (
        Empresa.objects
        .values("sector__nome")
        .annotate(
            total_inspecoes=Count("id", distinct=True),
            total_contraordenacoes=Count("contra_ordenacoes", distinct=True)
        )
        .order_by("sector__nome")
    )

    # ======================
    # PESQUISA SIMPLES
    # ======================
    data_inicio = request.GET.get("data_inicio")
    data_fim = request.GET.get("data_fim")
    nome = request.GET.get("nome")
    nif = request.GET.get("nif")

    if data_inicio:
        empresas = empresas.filter(data_inspeccao__gte=data_inicio)

    if data_fim:
        empresas = empresas.filter(data_inspeccao__lte=data_fim)

    if nome:
        empresas = empresas.filter(nome__icontains=nome)

    if nif:
        empresas = empresas.filter(nif__icontains=nif)

    # ======================
    # PESQUISA AVANÇADA
    # ======================
    propriedade = request.GET.get("propriedade")
    sector = request.GET.get("sector")
    tipo_inspeccao = request.GET.get("tipo_inspeccao")
    provincia = request.GET.get("provincia")
    municipio = request.GET.get("municipio")
    distrito = request.GET.get("distrito")
    bairro = request.GET.get("bairro")
    rua = request.GET.get("rua")
    observacao_entidade_empregadora = request.GET.get("observacao_entidade_empregadora")
    conclusao = request.GET.get("conclusao")

    if propriedade:
        empresas = empresas.filter(propriedade_id=propriedade)

    if sector:
        empresas = empresas.filter(sector_id=sector)

    if tipo_inspeccao:
        empresas = empresas.filter(tipo_inspeccao_id=tipo_inspeccao)

    if provincia:
        empresas = empresas.filter(provincia_id=provincia)

    if municipio:
        empresas = empresas.filter(municipio__icontains=municipio)

    if distrito:
        empresas = empresas.filter(distrito__icontains=distrito)

    if bairro:
        empresas = empresas.filter(bairro__icontains=bairro)

    if rua:
        empresas = empresas.filter(rua__icontains=rua)

    if observacao_entidade_empregadora:
        empresas = empresas.filter(observacao__icontains=observacao_entidade_empregadora)

    if conclusao:
        empresas = empresas.filter(conclusao__icontains=conclusao)

    # =================================================
    # DASHBOARD DINÂMICO (EM FUNÇÃO DA PESQUISA)
    # =================================================
    total_empresas = empresas.count()

    total_trabalhadores = (
        Trabalhador.objects
        .filter(empresa__in=empresas)
        .count()
    )

    total_contraordenacoes = (
        empresas
        .aggregate(
            total=Count("contra_ordenacoes", distinct=True)
        )["total"] or 0
    )

    context = {
        "empresa_form": empresa_form,
        "trabalhador_formset": trabalhador_formset,
        "empresas": empresas, "sectores":sectores, "incapacidades":lista_incapacidades,

        # Dashboard
        "total_empresas": total_empresas,
        "total_trabalhadores": total_trabalhadores,
        "total_contraordenacoes": total_contraordenacoes,
    }

    return render(request, "empresas/base.html", context)

