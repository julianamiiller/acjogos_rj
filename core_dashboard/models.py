from django.db import models
from perfis.models import Perfil


class Notificacao(models.Model):
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name='notificacoes'
    )
    
    titulo = models.CharField('Título', max_length=200)
    mensagem = models.TextField('Mensagem')
    
    TIPO_CHOICES = [
        ('info', 'Informação'),
        ('sucesso', 'Sucesso'),
        ('aviso', 'Aviso'),
        ('erro', 'Erro'),
        ('sistema', 'Sistema'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='info')
    
    lida = models.BooleanField('Lida', default=False)
    data_leitura = models.DateTimeField('Data de Leitura', null=True, blank=True)
    
    link = models.CharField('Link', max_length=500, blank=True, help_text='URL para ação relacionada')
    
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.titulo} - {self.perfil.user.get_full_name()}"
    
    def marcar_como_lida(self):
        from django.utils import timezone
        if not self.lida:
            self.lida = True
            self.data_leitura = timezone.now()
            self.save()


class AtividadeRecente(models.Model):
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name='atividades'
    )
    
    ACAO_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('cadastro', 'Cadastro'),
        ('edicao', 'Edição'),
        ('exclusao', 'Exclusão'),
        ('visualizacao', 'Visualização'),
        ('download', 'Download'),
        ('upload', 'Upload'),
        ('outro', 'Outro'),
    ]
    acao = models.CharField('Ação', max_length=50, choices=ACAO_CHOICES)
    
    descricao = models.CharField('Descrição', max_length=300)
    detalhes = models.TextField('Detalhes', blank=True)
    
    ip_address = models.GenericIPAddressField('Endereço IP', null=True, blank=True)
    user_agent = models.TextField('User Agent', blank=True)
    
    data_criacao = models.DateTimeField('Data/Hora', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Atividade Recente'
        verbose_name_plural = 'Atividades Recentes'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"{self.acao} - {self.perfil.user.get_full_name()} - {self.data_criacao.strftime('%d/%m/%Y %H:%M')}"


class ConfiguracaoDashboard(models.Model):
    perfil = models.OneToOneField(
        Perfil,
        on_delete=models.CASCADE,
        related_name='configuracao_dashboard'
    )
    
    exibir_atividades_recentes = models.BooleanField('Exibir Atividades Recentes', default=True)
    exibir_notificacoes = models.BooleanField('Exibir Notificações', default=True)
    exibir_estatisticas = models.BooleanField('Exibir Estatísticas', default=True)
    exibir_atalhos = models.BooleanField('Exibir Atalhos Rápidos', default=True)
    
    itens_por_pagina = models.IntegerField('Itens por Página', default=10)
    tema = models.CharField(
        'Tema',
        max_length=20,
        choices=[
            ('claro', 'Claro'),
            ('escuro', 'Escuro'),
            ('auto', 'Automático'),
        ],
        default='auto'
    )

    notificacoes_email = models.BooleanField('Receber Notificações por E-mail', default=True)
    notificacoes_push = models.BooleanField('Receber Notificações Push', default=False)
    
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Configuração do Dashboard'
        verbose_name_plural = 'Configurações do Dashboard'
    
    def __str__(self):
        return f"Configurações - {self.perfil.user.get_full_name()}"


class MenuFavorito(models.Model):
    perfil = models.ForeignKey(
        Perfil,
        on_delete=models.CASCADE,
        related_name='favoritos'
    )
    
    nome = models.CharField('Nome', max_length=100)
    url = models.CharField('URL', max_length=500)
    icone = models.CharField('Ícone', max_length=50, blank=True, help_text='Classe do ícone (ex: fa-home)')
    ordem = models.IntegerField('Ordem', default=0)
    
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Menu Favorito'
        verbose_name_plural = 'Menus Favoritos'
        ordering = ['ordem', 'nome']
        unique_together = ['perfil', 'url']
    
    def __str__(self):
        return f"{self.nome} - {self.perfil.user.get_full_name()}"