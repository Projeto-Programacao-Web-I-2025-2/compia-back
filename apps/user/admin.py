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
        ("Permissões", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )

    add_fieldsets = (
        ("Informações", {
            "classes": ("wide",),
            "fields": ("nome", "email", "password1", "password2", "role"),
        }),
        ("Permissões", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
        }),
    )

    def save_model(self, request, obj, form, change):
        if obj.role == obj.Role.BACKOFFICE:
            obj.is_staff = True
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
