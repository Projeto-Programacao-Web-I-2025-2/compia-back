from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Pedido
from .pagination import PedidoPagination
from .schemas import pedido_schema
from .serializers import PedidoSerializer
from apps.user.permissions import IsClientUser


@pedido_schema
class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    filterset_fields = ["status", "cliente__nome"]
    search_fields = ["cliente__nome", "produtos__nome"]
    ordering_fields = ["data_pedido", "total"]
    pagination_class = PedidoPagination
    permission_classes = [IsAuthenticated, IsClientUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pedido.objects.all()
        return Pedido.objects.filter(cliente=user)

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)
