from django import forms
from django.core.exceptions import ValidationError
from .models import ConfiguracaoDashboard, MenuFavorito, Notificacao


class ConfiguracaoDashboardForm(forms.ModelForm):
    """
    Formulário para configurações do dashboard.
    Permite personalização da experiência do usuário.
    """
    class Meta:
        model = ConfiguracaoDashboard
        fields = [
            'exibir_atividades_recentes',
            'exibir_notificacoes',
            'exibir_estatisticas',
            'exibir_atalhos',
            'itens_por_pagina',
            'tema',
            'notificacoes_email',
            'notificacoes_push',
        ]
        widgets = {
            'exibir_atividades_recentes': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'exibir_notificacoes': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'exibir_estatisticas': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'exibir_atalhos': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'itens_por_pagina': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '5',
                'max': '100',
                'step': '5'
            }),
            'tema': forms.Select(attrs={
                'class': 'form-control'
            }),
            'notificacoes_email': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'notificacoes_push': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'exibir_atividades_recentes': 'Exibir atividades recentes no dashboard',
            'exibir_notificacoes': 'Exibir notificações no dashboard',
            'exibir_estatisticas': 'Exibir estatísticas no dashboard',
            'exibir_atalhos': 'Exibir atalhos rápidos no dashboard',
            'itens_por_pagina': 'Itens por página em listagens',
            'tema': 'Tema de cores',
            'notificacoes_email': 'Receber notificações por e-mail',
            'notificacoes_push': 'Receber notificações push',
        }
        help_texts = {
            'itens_por_pagina': 'Número de itens exibidos em listas (entre 5 e 100)',
            'tema': 'Escolha o tema visual do sistema',
        }
    
    def clean_itens_por_pagina(self):
        itens = self.cleaned_data.get('itens_por_pagina')
        
        if itens and (itens < 5 or itens > 100):
            raise ValidationError('O número de itens deve estar entre 5 e 100.')
        
        return itens


class MenuFavoritoForm(forms.ModelForm):
    """
    Formulário para adicionar itens ao menu de favoritos.
    """
    class Meta:
        model = MenuFavorito
        fields = ['nome', 'url', 'icone', 'ordem']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do atalho',
                'maxlength': '100'
            }),
            'url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/caminho/da/pagina/',
                'maxlength': '500'
            }),
            'icone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'fa-home (opcional)',
                'maxlength': '50'
            }),
            'ordem': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'value': '0'
            }),
        }
        labels = {
            'nome': 'Nome do atalho',
            'url': 'URL',
            'icone': 'Ícone (Font Awesome)',
            'ordem': 'Ordem de exibição',
        }
        help_texts = {
            'nome': 'Nome descritivo para o atalho',
            'url': 'URL da página (ex: /empresas/minha-empresa/)',
            'icone': 'Classe do ícone Font Awesome (ex: fa-home, fa-building)',
            'ordem': 'Quanto menor o número, mais no início aparece',
        }
    
    def clean_url(self):
        url = self.cleaned_data.get('url')
        
        if not url:
            raise ValidationError('A URL é obrigatória.')
        
        # Verifica se começa com /
        if not url.startswith('/'):
            url = '/' + url
        
        # Verifica se termina com /
        if not url.endswith('/'):
            url = url + '/'
        
        return url
    
    def clean_ordem(self):
        ordem = self.cleaned_data.get('ordem')
        
        if ordem is None:
            return 0
        
        if ordem < 0:
            raise ValidationError('A ordem não pode ser negativa.')
        
        return ordem


class NotificacaoForm(forms.ModelForm):
    """
    Formulário para criar notificações (uso administrativo).
    """
    enviar_para_todos = forms.BooleanField(
        required=False,
        label='Enviar para todos os usuários',
        help_text='Marca esta opção para enviar a notificação para todos os perfis',
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Notificacao
        fields = ['perfil', 'titulo', 'mensagem', 'tipo', 'link']
        widgets = {
            'perfil': forms.Select(attrs={
                'class': 'form-control'
            }),
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título da notificação',
                'maxlength': '200'
            }),
            'mensagem': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Mensagem da notificação...'
            }),
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'link': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '/caminho/da/acao/ (opcional)',
                'maxlength': '500'
            }),
        }
        labels = {
            'perfil': 'Destinatário',
            'titulo': 'Título',
            'mensagem': 'Mensagem',
            'tipo': 'Tipo',
            'link': 'Link de ação (opcional)',
        }
        help_texts = {
            'link': 'URL para onde o usuário será redirecionado ao clicar na notificação',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se enviar_para_todos estiver marcado, perfil não é obrigatório
        if self.data.get('enviar_para_todos'):
            self.fields['perfil'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        enviar_para_todos = cleaned_data.get('enviar_para_todos')
        perfil = cleaned_data.get('perfil')
        
        if not enviar_para_todos and not perfil:
            raise ValidationError('Selecione um destinatário ou marque "Enviar para todos".')
        
        return cleaned_data


class FiltroAtividadesForm(forms.Form):
    """
    Formulário para filtrar o histórico de atividades.
    """
    PERIODO_CHOICES = [
        ('', 'Todos os períodos'),
        ('hoje', 'Hoje'),
        ('semana', 'Última semana'),
        ('mes', 'Último mês'),
        ('trimestre', 'Último trimestre'),
    ]
    
    acao = forms.ChoiceField(
        required=False,
        label='Tipo de ação',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[('', 'Todas as ações')]
    )
    
    periodo = forms.ChoiceField(
        required=False,
        label='Período',
        choices=PERIODO_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    busca = forms.CharField(
        required=False,
        label='Buscar',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Buscar por descrição...'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Importa aqui para evitar importação circular
        from .models import AtividadeRecente
        
        # Adiciona as opções de ação dinamicamente
        acoes = [('', 'Todas as ações')] + list(AtividadeRecente.ACAO_CHOICES)
        self.fields['acao'].choices = acoes


class FiltroNotificacoesForm(forms.Form):
    """
    Formulário para filtrar notificações.
    """
    STATUS_CHOICES = [
        ('todas', 'Todas'),
        ('nao_lidas', 'Não lidas'),
        ('lidas', 'Lidas'),
    ]
    
    TIPO_CHOICES = [
        ('', 'Todos os tipos'),
    ]
    
    status = forms.ChoiceField(
        required=False,
        label='Status',
        choices=STATUS_CHOICES,
        initial='todas',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    tipo = forms.ChoiceField(
        required=False,
        label='Tipo',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=[('', 'Todos os tipos')]
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Importa aqui para evitar importação circular
        from .models import Notificacao
        
        # Adiciona as opções de tipo dinamicamente
        tipos = [('', 'Todos os tipos')] + list(Notificacao.TIPO_CHOICES)
        self.fields['tipo'].choices = tipos