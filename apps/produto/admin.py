from django.contrib import admin

from .models import Categoria, Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco",)
    list_filter = ("categorias",)
    search_fields = ("nome",)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome",)
    search_fields = ("nome",)


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
