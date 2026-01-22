# afiliados/urls.py
from django.urls import path
from . import views

app_name = 'afiliados'

urlpatterns = [
    path('completar-cadastro/', views.cadastro_afiliado, name='cadastro_afiliado'),
    path('meu-perfil/', views.meu_perfil_afiliado, name='meu_perfil'),
    path('editar/', views.editar_afiliado, name='editar_afiliado'),
    path('contratos/', views.contratos_afiliado, name='contratos'),
    path('contratos/aceitar/<int:contrato_id>/', views.aceitar_contrato, name='aceitar_contrato'),
]