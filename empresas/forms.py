from django import forms
from .models import Empresa

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = [
            'nome_fantasia', 'razao_social', 'cnpj',
            'cep', 'logradouro', 'numero', 'complemento', 
            'bairro', 'cidade', 'estado',
            'email_contato', 'telefone', 'site',
        ]
        # Adicionamos IDs para o JavaScript encontrar os campos facilmente
        widgets = {
            'cep': forms.TextInput(attrs={'id': 'id_cep', 'onblur': 'pesquisacep(this.value);'}),
            'logradouro': forms.TextInput(attrs={'id': 'id_logradouro'}),
            'bairro': forms.TextInput(attrs={'id': 'id_bairro'}),
            'cidade': forms.TextInput(attrs={'id': 'id_cidade'}),
            'estado': forms.TextInput(attrs={'id': 'id_estado'}),
        }
