from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Vendedor
from .serializers import VendedorCreateSerializer, VendedorSerializer
from apps.produto.models import Produto
from apps.produto.serializers import ProdutoSerializer
from apps.user.permissions import IsSellerUser


class VendedorViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Vendedor.objects.all()
    permission_classes = [IsAuthenticated, IsSellerUser]

    def get_permissions(self):
        if self.action in ["create"]:
            return [AllowAny()]
        elif self.action in ["destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsSellerUser()]
        return []

    def get_serializer_class(self):
        if self.action == "create":
            return VendedorCreateSerializer
        return VendedorSerializer

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'], url_path='me')
    def me(self, request):
        vendedor = getattr(request.user, "vendedor", None)

        if not vendedor:
            return Response({"detail": "Vendedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(vendedor)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(vendedor, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            user = vendedor.user
            vendedor.delete()
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='meus-produtos')
    def meus_produtos(self, request):
        vendedor = getattr(request.user, "vendedor", None)
        if not vendedor:
            return Response({"detail": "Vendedor não encontrado."}, status=status.HTTP_404_NOT_FOUND)
        produtos = Produto.objects.filter(vendedor=vendedor)
        serializer = ProdutoSerializer(produtos, many=True)
        return Response(serializer.data)
