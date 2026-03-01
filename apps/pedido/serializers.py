from rest_framework import serializers

from apps.pedido.models import Pedido


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"

    def validate_cliente(self, value):
        if not hasattr(value, "role") or value.role != "cliente":
            raise serializers.ValidationError("O usuário selecionado não é um cliente.")
        return value
