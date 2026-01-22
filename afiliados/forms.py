from django import forms
from django.core.exceptions import ValidationError
from .models import Afiliado, ContratoAfiliacao
import re


class AfiliadoForm(forms.ModelForm):
    """
    Formulário para cadastro inicial do afiliado.
    """
    class Meta:
        model = Afiliado
        fields = [
            'cpf',
            'data_nascimento',
            'telefone',
            'telefone_alternativo',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'area_atuacao',
            'especialidade',
            'biografia',
        ]
        widgets = {
            'cpf': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '000.000.000-00',
                'maxlength': '14'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'telefone_alternativo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'maxlength': '9'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc.'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nº'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, Bloco, etc.'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Selecione o estado'),
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
            ]),
            'area_atuacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Marketing Digital, Vendas, etc.'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Redes Sociais, E-commerce, etc.'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte um pouco sobre sua experiência profissional...'
            }),
        }
    
    def clean_cpf(self):
        """Valida e formata o CPF"""
        cpf = self.cleaned_data.get('cpf', '')
        
        # Remove caracteres não numéricos
        cpf_numeros = re.sub(r'\D', '', cpf)
        
        if len(cpf_numeros) != 11:
            raise ValidationError('CPF deve conter 11 dígitos.')
        
        # Verifica CPFs inválidos conhecidos
        if cpf_numeros == cpf_numeros[0] * 11:
            raise ValidationError('CPF inválido.')
        
        # Valida dígitos verificadores
        def calcular_digito(cpf_parcial):
            soma = 0
            for i, digito in enumerate(cpf_parcial):
                soma += int(digito) * (len(cpf_parcial) + 1 - i)
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)
        
        if cpf_numeros[9] != calcular_digito(cpf_numeros[:9]):
            raise ValidationError('CPF inválido.')
        if cpf_numeros[10] != calcular_digito(cpf_numeros[:10]):
            raise ValidationError('CPF inválido.')
        
        # Formata o CPF
        cpf_formatado = f"{cpf_numeros[:3]}.{cpf_numeros[3:6]}.{cpf_numeros[6:9]}-{cpf_numeros[9:]}"
        
        # Verifica se já existe outro afiliado com este CPF
        if Afiliado.objects.filter(cpf=cpf_formatado).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Já existe um afiliado cadastrado com este CPF.')
        
        return cpf_formatado
    
    def clean_cep(self):
        """Valida e formata o CEP"""
        cep = self.cleaned_data.get('cep', '')
        
        if not cep:
            return cep
        
        # Remove caracteres não numéricos
        cep_numeros = re.sub(r'\D', '', cep)
        
        if len(cep_numeros) != 8:
            raise ValidationError('CEP deve conter 8 dígitos.')
        
        # Formata o CEP
        return f"{cep_numeros[:5]}-{cep_numeros[5:]}"
    
    def clean_telefone(self):
        """Valida o telefone"""
        telefone = self.cleaned_data.get('telefone', '')
        
        # Remove caracteres não numéricos
        telefone_numeros = re.sub(r'\D', '', telefone)
        
        if len(telefone_numeros) not in [10, 11]:
            raise ValidationError('Telefone deve conter 10 ou 11 dígitos.')
        
        return telefone


class AfiliadoEditForm(forms.ModelForm):
    """
    Formulário para edição dos dados do afiliado.
    Permite editar informações pessoais e profissionais, mas não o CPF.
    """
    class Meta:
        model = Afiliado
        fields = [
            'data_nascimento',
            'telefone',
            'telefone_alternativo',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
            'area_atuacao',
            'especialidade',
            'biografia',
            'banco',
            'agencia',
            'conta',
            'tipo_conta',
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'telefone_alternativo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(00) 00000-0000'
            }),
            'cep': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-000',
                'maxlength': '9'
            }),
            'endereco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Rua, Avenida, etc.'
            }),
            'numero': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nº'
            }),
            'complemento': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Apto, Bloco, etc.'
            }),
            'bairro': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bairro'
            }),
            'cidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Cidade'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-control'
            }, choices=[
                ('', 'Selecione o estado'),
                ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
                ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
                ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
                ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
                ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'),
                ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
                ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
                ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
                ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
                ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
            ]),
            'area_atuacao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Marketing Digital, Vendas, etc.'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Redes Sociais, E-commerce, etc.'
            }),
            'biografia': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Conte um pouco sobre sua experiência profissional...'
            }),
            'banco': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do banco'
            }),
            'agencia': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0000'
            }),
            'conta': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '00000-0'
            }),
            'tipo_conta': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def clean_cep(self):
        """Valida e formata o CEP"""
        cep = self.cleaned_data.get('cep', '')
        
        if not cep:
            return cep
        
        # Remove caracteres não numéricos
        cep_numeros = re.sub(r'\D', '', cep)
        
        if len(cep_numeros) != 8:
            raise ValidationError('CEP deve conter 8 dígitos.')
        
        # Formata o CEP
        return f"{cep_numeros[:5]}-{cep_numeros[5:]}"
    
    def clean_telefone(self):
        """Valida o telefone"""
        telefone = self.cleaned_data.get('telefone', '')
        
        # Remove caracteres não numéricos
        telefone_numeros = re.sub(r'\D', '', telefone)
        
        if len(telefone_numeros) not in [10, 11]:
            raise ValidationError('Telefone deve conter 10 ou 11 dígitos.')
        
        return telefone


class ContratoAfiliacaoForm(forms.ModelForm):
    """
    Formulário para criação/edição de contratos de afiliação.
    Usado principalmente no admin ou por gestores.
    """
    class Meta:
        model = ContratoAfiliacao
        fields = [
            'afiliado',
            'numero_contrato',
            'data_inicio',
            'data_fim',
            'status',
            'comissao_percentual',
            'observacoes',
        ]
        widgets = {
            'afiliado': forms.Select(attrs={
                'class': 'form-control'
            }),
            'numero_contrato': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'CTR-2024-0001'
            }),
            'data_inicio': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'data_fim': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'status': forms.Select(attrs={
                'class': 'form-control'
            }),
            'comissao_percentual': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '100',
                'placeholder': '10.00'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Observações sobre o contrato...'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        
        if data_inicio and data_fim:
            if data_fim <= data_inicio:
                raise ValidationError('A data de término deve ser posterior à data de início.')
        
        return cleaned_data
    
    def clean_comissao_percentual(self):
        comissao = self.cleaned_data.get('comissao_percentual')
        
        if comissao and (comissao < 0 or comissao > 100):
            raise ValidationError('A comissão deve estar entre 0% e 100%.')
        
        return comissao