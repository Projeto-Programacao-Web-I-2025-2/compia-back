from django.contrib import admin

from apps.pedido.models import Pedido, ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    can_delete = False
    readonly_fields = ("item", "quantidade", "tipo_produto", "vendedor")
    fields = ("item", "quantidade", "tipo_produto", "vendedor")
    show_change_link = False
    verbose_name = "Item do Pedido"
    verbose_name_plural = "Itens do Pedido"
    max_num = 0

    def item(self, obj):
        return obj.produto.nome if obj.produto else "-"
    item.short_description = "Produto"

    def tipo_produto(self, obj):
        if hasattr(obj.produto, "ebook"):
            return "Ebook"
        elif hasattr(obj.produto, "livro"):
            return "Livro"
        return "Outro"
    tipo_produto.short_description = "Tipo"

    def vendedor(self, obj):
        return obj.produto.vendedor if obj.produto and obj.produto.vendedor else "-"
    vendedor.short_description = "Vendedor"


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "data_pedido", "frete", "total", "status")
    list_filter = ("status", "data_pedido")
    search_fields = ("cliente__nome",)
    readonly_fields = ("id", "cliente", "data_pedido", "data_entrega", "frete", "total", "status")
    fieldsets = (
        ("Informações gerais", {
            "fields": ("id", "cliente", "data_pedido", "data_entrega", "frete", "total", "status")
        }),
    )
    inlines = [ItemPedidoInline]

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


admin.site.register(Pedido, PedidoAdmin)
