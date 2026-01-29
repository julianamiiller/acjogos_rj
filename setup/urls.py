import os
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import views as auth_views  # <--- Importante: Importei as views de auth
from django.conf import settings
from django.conf.urls.static import static

from perfis.views import cadastro_view, pos_login_view, cadastro_pendente_view
from empresas.views import (
    empresa_cadastrar_view, 
    minha_empresa_view, 
    empresa_editar_view
)

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota de logout forçando o redirecionamento para a tela de login
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    
    path('accounts/cadastro/', cadastro_view, name='cadastro'), 
    path('accounts/pendente/', cadastro_pendente_view, name='cadastro_pendente'),
    
    # Rotas de Autenticação e Senha
    path('accounts/', include('django.contrib.auth.urls')),
    
    #protecao home
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    #pos login
    path('pos-login/', pos_login_view, name='pos_login'),

    path('dashboard/', include('core_dashboard.urls', namespace='core_dashboard')),

    path('empresas/cadastrar/', empresa_cadastrar_view, name='empresa_cadastrar'),
    path('empresas/minha/', minha_empresa_view, name='minha_empresa'),
    path('empresas/editar/', empresa_editar_view, name='empresa_editar'),

    path('afiliados/', include('afiliados.urls', namespace='afiliados')),

    path('test-reset-form/', TemplateView.as_view(
        template_name='registration/password_reset_form.html'
    )),
    path('test-reset-done/', TemplateView.as_view(
        template_name='registration/password_reset_done.html'
    )),
    path('test-reset-confirm/', TemplateView.as_view(
        template_name='registration/password_reset_confirm.html'
    )),
    path('test-reset-complete/', TemplateView.as_view(
        template_name='registration/password_reset_complete.html'
    )),

    path('coletivos/', include('coletivos.urls', namespace='coletivos')),

    

]

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, 
        document_root=settings.STATIC_ROOT
    )