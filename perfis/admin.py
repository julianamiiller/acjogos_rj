from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Perfil

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    verbose_name_plural = 'Perfil Adicional'

class CustomUserAdmin(UserAdmin):
    inlines = (PerfilInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_tipo_vinculo', 'is_staff')
    
    def get_tipo_vinculo(self, obj):
        try:
            return obj.perfil.get_tipo_usuario_display()
        except Perfil.DoesNotExist:
            return "Sem Perfil"
    get_tipo_vinculo.short_description = 'Tipo de Vínculo'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)