from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil

class CadastroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Nome")
    last_name = forms.CharField(max_length=30, required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label="E-mail")
    
    tipo_usuario = forms.ChoiceField(
        choices=Perfil.TIPOS_USUARIO[1:],
        label="Tipo de Vínculo"
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'tipo_usuario')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmar Senha"

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
            perfil, _ = Perfil.objects.get_or_create(user=user)
            perfil.tipo_usuario = self.cleaned_data['tipo_usuario']
            perfil.save()
        return user