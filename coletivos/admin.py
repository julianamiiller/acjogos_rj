from django.contrib import admin
from .models import Coletivo

@admin.register(Coletivo)
class ColetivoAdmin(admin.ModelAdmin):
    list_display = ('nome_institucional', 'cnpj', 'ativo', 'data_cadastro')
    search_fields = ('nome_institucional', 'cnpj')
    list_filter = ('ativo',)
