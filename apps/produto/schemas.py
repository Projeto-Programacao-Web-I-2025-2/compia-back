from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import ProdutoSerializer, ProdutoListSerializer

produto_schema = extend_schema_view(
    list=extend_schema(
        summary="Listar produtos",
        description="Retorna uma lista de produtos.",
        responses={200: ProdutoListSerializer(many=True)},
        tags=["produtos"],
    ),
    retrieve=extend_schema(
        summary="Detalhar produto",
        description="Retorna os detalhes de um produto.",
        responses={200: ProdutoSerializer},
        tags=["produtos"],
    ),
    create=extend_schema(
        summary="Criar produto",
        description="Cria um novo produto.",
        request=ProdutoSerializer,
        responses={201: ProdutoSerializer},
        tags=["produtos"],
    ),
    update=extend_schema(
        summary="Atualizar produto",
        description="Atualiza todos os campos de um produto.",
        request=ProdutoSerializer,
        responses={200: ProdutoSerializer},
        tags=["produtos"],
    ),
    partial_update=extend_schema(
        summary="Atualização parcial do produto",
        description="Atualiza parcialmente os campos de um produto.",
        request=ProdutoSerializer,
        responses={200: ProdutoSerializer},
        tags=["produtos"],
    ),
    destroy=extend_schema(
        summary="Excluir produto",
        description="Exclui um produto.",
        responses={204: None},
        tags=["produtos"],
    ),
)

__all__ = [
    "produto_schema",
]
