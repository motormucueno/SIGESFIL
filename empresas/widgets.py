from .models import SectorEconomico, ContraOrdenacao
from trabalhadores.models import Razoes, Incapacidade
from django_select2.forms import ModelSelect2Widget, ModelSelect2MultipleWidget

class SectorModelSelect2Widget(ModelSelect2Widget):
    model = SectorEconomico
    search_fields = ["nome__icontains",]
class IncapacidadeModelSelect2Widget(ModelSelect2Widget):
    model = Incapacidade
    search_fields = ["nome__icontains",]
class RazoesModelSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = Razoes
    search_fields = ["nome__icontains",]
class ContraordenacaoModelSelect2MultipleWidget(ModelSelect2MultipleWidget):
    model = ContraOrdenacao
    search_fields = ["nome__icontains",]
