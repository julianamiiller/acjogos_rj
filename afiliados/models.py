from django.db import models
from perfis.models import Perfil


class Afiliado(models.Model):
    perfil = models.OneToOneField(
        Perfil,
        on_deletname='dados_afiliado',
        limit_choices_to={'tipo_usuario': 'AFILIADO'}
    )
    
        related_
    cpf = models.CharField('CPF', max_length=14, unique=True)
    data_nascimento = models.DateField('Data de Nascimento', null=True, blank=True)
    telefone = models.CharField('Telefone', max_length=20)
    telefone_alternativo = models.CharField('Telefone Alternativo', max_length=20, blank=True)
    

    cep = models.CharField('CEP', max_length=9, blank=True)
    endereco = models.CharField('Endereço', max_length=200, blank=True)
    numero = models.CharField('Número', max_length=10, blank=True)
    complemento = models.CharField('Complemento', max_length=100, blank=True)
    bairro = models.CharField('Bairro', max_length=100, blank=True)
    cidade = models.CharField('Cidade', max_length=100, blank=True)
    estado = models.CharField('Estado', max_length=2, blank=True)
    
    area_atuacao = models.CharField('Área de Atuação', max_length=100, blank=True)
    especialidade = models.CharField('Especialidade', max_length=100, blank=True)
    biografia = models.TextField('Biografia', blank=True)
    

    banco = models.CharField('Banco', max_length=100, blank=True)
    agencia = models.CharField('Agência', max_length=10, blank=True)
    conta = models.CharField('Conta', max_length=20, blank=True)
    tipo_conta = models.CharField(
        'Tipo de Conta',
        max_length=20,
        choices=[
            ('corrente', 'Corrente'),
            ('poupanca', 'Poupança'),
        ],
        blank=True
    )
    
    ativo = models.BooleanField('Ativo', default=True)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Afiliado'
        verbose_name_plural = 'Afiliados'
        ordering = ['-data_cadastro']
    
    def __str__(self):
        return f"{self.perfil.user.get_full_name()} - CPF: {self.cpf}"
    
    @property
    def nome_completo(self):
        return self.perfil.user.get_full_name()


class ContratoAfiliacao(models.Model):
    afiliado = models.ForeignKey(
        Afiliado,
        on_delete=models.CASCADE,
        related_name='contratos'
    )
    
    numero_contrato = models.CharField('Número do Contrato', max_length=50, unique=True)
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Término', null=True, blank=True)
    
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('suspenso', 'Suspenso'),
        ('encerrado', 'Encerrado'),
        ('pendente', 'Pendente'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    comissao_percentual = models.DecimalField(
        'Comissão (%)',
        max_digits=5,
        decimal_places=2,
        default=10.00
    )
    
    termo_aceito = models.BooleanField('Termo Aceito', default=False)
    data_aceite = models.DateTimeField('Data de Aceite', null=True, blank=True)
    ip_aceite = models.GenericIPAddressField('IP do Aceite', null=True, blank=True)
    
    observacoes = models.TextField('Observações', blank=True)
    
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)
    
    class Meta:
        verbose_name = 'Contrato de Afiliação'
        verbose_name_plural = 'Contratos de Afiliação'
        ordering = ['-data_criacao']
    
    def __str__(self):
        return f"Contrato {self.numero_contrato} - {self.afiliado.nome_completo}"