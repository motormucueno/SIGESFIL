from django.urls import path
from .views import empresa_view, ajax_trabalhadores, ajax_contraordenacoes
    #listar_empresa, exportar_trabalhadores_excel, exportar_empresas_excel, exportar_contraordenacoes_excel)
#from .views import exportar_empresas_pdf, exportar_trabalhadores_pdf, exportar_contraordenacoes_pdf
urlpatterns = [
    #path('', listar_empresa, name="listar_empresa"),
    #path('cadastrar/', cadastrar_empresa, name="cadastrar_empresa")
# path("exportar/empresas/", exportar_empresas_excel, name="exportar_empresas_excel"),
# path("exportar/trabalhadores/", exportar_trabalhadores_excel, name="exportar_trabalhadores_excel"),
# path("exportar/contraordenacoes/", exportar_contraordenacoes_excel, name="exportar_contraordenacoes_excel"),
# path('exportar/empresas/pdf/', exportar_empresas_pdf, name='exportar_empresas_pdf'),
#     path('exportar/trabalhadores/pdf/', exportar_trabalhadores_pdf, name='exportar_trabalhadores_pdf'),
#     path('exportar/contraordenacoes/pdf/', exportar_contraordenacoes_pdf, name='exportar_contraordenacoes_pdf'),
#path("", cadastrar_empresa, name="cadastrar_empresa"),
#path("", empresa_dashboard, name="empresa_dashboard"),
path("", empresa_view, name="empresa_view"),
path('ajax/contraordenacoes/', ajax_contraordenacoes, name='ajax_contraordenacoes'),
    path('ajax/trabalhadores/', ajax_trabalhadores, name='ajax_trabalhadores'),
]