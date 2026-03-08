from rest_framework import serializers

from .models import Pedido, ItemPedido
from apps.cliente.models import Cliente
from decimal import Decimal


class ItemPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemPedido
        fields = ["produto", "quantidade"]


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = [
            "id",
            "cliente",
            "itens",
            "data_pedido",
            "data_entrega",
            "frete",
            "total",
            "status",
        ]
        read_only_fields = ["total", "cliente"]

    def calculate_total(self, itens, frete):
        total = sum([item.produto.preco * item.quantidade for item in itens])
        if frete:
            total += frete
        return total

    def create(self, validated_data):
        request = self.context.get('request')
        itens_data = validated_data.pop('itens', [])
        validated_data.pop('cliente', None)
        frete = validated_data.get('frete', Decimal('0.00'))

        try:
            cliente = Cliente.objects.get(user=request.user)
        except Cliente.DoesNotExist:
            raise serializers.ValidationError("Usuário não possui perfil de cliente.")

        pedido = Pedido.objects.create(cliente=cliente, **validated_data)
        itens_objs = []
        for item in itens_data:
            item_obj = ItemPedido.objects.create(
                pedido=pedido,
                produto=item['produto'],
                quantidade=item['quantidade']
            )
            itens_objs.append(item_obj)
        pedido.total = self.calculate_total(itens_objs, frete)
        pedido.save()
        return pedido

    def update(self, instance, validated_data):
        instance.data_entrega = validated_data.get('data_entrega', instance.data_entrega)
        instance.frete = validated_data.get('frete', instance.frete)
        instance.status = validated_data.get('status', instance.status)
        instance.total = self.calculate_total(instance.itens.all(), instance.frete or Decimal('0.00'))
        instance.save()
        return instance
