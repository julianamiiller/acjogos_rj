from django import forms
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_fantasia',
            'razao_social',
            'cnpj',
            'email_contato',
            'telefone',
            'site',
        ]
