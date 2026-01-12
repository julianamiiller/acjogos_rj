import os
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required 
from perfis.views import cadastro_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rota personalizada de cadastro
    path('accounts/cadastro/', cadastro_view, name='cadastro'), 
    
    # Esta linha abaixo já inclui TODAS as rotas de login, logout e reset de senha
    # As rotas de reset serão: accounts/password_reset/, accounts/password_reset/done/, etc.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Home protegida (só acessa se estiver logado)
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),

    path('test-reset-form/', TemplateView.as_view(template_name='registration/password_reset_form.html')),
    path('test-reset-done/', TemplateView.as_view(template_name='registration/password_reset_done.html')),
    path('test-reset-confirm/', TemplateView.as_view(template_name='registration/password_reset_confirm.html')),
    path('test-reset-complete/', TemplateView.as_view(template_name='registration/password_reset_complete.html')),
# nao suba essas rotas de teste para o github
]

# Configuração para arquivos estáticos (CSS, JS, Imagens) em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)