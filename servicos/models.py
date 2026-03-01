from django.db import models

class Capitulo(models.Model):
    numero = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    def __str__(self): return f"Capítulo {self.numero}"
class Seccao(models.Model):
    numero = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name="seccoes")
    def __str__(self): return f"Secção {self.numero}"
class SubSeccao(models.Model):
    numero = models.CharField(max_length=20)
    descricao = models.TextField(blank=True)
    seccao = models.ForeignKey(Seccao, on_delete=models.CASCADE, related_name="subseccoes")
    def __str__(self): return f"Subsecção {self.numero}"
class Artigo(models.Model):
    numero = models.CharField(max_length=20)
    titulo = models.TextField(blank=True)
    descricao = models.CharField(max_length=255, blank=True, null=True)
    conteudo = models.TextField()
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, null=True, blank=True)
    seccao = models.ForeignKey(Seccao, on_delete=models.CASCADE, null=True, blank=True)
    subseccao = models.ForeignKey(SubSeccao, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self): return f"Artigo {self.numero}"