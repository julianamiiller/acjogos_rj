from django.urls import path
from .views import empresa_cadastrar_view, minha_empresa_view, empresa_editar_view

urlpatterns = [
    path('cadastrar/', empresa_cadastrar_view, name='empresa_cadastrar'),
    path('minha/', minha_empresa_view, name='minha_empresa'),
    path('editar/', empresa_editar_view, name='empresa_editar'),
]