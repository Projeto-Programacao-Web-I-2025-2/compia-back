from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin import SimpleListFilter

from .models import Categoria, Ebook, Livro, Produto


class ProdutoTypeFilter(SimpleListFilter):
    title = "Tipo de Produto"
    parameter_name = "tipo_produto"

    def lookups(self, request, model_admin):
        return (
            ("livro", "Livro"),
            ("ebook", "Ebook"),
        )

    def queryset(self, request, queryset):
        if self.value() == "livro":
            return queryset.filter(livro__isnull=False)
        elif self.value() == "ebook":
            return queryset.filter(ebook__isnull=False)


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "produto", "preco")
    list_filter = ("categorias", "idioma", ProdutoTypeFilter)
    search_fields = ("nome",)

    def produto(self, obj):
        if hasattr(obj, "livro"):
            url = reverse("admin:produto_livro_change", args=[obj.livro.id])
            return format_html('<a href="{}">Livro</a>', url)
        elif hasattr(obj, "ebook"):
            url = reverse("admin:produto_ebook_change", args=[obj.ebook.id])
            return format_html('<a href="{}">Ebook</a>', url)
        return "-"
    produto.short_description = "Produto"

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_superuser


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nome",)
    search_fields = ("nome",)

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_staff


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)


class LivroAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "estoque", "idioma", "vendedor")
    list_filter = ("categorias", "idioma")
    search_fields = ("nome",)
    readonly_fields = (
        "id", "nome", "preco", "estoque", "vendedor", "descricao",
        "autor", "ano_lancamento", "idioma"
    )
    fields = (
        "id", "nome", "categorias", "preco", "vendedor", "estoque",
        "descricao", "autor", "ano_lancamento", "idioma"
    )

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_staff


class EbookAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "preco", "idioma", "vendedor")
    list_filter = ("categorias", "idioma")
    search_fields = ("nome",)
    readonly_fields = (
        "id", "nome", "preco", "arquivo", "vendedor", "descricao",
        "autor", "ano_lancamento", "idioma"
    )
    fields = (
        "id", "nome", "categorias", "preco", "vendedor", "arquivo",
        "descricao", "autor", "ano_lancamento", "idioma"
    )

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_module_permission(self, request):
        return request.user.is_staff


admin.site.register(Livro, LivroAdmin)
admin.site.register(Ebook, EbookAdmin)
