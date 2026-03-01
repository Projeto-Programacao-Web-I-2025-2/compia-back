from drf_spectacular.utils import extend_schema, extend_schema_view

from .serializers import PedidoSerializer

pedido_schema = extend_schema_view(
    list=extend_schema(
        summary="Listar pedidos",
        description="Retorna uma lista de pedidos.",
        responses={200: PedidoSerializer(many=True)},
        tags=["pedidos"],
    ),
    retrieve=extend_schema(
        summary="Detalhar pedido",
        description="Retorna os detalhes de um pedido.",
        responses={200: PedidoSerializer},
        tags=["pedidos"],
    ),
    create=extend_schema(
        summary="Criar pedido",
        description="Cria um novo pedido.",
        request=PedidoSerializer,
        responses={201: PedidoSerializer},
        tags=["pedidos"],
    ),
    update=extend_schema(
        summary="Atualizar pedido",
        description="Atualiza todos os campos de um pedido.",
        request=PedidoSerializer,
        responses={200: PedidoSerializer},
        tags=["pedidos"],
    ),
    partial_update=extend_schema(
        summary="Atualização parcial do pedido",
        description="Atualiza parcialmente os campos de um pedido.",
        request=PedidoSerializer,
        responses={200: PedidoSerializer},
        tags=["pedidos"],
    ),
    destroy=extend_schema(
        summary="Excluir pedido",
        description="Exclui um pedido.",
        responses={204: None},
        tags=["pedidos"],
    ),
    )

__all__ = [
    "pedido_schema",
]
