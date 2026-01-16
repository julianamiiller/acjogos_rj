import os
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required 
from django.conf import settings
from django.conf.urls.static import static

# Organizando os imports das views de forma limpa
from perfis.views import cadastro_view, pos_login_view, cadastro_pendente_view
from empresas.views import (
    empresa_cadastrar_view, 
    minha_empresa_view, 
    empresa_editar_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota personalizada de cadastro
    path('accounts/cadastro/', cadastro_view, name='cadastro'), 
    
    # Rota de cadastro pendente
    path('accounts/pendente/', cadastro_pendente_view, name='cadastro_pendente'),
    
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Home protegida
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),

    path('pos-login/', pos_login_view, name='pos_login'),

    # Rotas de teste (remova antes do deploy)
    path('test-reset-form/', TemplateView.as_view(template_name='registration/password_reset_form.html')),
    path('test-reset-done/', TemplateView.as_view(template_name='registration/password_reset_done.html')),
    path('test-reset-confirm/', TemplateView.as_view(template_name='registration/password_reset_confirm.html')),
    path('test-reset-complete/', TemplateView.as_view(template_name='registration/password_reset_complete.html')),
    
    # --- ROTAS DE EMPRESA ---
    path('empresas/cadastrar/', empresa_cadastrar_view, name='empresa_cadastrar'),
    path('empresas/minha/', minha_empresa_view, name='minha_empresa'),
    
    # Rota de edição (Agora única e apontando para a view correta)
    path('empresas/editar/', empresa_editar_view, name='empresa_editar'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)