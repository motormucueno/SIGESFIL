from django.db import models
from django_countries.fields import CountryField
from empresas.models import Empresa

class Provincia(models.Model):
    nome = models.CharField("Província", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Província"
        verbose_name_plural = "Província"
    def __str__(self):
        return self.nome
class TipoDocumento(models.Model):
    nome = models.CharField("Tipo de documento", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Documento de identidade"
        verbose_name_plural = "Documento de identidade"
    def __str__(self):
        return self.nome
class Genero(models.Model):
    nome = models.CharField("Nome", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Género"
        verbose_name_plural = "Género"
    def __str__(self):
        return self.nome

class ClassificacaoTrabalhador(models.Model):
    nome = models.CharField("Trabalhador", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Classificação de trabalhador"
        verbose_name_plural = "Classificação dos trabalhador"
    def __str__(self):
        return self.nome
class TipoContracto(models.Model):
    nome = models.CharField("Nome", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Contrato de trabalho"
        verbose_name_plural = "Contrato de trabalho"
    def __str__(self):
        return self.nome
class Razoes(models.Model):
    nome = models.CharField("Razões de contracto de trabalho por tempo determinado", max_length=300)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Razões de contracto de trabalho por tempo determinado"
        verbose_name_plural = "Razões de contracto de trabalho por tempo determinado"
    def __str__(self):
        return self.nome
class TipoAcidente(models.Model):
    nome = models.CharField("Acidente de trabalho", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Acidente de trabalho"
        verbose_name_plural = "Acidente de trabalho"
    def __str__(self):
        return self.nome
class Incapacidade(models.Model):
    nome = models.CharField("Incapacidade", max_length=50)
    criado_em = models.DateTimeField("Data de criação", auto_now_add=True)
    actualizado_em = models.DateTimeField("Data de actualização", auto_now=True)
    class Meta:
        verbose_name = "Incapacidade"
        verbose_name_plural = "Incapacidade"
    def __str__(self):
        return self.nome

class Trabalhador(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="trabalhadores")
    nome = models.CharField("Nome do trabalhador", max_length=300)
    genero = models.ForeignKey(Genero, verbose_name="Género", on_delete=models.PROTECT, null=True)
    nascimento = models.DateField("Data de nascimento", null=True)
    trabalhador = models.ForeignKey(ClassificacaoTrabalhador, verbose_name="Trabalhador", on_delete=models.PROTECT, null=True)
    pais = CountryField(verbose_name="País de origem", null=True,)
    documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT,verbose_name="Documento de identidade", null=True, blank=True)
    numero_documento = models.CharField("Nº de documento", max_length=50, null=True, blank=True)
    contracto = models.ForeignKey(TipoContracto, on_delete=models.PROTECT, verbose_name="Contracto de trabalho", null=True,)
    razoes = models.ForeignKey(Razoes, on_delete=models.PROTECT, verbose_name="Razões de contracto de trabalho por tempo determinado", null=True, blank=True)
    duracao = models.PositiveIntegerField(verbose_name="Duração(número de meses)", null=True, blank=True)
    acidente = models.ForeignKey(TipoAcidente, on_delete=models.PROTECT, verbose_name="Acidente de trabalho", null=True, blank=True)
    doenca = models.BooleanField(verbose_name="Doença profissional", default=False)
    incapacidade = models.ForeignKey(Incapacidade, on_delete=models.PROTECT, verbose_name="Incapacidade",null=True, blank=True)
    custo_directo = models.DecimalField(verbose_name="Custos directos em kz", max_digits=12, decimal_places=2, null=True, blank=True)
    custo_indirecto = models.DecimalField(verbose_name="Custos indirectos em kz", max_digits=12, decimal_places=2, null=True, blank=True)
    capacidade_reduzida = models.BooleanField(verbose_name="Capacidade reduzida", default=False)
    telefone = models.CharField("Telefone", null=True, blank=True, max_length=9)
    observacao = models.TextField("Outras informações", null=True, blank=True)
    representante = models.BooleanField(verbose_name="Representante", default=False)

    class Meta:
        verbose_name = "Trabalhador"
        verbose_name_plural = "Trabalhador"

    def __str__(self):
        return self.nome
