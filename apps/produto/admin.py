from django.contrib import admin

from .models import Categoria, Ebook, Livro, Produto


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco",)
    list_filter = ("categorias",)
    search_fields = ("nome",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome",)
    search_fields = ("nome",)


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)


class LivroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "estoque",)
    list_filter = ("categorias",)
    search_fields = ("nome",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False


class EbookAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco",)
    list_filter = ("categorias",)
    search_fields = ("nome",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request):
        return False


admin.site.register(Livro, LivroAdmin)
admin.site.register(Ebook, EbookAdmin)
