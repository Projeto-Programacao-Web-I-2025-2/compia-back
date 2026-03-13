from django.contrib import admin

from .models import Vendedor


class VendedorAdmin(admin.ModelAdmin):
    list_display = ("id", "user_nome", "user_email")
    search_fields = ("user__nome", "user__email")
    fieldsets = (
        ("Informações do Vendedor", {
            "fields": ("user_nome", "user_email")
        }),
    )

    def user_nome(self, obj):
        return obj.user.nome
    user_nome.short_description = "Nome"
    user_nome.admin_order_field = "user__nome"

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = "E-mail"
    user_email.admin_order_field = "user__email"

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def delete_model(self, request, obj):
        user = obj.user
        user.delete()

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            user = obj.user
            user.delete()


admin.site.register(Vendedor, VendedorAdmin)
