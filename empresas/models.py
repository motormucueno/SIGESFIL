from django.db import models

class TipoInspeccao(models.Model):
    nome = models.CharField("Tipo de inspecção", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Tipo de inspecção"
        verbose_name_plural = "Tipos de inspecção"
    def __str__(self):
        return self.nome
class SectorEconomico(models.Model):
    nome = models.CharField("Ramo económico", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Sector económico"
        verbose_name_plural = "Sector económico"
    def __str__(self):
        return self.nome
class TipoPropriedade(models.Model):
    nome = models.CharField("Tipo de propriedade", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Tipo de propriedade"
        verbose_name_plural = "Tipo de propriedade"
    def __str__(self):
        return self.nome
class Provincia(models.Model):
    nome = models.CharField("Província", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Província"
        verbose_name_plural = "Província"
    def __str__(self):
        return self.nome
class ContraOrdenacao(models.Model):
    nome = models.CharField("Seleccione as contra-ordenações verificadas", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Contra-ordenação"
        verbose_name_plural = "Contra-ordenação"
    def __str__(self):
        return self.nome
class ContraOrdenacaoRecomendacao(models.Model):
    nome = models.CharField("Seleccione as contra-ordenações verificadas", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Contra-ordenação para recomendação"
        verbose_name_plural = "Contra-ordenação para recomendação"
    def __str__(self):
        return self.nome
class ObjectivoInspeccao(models.Model):
    nome = models.CharField("Objectivo da inspecção", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Objectivo da inspecção"
        verbose_name_plural = "Objectivo da inspecção"
    def __str__(self):
        return self.nome
class Empresa(models.Model):
    # DADOS DA EMPRESA
    objectivo_inspeccao = models.ForeignKey(ObjectivoInspeccao, on_delete=models.PROTECT, verbose_name="Objectivo da inspecção", null=True)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    data_inspeccao = models.DateField("Data inspectiva")
    sector = models.ForeignKey(SectorEconomico, on_delete=models.PROTECT, verbose_name="Ramo económico", null=True)
    hora_inicio = models.TimeField("Hora de início da inspecção", null=True)
    hora_termino = models.TimeField("Hora de término da inspecção", null=True)
    tipo_inspeccao = models.ForeignKey(TipoInspeccao, on_delete=models.PROTECT, verbose_name="Tipo inspecção", null=True)
    nome = models.CharField("Designação da empresa", max_length=300)
    nif = models.CharField("NIF da empresa", max_length=50)
    propriedade = models.ForeignKey(TipoPropriedade, on_delete=models.PROTECT, verbose_name="Propriedade da Empresa", null=True)
    telefone = models.CharField("Telefone da empresa", null=True, blank=True, max_length=9)
    email = models.EmailField("Email da empresa", max_length=50, null=True, blank=True)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT, verbose_name="Província", null=True)
    municipio = models.CharField("Município", max_length=100, null=True, blank=True)
    distrito = models.CharField("Distrito", max_length=100, null=True, blank=True)
    bairro = models.CharField("Bairro", max_length=100, null=True, blank=True)
    rua = models.CharField("Rua", max_length=100, null=True, blank=True)
    documentos_analizados = models.TextField("Documentos / aspectos analisados", null=True, blank=True)
    provas_colhidas = models.TextField("Elementos de provas colhidos", null=True, blank=True)
    factos_constatados = models.TextField("Factos constatados", null=True, blank=True)
    contra_ordenacoes = models.ManyToManyField(ContraOrdenacao, verbose_name="Contra-ordenações laborais", blank=True)
    observacao_entidade_empregadora = models.TextField("Observação da entidade empregadora", null=True, blank=True)
    conclusão = models.TextField("Conclusão da inspecção", null=True, blank=True)
    prazo_regularizacao = models.IntegerField(
        "Prazo de regularização das contra-ordenações leves",
        null=True,
        blank=True
    )
    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"
    def __str__(self):
        return self.nome

