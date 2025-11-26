from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Especialidade, PerfilOficina, Problema

# Registra os modelos para aparecerem no painel
admin.site.register(Especialidade)
admin.site.register(Problema)
admin.site.register(PerfilOficina)

# Configuração especial para o Usuário (para ver se é cliente/oficina)
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Tipo de Usuário', {'fields': ('is_cliente', 'is_oficina')}),
    )
    list_display = ['username', 'email', 'is_cliente', 'is_oficina', 'is_staff']