from django import forms
from .models import Coletivo


class ColetivoForm(forms.ModelForm):
    class Meta:
        model = Coletivo
        exclude = ('perfil', 'ativo', 'data_cadastro', 'data_atualizacao')
