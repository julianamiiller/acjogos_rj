from django.db import models
from perfis.models import Perfil

class Empresa(models.Model):
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name='empresas'
    )

    nome_fantasia = models.CharField(max_length=150)
    razao_social = models.CharField(max_length=150)
    cnpj = models.CharField(max_length=18, unique=True)

    email_contato = models.EmailField()
    telefone = models.CharField(max_length=15)

    site = models.URLField(blank=True, null=True)

    # Adicionamos null=True apenas para facilitar a migração inicial
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.nome_fantasia