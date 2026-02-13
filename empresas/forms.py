from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django_select2.forms import Select2MultipleWidget
from .models import SectorEconomico, ContraOrdenacao, ObjectivoInspeccao
from trabalhadores.models import Razoes, Incapacidade
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

from empresas.models import Empresa
from trabalhadores.models import Trabalhador, Incapacidade, Razoes




# ==========================
# FORMULÁRIO DA EMPRESA
# ==========================

class EmpresaForm(forms.ModelForm):

    class Meta:
        model = Empresa
        fields = [
            "objectivo_inspeccao", 'data_inspeccao', 'hora_inicio', 'hora_termino',
            'nome', 'nif', 'propriedade', 'sector','tipo_inspeccao',
            'provas_colhidas', 'factos_constatados','documentos_analizados',
            'observacao_entidade_empregadora', 'conclusão', 'telefone', 'email', 'provincia',
            'municipio','distrito', 'bairro', 'rua','contra_ordenacoes', 'prazo_regularizacao'
        ]
        widgets = {
            "objectivo_inspeccao": ModelSelect2Widget(
                model=ObjectivoInspeccao,
                search_fields=["nome__icontains"],
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Seleccione objectivo"
                }),
            "sector": ModelSelect2Widget(
                model=SectorEconomico,
                search_fields=["nome__icontains"],
                attrs={
                 "class": "form-control",
                 "data-placeholder": "Seleccione sector económico"
             }),
            "data_inspeccao": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control"
            }),
            "hora_inicio": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),
            "hora_termino": forms.TimeInput(attrs={
                "type": "time",
                "class": "form-control"
            }),
            "documentos_analizados": forms.Textarea(attrs={
                "class": "form-control", "rows": 3
            }),
            "provas_colhidas": forms.Textarea(attrs={
                "class": "form-control", "rows": 3
            }),
            "factos_constatados": forms.Textarea(attrs={
                "class": "form-control", "rows": 4
            }),
            "observacao_entidade_empregadora": forms.Textarea(attrs={
                "class": "form-control", "rows": 3
            }),
            "conclusão": forms.Textarea(attrs={
                "class": "form-control", "rows": 3
            }),
            "contra_ordenacoes": ModelSelect2MultipleWidget(
                model=ContraOrdenacao,
                search_fields=["nome__icontains"],
                attrs={
                    "class": "form-control",
                    "data-placeholder": "Seleccione as contra-ordenações",
                    "style": "width:100%"
                #}
            #),
        })}


    def clean(self):
        cleaned = super().clean()

        obrigatorios = [
            "objectivo_inspeccao", 'data_inspeccao', 'hora_inicio', 'hora_termino',
            'nome', 'nif', 'propriedade', 'sector',
            'municipio', 'tipo_inspeccao',
            'provas_colhidas', 'factos_constatados'
        ]

        for campo in obrigatorios:
            if not cleaned.get(campo):
                self.add_error(campo, 'Este campo é obrigatório.')

        return cleaned


# ==========================
# FORMULÁRIO DO TRABALHADOR
# ==========================

class TrabalhadorForm(forms.ModelForm):
    class Meta:
        model = Trabalhador
        exclude = ('empresa',)
        widgets = {
            'razoes': ModelSelect2MultipleWidget(
                model=Razoes,
                search_fields=["nome__icontains"],
                attrs={
                'class': 'form-control',
                'data-placeholder': 'Seleccione as razões'
            }),
            'incapacidade': ModelSelect2Widget(
                model=Incapacidade,
                search_fields=["nome__icontains"],
                attrs={
                'class': 'form-control',
                'data-placeholder': 'Seleccione incapacidade'
            }),

        }
    def clean(self):
        cleaned = super().clean()
        contracto = cleaned.get('contracto')
        razoes = cleaned.get('razoes')
        duracao = cleaned.get('duracao')
        acidente = cleaned.get('acidente')
        incapacidade = cleaned.get('incapacidade')
        if contracto and contracto.nome.lower() == 'determinado':
            if not razoes:
                self.add_error('razoes', 'Obrigatório para contrato determinado.')
            if not duracao:
                self.add_error('duracao', 'Obrigatório para contrato determinado.')
        if acidente and not incapacidade:
            self.add_error('incapacidade', 'Informe a incapacidade.')
        return cleaned


TrabalhadorFormSet = inlineformset_factory(
    Empresa,
    Trabalhador,
    form=TrabalhadorForm,
    extra=1,
    can_delete=True
)

