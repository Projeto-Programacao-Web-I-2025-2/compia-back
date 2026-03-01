from rest_framework import serializers

from .models import Pedido
from decimal import Decimal


class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = "__all__"
        read_only_fields = ["total", "cliente"]

    def calculate_total(self, produtos, frete):
        total = sum([produto.preco for produto in produtos])
        if frete:
            total += frete
        return total

    def create(self, validated_data):
        request = self.context.get('request')
        produtos = validated_data.pop('produtos', [])
        validated_data.pop('cliente', None)
        frete = validated_data.get('frete', Decimal('0.00'))
        pedido = Pedido.objects.create(
            cliente=request.user,
            **validated_data
        )
        pedido.produtos.set(produtos)
        pedido.total = self.calculate_total(pedido.produtos.all(), frete)
        pedido.save()
        return pedido

    def update(self, instance, validated_data):
        produtos = validated_data.pop('produtos', None)
        validated_data.pop('cliente', None)
        frete = validated_data.get('frete', instance.frete or Decimal('0.00'))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if produtos is not None:
            instance.produtos.set(produtos)
        instance.total = self.calculate_total(instance.produtos.all(), frete)
        instance.save()
        return instance
