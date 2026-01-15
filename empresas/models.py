from django.db import models
from perfis.models import Perfil

class Empresa(models.Model):
    # Lista de tuplas para o campo de escolha (Choices)
    ESTADOS_CHOICES = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
        ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]

    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE, related_name='empresa')
    
    # Dados Cadastrais
    nome_fantasia = models.CharField(max_length=150, verbose_name="Nome Fantasia")
    razao_social = models.CharField(max_length=150, verbose_name="Razão Social")
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    
    # Endereço
    cep = models.CharField(max_length=9, verbose_name="CEP")
    logradouro = models.CharField(max_length=255, verbose_name="Logradouro")
    numero = models.CharField(max_length=20, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    
    # Adicionado o choices para garantir padronização no banco de dados
    estado = models.CharField(
        max_length=2, 
        choices=ESTADOS_CHOICES, 
        verbose_name="UF"
    )

    # Contato
    email_contato = models.EmailField(verbose_name="E-mail de Contato")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    site = models.URLField(blank=True, null=True, verbose_name="Site/URL")

    criado_em = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"

    def __str__(self):
        return self.nome_fantasia