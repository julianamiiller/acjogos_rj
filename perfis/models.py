from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model):
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

    def __str__(self):
        return self.user.username + " (" + self.get_tipo_usuario_display() + ")"