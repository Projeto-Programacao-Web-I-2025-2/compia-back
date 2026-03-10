from rest_framework import serializers
from .models import Venda, ItemVenda


class ItemVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemVenda
        fields = ["produto", "quantidade"]


class VendaSerializer(serializers.ModelSerializer):
    itens = ItemVendaSerializer(many=True)

    class Meta:
        model = Venda
        fields = ["id", "cliente", "vendedor", "data_venda", "valor_total", "itens"]
