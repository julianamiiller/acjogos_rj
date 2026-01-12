from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
    # --- SUA BASE ORIGINAL ---
    TIPOS_USUARIO = [
        ('DIRETOR', 'Diretoria'),
        ('ASSOCIADO', 'Associado'),
        ('AFILIADO', 'Afiliado'),
        ('COLETIVO', 'Coletivo/Institucional'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPOS_USUARIO,
        default='AFILIADO',
    )
    
    telefone_contato = models.CharField(max_length=15, blank=True, null=True)

    # --- NOVAS ATUALIZAÇÕES  ---
    
    # Nome social é listado como opcional no documento 
    nome_social = models.CharField(max_length=150, blank=True, null=True) 
    
    # CPF é obrigatório para o responsável 
    cpf = models.CharField(max_length=14, unique=True, null=True, blank=True)
    
    # Nick no Discord
    discord_nick = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nick no Discord")
    
    # Campos de Endereço exigidos 
    cep = models.CharField(max_length=9, blank=True, null=True)
    endereco = models.CharField(max_length=255, blank=True, null=True, verbose_name="Endereço")
    numero = models.CharField(max_length=10, blank=True, null=True, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username + " (" + self.get_tipo_usuario_display() + ")"