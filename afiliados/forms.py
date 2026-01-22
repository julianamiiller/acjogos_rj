from django import forms
from .models import Afiliado

class AfiliadoForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        exclude = ['perfil', 'ativo', 'data_cadastro', 'data_atualizacao']
        
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not field.widget.attrs.get('class'):
                field.widget.attrs['class'] = 'form-control'

class AfiliadoEditForm(forms.ModelForm):
    class Meta:
        model = Afiliado
        exclude = ['perfil', 'ativo']
        
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'biografia': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'