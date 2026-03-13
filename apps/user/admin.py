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
            "fields": ("is_staff", "is_superuser"),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        # Se for o próprio usuário, pode editar tudo
        if request.user == obj:
            return ()
        # Se o usuário autenticado for superuser e o objeto for BACKOFFICE, pode editar tudo
        if request.user.is_superuser and obj.role == request.user.Role.BACKOFFICE:
            return ()
        # Caso contrário, readonly nos campos sensíveis
        return ("nome", "email", "password", "role")

    def save_model(self, request, obj, form, change):
        if obj.role == obj.Role.BACKOFFICE:
            obj.is_staff = True
        super().save_model(request, obj, form, change)

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff


admin.site.register(User, UserAdmin)
