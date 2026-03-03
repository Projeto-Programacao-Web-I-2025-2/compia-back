from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from drf_spectacular.utils import extend_schema

from .models import Categoria, Produto
from .pagination import ProdutoPagination
from .schemas import produto_schema
from .serializers import CategoriaSerializer, ProdutoSerializer, ProdutoListSerializer


@produto_schema
class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    filterset_fields = ["nome", "descricao", "idioma", "tipo_produto", "categorias"]
    ordering_fields = ["nome", "preco", "ano_lancamento", "tipo_produto"]
    pagination_class = ProdutoPagination

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ["list"]:
            return ProdutoListSerializer
        else:
            return ProdutoSerializer

    @extend_schema(
        summary="Lista todas as categorias",
        responses=CategoriaSerializer(many=True),
        tags=["produtos"],
    )
    @action(
        detail=False,
        methods=["get"],
        url_path="categorias",
        filterset_fields=[],
        pagination_class=None
    )
    def categorias(self, request):
        categorias = Categoria.objects.all()
        serializer = CategoriaSerializer(categorias, many=True)
        return Response(serializer.data)
