from django.contrib import admin
from .models import Empresa, TipoInspeccao, SectorEconomico, TipoPropriedade, Provincia, ContraOrdenacao, ObjectivoInspeccao
from trabalhadores.models import Trabalhador, Genero, TipoDocumento, ClassificacaoTrabalhador, TipoAcidente, TipoContracto, Incapacidade, Provincia, Razoes

# Admins simplificados para os modelos auxiliares
@admin.register(ObjectivoInspeccao)
class ObjectivoInspeccaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)
@admin.register(TipoInspeccao)
class TipoInspeccaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(SectorEconomico)
class SectorEconomicoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(TipoPropriedade)
class TipoPropriedadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(Provincia)
class ProvinciaAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(TipoDocumento)
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(ContraOrdenacao)
class ContraOrdenacaoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(ClassificacaoTrabalhador)
class ClassificacaoTrabalhadorAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(Razoes)
class RazoesAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(TipoContracto)
class TipoContractoAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(Incapacidade)
class IncapacidadeAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)

@admin.register(TipoAcidente)
class TipoAcidenteAdmin(admin.ModelAdmin):
    list_display = ("nome", "criado_em", "actualizado_em")
    list_filter = ("nome",)
    search_fields = ("nome",)
    ordering = ("id",)


# Inline para Trabalhador
class TrabalhadorInline(admin.TabularInline):  # Você pode usar StackedInline se quiser mais espaço por trabalhador
    model = Trabalhador
    extra = 1  # número de trabalhadores que aparecem por padrão
    min_num = 0
    #classes = ["collapse"]  # opcional: recolher
    show_change_link = True  # permite clicar para editar individualmente
    fields = [
        'nome', 'genero', 'nascimento', 'trabalhador', 'pais', 'documento',
        'numero_documento', 'contracto', 'razoes', 'duracao',
        'acidente', 'doenca', 'incapacidade', 'custo_directo', 'custo_indirecto',
        'capacidade_reduzida', 'telefone', 'observacao', 'representante'
    ]

# Ação personalizada
@admin.action(description="Exportar contra-ordenações")
def action_exportar(modeladmin, request, queryset):
    for empresa in queryset:
        for act in empresa.contra_ordenacoes.all():
            print(act)
# Admin da Empresa
@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):

    list_display = ("objectivo_inspeccao", "alterar_formato_data", "hora_inicio", "hora_termino",'nome', 'nif', "propriedade","sector", "tipo_inspeccao",
                    "documentos_analizados","provas_colhidas", "factos_constatados", "mostrar_contraordenacao", "prazo_regularizacao",
                    "observacao_entidade_empregadora", "conclusão","telefone", "email",'provincia', 'municipio', "bairro", "rua")
    search_fields = ('nome', 'nif', 'municipio')
    list_filter = ("data_inspeccao", "propriedade", "tipo_inspeccao", "sector", 'provincia')
    filter_vertical = ("contra_ordenacoes",) #permite seleccionar mais de uma contraordenação
    #autocomplete_fields = ("contra_ordenacoes",)
    actions = [action_exportar]
    ordering = ("data_inspeccao",)
    inlines = [TrabalhadorInline]  # Aqui é que os trabalhadores aparecem dentro da empresa
    # O codigo abaixo permite organizar o formulário em secções
    fieldsets = (
        ("📌 Data e Horário da Inspecção", {
            "fields": (
                "data_inspeccao",
                "hora_inicio",
                "hora_termino",
            )
        }),
        ("🏢 Identificação da Empresa", {
            "fields": (
                "nome",
                "nif",
                "propriedade",
                "sector",
                "telefone",
                "email",
            )
        }),

        ("📍 Localização", {
            "fields": (
                "provincia",
                "municipio",
                "distrito",
                "bairro",
                "rua",
            )
        }),
        ("📂 Dados Inspectivos", {
            "fields": (
                "tipo_inspeccao",
                "documentos_analizados",
                "provas_colhidas",
                "factos_constatados",
            )
        }),

        ("⚠️ Contra-ordenações verificadas", {
            "fields": (
                "contra_ordenacoes",
                "prazo_regularizacao",
            )
        }),

        ("📝 Observações Finais", {
            "fields": (
                "observacao_entidade_empregadora",
                "conclusão",
            )
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/admin_personalizar.css',)
        }


    def alterar_formato_data(self, obj):
        if obj.data_inspeccao:
            return obj.data_inspeccao.strftime("%d/%m/%Y")
    alterar_formato_data.short_description = "Data da inspecção"
    def mostrar_contraordenacao(self, obj):
        return ", ".join([c.nome for c in obj.contra_ordenacoes.all()])
    mostrar_contraordenacao.short_description = "Contra-ordenações"
