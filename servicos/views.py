from django.shortcuts import render
from empresas.models import ContraOrdenacao
from servicos.models import Artigo
import re
from django.db.models import Q
from servicos.models import Capitulo


def home(request):
    return render(request, 'servicos/home.html')

def calculos(request):
    return render(request, 'servicos/calculos.html')

def legislacao(request):
    leis = ["A", "B", "C"]
    return render(request, 'servicos/legislacao.html', {'leis': leis})

# -------------------
# CONTRA-ORDENAÇÃO
# -------------------
def contraordenacao(request):
    termo = request.GET.get('q', '').strip()
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

# -------------------
# LEI GERAL DO TRABALHO
# -------------------
def limpar_cabecalhos(texto):
    # Remove LEI GERAL DO TRABALHO - LEI N.º 12/2023
    texto = re.sub(
        r'\d*\s*Lei\s+Geral\s+do\s+Trabalho\s*-\s*Lei\s+N[.º°o]*\s*\d+/\d+',
        '',
        texto,
        flags=re.IGNORECASE
    )

    # Remove Ministério da Administração Pública, Trabalho e Segurança Social
    texto = re.sub(
        r'Minist[eé]rio\s+da\s+Administra[cç][aã]o\s+P[úu]blica,\s+Trabalho\s+e\s+Seguran[cç]a\s+Social\d*',
        '',
        texto,
        flags=re.IGNORECASE
    )

    return texto

def organizar_conteudo(texto):
    if not texto:
        return []

    texto = limpar_cabecalhos(texto)

    # Normaliza espaços
    texto = re.sub(r'\s+', ' ', texto).strip()

    # 1️⃣ Separar números (1., 2., 3.)
    texto = re.sub(r'(?<!\S)(\d+\.)\s*', r'\n\1 ', texto)

    # 2️⃣ Separar alíneas após ":" (início da enumeração)
    texto = re.sub(r':\s*([a-z]{1,2}\))', r':\n\1 ', texto, flags=re.IGNORECASE)

    # 3️⃣ Separar alíneas seguintes após ";"
    texto = re.sub(r';\s*([a-z]{1,2}\))', r';\n\1 ', texto, flags=re.IGNORECASE)

    # Divide em parágrafos
    paragrafos = [p.strip() for p in texto.split('\n') if p.strip()]

    return paragrafos




def lei_geral(request):
    termo = request.GET.get("q", "").strip()

    artigos = Artigo.objects.all().select_related(
        "capitulo", "seccao", "subseccao"
    ).order_by(
        "capitulo__id", "seccao__id", "subseccao__id", "id"
    )

    artigos_filtrados = []

    for artigo in artigos:
        paragrafos = organizar_conteudo(artigo.conteudo)
        artigo.total_paragrafos = len(paragrafos)

        if termo:
            termo_regex = re.compile(re.escape(termo), re.IGNORECASE)
            artigo.todos_paragrafos_destacados = [
                termo_regex.sub(r'<mark>\g<0></mark>', p) for p in paragrafos
            ]
        else:
            artigo.todos_paragrafos_destacados = paragrafos

        if termo:
            paragrafos_exibidos = [
                p for p in artigo.todos_paragrafos_destacados
                if termo.lower() in p.lower()
            ]

            if paragrafos_exibidos:
                artigo.paragrafos = paragrafos_exibidos
                artigos_filtrados.append(artigo)
        else:
            artigo.paragrafos = paragrafos
            artigos_filtrados.append(artigo)

    # 🔥 NOVO: carregar capítulos para sidebar
    capitulos = Capitulo.objects.prefetch_related(
        "seccoes__subseccoes"
    ).all().order_by("numero")

    todos_artigos = Artigo.objects.all().order_by(
        "capitulo__id", "seccao__id", "subseccao__id", "id"
    )

    contexto = {
        "artigos": artigos_filtrados,  # resultados da pesquisa
        "todos_artigos": todos_artigos,  # sidebar completa
        "termo": termo,
        "capitulos": capitulos
    }

    return render(request, "servicos/lei_geral.html", contexto)




