from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Cliente
from .serializers import ClienteCreateSerializer, ClienteSerializer
from apps.user.permissions import IsClientUser


class ClienteViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Cliente.objects.all()
    permission_classes = [IsAuthenticated, IsClientUser]

    def get_permissions(self):
        if self.action in ["create"]:
            return [AllowAny()]
        elif self.action in ["destroy", "update", "partial_update"]:
            return [IsAuthenticated(), IsClientUser()]
        return []

    def get_serializer_class(self):
        if self.action == "create":
            return ClienteCreateSerializer
        return ClienteSerializer

    @action(detail=False, methods=['get', 'put', 'patch', 'delete'], url_path='me')
    def me(self, request):
        cliente = getattr(request.user, "cliente", None)

        if not cliente:
            return Response({"detail": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = self.get_serializer(cliente)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            partial = request.method == 'PATCH'
            serializer = self.get_serializer(cliente, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'DELETE':
            user = cliente.user
            cliente.delete()
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
