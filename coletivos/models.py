from django.db import models
from perfis.models import Perfil

class Coletivo(models.Model):
    perfil = models.OneToOneField(
        Perfil,
        on_delete=models.CASCADE,
        related_name='dados_coletivo',
        limit_choices_to={'tipo_usuario': 'COLETIVO'}
    )

    nome_institucional = models.CharField(max_length=200)
    cnpj = models.CharField(max_length=18, unique=True)
    responsavel_legal = models.CharField(max_length=150)
    telefone = models.CharField(max_length=20)
    email_institucional = models.EmailField()

    cep = models.CharField(max_length=9, blank=True)
    endereco = models.CharField(max_length=200, blank=True)
    numero = models.CharField(max_length=10, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)

    descricao = models.TextField(blank=True)

    ativo = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Coletivo Institucional'
        verbose_name_plural = 'Coletivos Institucionais'

    def __str__(self):
        return self.nome_institucional
