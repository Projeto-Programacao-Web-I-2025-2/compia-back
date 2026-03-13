from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Pedido
from .schemas import pedido_schema
from .serializers import PedidoSerializer
from apps.cliente.models import Cliente
from apps.user.permissions import IsClientUser


@pedido_schema
class PedidoViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = PedidoSerializer
    filterset_fields = ["status"]
    search_fields = ["produtos__nome"]
    ordering_fields = ["data_pedido", "total"]
    permission_classes = [IsAuthenticated, IsClientUser]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Pedido.objects.all().order_by("-id")
        try:
            cliente = Cliente.objects.get(user=user)
        except Cliente.DoesNotExist:
            return Pedido.objects.none()
        return Pedido.objects.filter(cliente=cliente).order_by("-id")

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated, IsClientUser])
    def cancelar(self, request, pk=None):
        pedido = self.get_object()
        if pedido.status in [Pedido.StatusPedido.ENTREGUE, Pedido.StatusPedido.CANCELADO, Pedido.StatusPedido.ENVIADO]:
            return Response(
                {
                    "detail": "Não é possível cancelar um pedido já enviado, entregue ou cancelado."
                },
                status=400
            )
        pedido.status = Pedido.StatusPedido.CANCELADO
        pedido.save()
        return Response({"detail": "Pedido cancelado com sucesso."})
