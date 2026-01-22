from django.urls import path
from . import views

app_name = 'core_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('notificacoes/', views.notificacoes, name='notificacoes'),
    path('notificacoes/<int:notificacao_id>/lida/', views.marcar_notificacao_lida, name='marcar_notificacao_lida'),
    path('notificacoes/marcar-todas/', views.marcar_todas, name='marcar_todas'),
    path('atividades/', views.atividades, name='atividades'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
    path('favoritos/adicionar/', views.adicionar_favorito, name='adicionar_favorito'),
    path('favoritos/remover/<int:favorito_id>/', views.remover_favorito, name='remover_favorito'),
]