from django.urls import path
from . import views

app_name = 'coletivos'

urlpatterns = [
  
    path('cadastro/', views.cadastro_coletivo, name='cadastro'),


    path('perfil/', views.meu_perfil_coletivo, name='meu_perfil'),

    path('editar/', views.editar_coletivo, name='editar'),

    path('dashboard/', views.dashboard_coletivo, name='dashboard'),
]
