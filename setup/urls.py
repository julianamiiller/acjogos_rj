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
    path('accounts/cadastro/', cadastro_view, name='cadastro'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)