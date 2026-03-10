from rest_framework import viewsets

from .models import Venda
from .serializers import VendaSerializer
from apps.user.permissions import IsSellerUser


class VendaViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsSellerUser]
    serializer_class = VendaSerializer

    def get_queryset(self):
        return Venda.objects.filter(vendedor=self.request.user.vendedor)
