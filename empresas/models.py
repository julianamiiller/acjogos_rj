from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    # Vínculo com o usuário dono da empresa (Associado) [cite: 24]
    responsavel = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # Dados Jurídicos 
    nome_fantasia = models.CharField(max_length=255) # [cite: 37]
    razao_social = models.CharField(max_length=255) # [cite: 38]
    cnpj = models.CharField(max_length=18, unique=True) # [cite: 39]
    email_contato = models.EmailField() # [cite: 40]
    telefone = models.CharField(max_length=20) # [cite: 41]
    site = models.URLField(blank=True, null=True) # [cite: 42]
    
    # Endereço da Empresa [cite: 43]
    cep = models.CharField(max_length=9)
    endereco_completo = models.CharField(max_length=255) # Simplificando endereço para o exemplo
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nome_fantasia