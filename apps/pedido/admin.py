from django.contrib import admin

from apps.pedido.models import Pedido


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "data_pedido", "frete", "total", "status")
    list_filter = ("status", "data_pedido")
    search_fields = ("cliente__nome",)

    def has_add_permission(self, request):
        return False


admin.site.register(Pedido, PedidoAdmin)
