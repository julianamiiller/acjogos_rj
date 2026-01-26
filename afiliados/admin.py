from django.contrib import admin
from .models import Afiliado, ContratoAfiliacao


@admin.register(Afiliado)
class AfiliadoAdmin(admin.ModelAdmin):
    list_display = (
        'perfil',
        'cpf',
        'ativo',
        'data_cadastro',
    )
    search_fields = (
        'perfil__user__username',
        'perfil__user__email',
        'cpf',
    )
    list_filter = ('ativo', 'data_cadastro')
    ordering = ('-data_cadastro',)


@admin.register(ContratoAfiliacao)
class ContratoAfiliacaoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_contrato',
        'afiliado',
        'status',
        'data_inicio',
        'data_fim',
        'termo_aceito',
    )
    list_filter = (
        'status',
        'termo_aceito',
        'data_inicio',
    )
    search_fields = (
        'numero_contrato',
        'afiliado__perfil__user__username',
    )
    ordering = ('-data_criacao',)
