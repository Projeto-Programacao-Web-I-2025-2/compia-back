from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    model = User
    ordering = ("id", "nome")
    list_display = ("id", "nome", "email", "role",)
    list_filter = ("role",)
    search_fields = ("nome", "email",)

    fieldsets = (
        ("Informações", {"fields": ("nome", "email", "password", "role")}),
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

    add_fieldsets = (
        ("Informações", {
            "classes": ("wide",),
            "fields": ("nome", "email", "password1", "password2", "role"),
        }),
        ("Permissões", {
            "fields": ("is_active", "is_staff", "is_superuser"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        # Se for o próprio usuário, pode editar tudo
        if request.user == obj:
            return ()
        # Se o usuário autenticado for BACKOFFICE, pode editar tudo
        if obj.role == request.user.Role.BACKOFFICE:
            return ()
        # Se o usuário autenticado for EDITOR, nao pode editar outros EDITOR ou BACKOFFICE
        if obj.role == request.user.Role.EDITOR and request.user.role == request.user.Role.EDITOR:
            return ("nome", "email", "password", "role")
        # Caso contrário, readonly nos campos sensíveis
        return ("nome", "email", "password", "role")

    def save_model(self, request, obj, form, change):
        if obj.role == obj.Role.BACKOFFICE:
            obj.is_staff = True
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
