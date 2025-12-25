import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ValidadorComplexidadeSenha:
    """
    Garante que a senha tenha letras maiúsculas, números e caracteres especiais.
    """
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos uma letra maiúscula."),
                code='senha_sem_maiuscula',
            )
        
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um número."),
                code='senha_sem_numero',
            )
            
        if not re.findall('[^a-zA-Z0-9]', password):
            raise ValidationError(
                _("A senha deve conter pelo menos um caractere especial (ex: @, #, $, %)."),
                code='senha_sem_especial',
            )

    def get_help_text(self):
        return _("Sua senha deve conter letras maiúsculas, números e caracteres especiais.")

class ValidadorTamanhoMinimo:
    """
    Validação customizada para comprimento mínimo da senha.
    """
    def __init__(self, comprimento_minimo=8):
        self.comprimento_minimo = comprimento_minimo

    def validate(self, password, user=None):
        if len(password) < self.comprimento_minimo:
            raise ValidationError(
                _("Senha muito curta. O sistema exige pelo menos %(min)d caracteres."),
                code='senha_muito_curta',
                params={'min': self.comprimento_minimo},
            )

    def get_help_text(self):
        return _("Use no mínimo %(min)d caracteres.") % {'min': self.comprimento_minimo}