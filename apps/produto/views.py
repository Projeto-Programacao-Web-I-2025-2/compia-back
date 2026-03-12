from rest_framework import mixins, status, viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema

from django_filters.rest_framework import DjangoFilterBackend


from .models import Categoria, Ebook, Livro, Produto
from .schemas import produto_schema
from .serializers import CategoriaSerializer, ProdutoSerializer, LivroSerializer, EbookSerializer
from apps.user.permissions import IsSellerUser


@produto_schema
class ProdutoViewSet(viewsets.ReadOnlyModelViewSet):
    filterset_fields = ["idioma", "categorias"]
    ordering_fields = ["nome", "preco", "ano_lancamento"]
    serializer_class = ProdutoSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["nome", "descricao"]

    def get_queryset(self):
        queryset = Produto.objects.all().order_by("-preco")

        tipo = self.request.query_params.get("tipo")
        if tipo == "livro":
            queryset = queryset.filter(livro__isnull=False)
        elif tipo == "ebook":
            queryset = queryset.filter(ebook__isnull=False)
        return queryset.distinct()

    def get_permissions(self):
        if self.action in ["meus-produtos"]:
            return [IsSellerUser()]
        return [AllowAny()]

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

    @action(detail=False, methods=['get'], url_path='meus-produtos')
    def meus_produtos(self, request):
        vendedor = getattr(request.user, "vendedor", None)
        if not vendedor:
            return Response({"detail": "Vendedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        produtos = Produto.objects.filter(vendedor=vendedor)
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)


class LivroViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = LivroSerializer
    permission_classes = [IsSellerUser]

    def get_queryset(self):
        user = self.request.user
        vendedor = getattr(user, "vendedor", None)
        if vendedor:
            return Livro.objects.filter(vendedor=vendedor)
        return Livro.objects.none()


class EbookViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = EbookSerializer
    permission_classes = [IsSellerUser]

    def get_queryset(self):
        user = self.request.user
        vendedor = getattr(user, "vendedor", None)
        if vendedor:
            return Ebook.objects.filter(vendedor=vendedor)
        return Ebook.objects.none()
