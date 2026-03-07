from rest_framework import serializers

from .models import Categoria, Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"
        read_only_fields = ["vendedor"]

    def create(self, validated_data):
        request = self.context.get('request')
        categorias = validated_data.pop('categorias', [])
        produto = Produto.objects.create(
            vendedor=request.user,
            **validated_data
        )
        produto.categorias.set(categorias)
        return produto

    def update(self, instance, validated_data):
        categorias = validated_data.pop('categorias', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if categorias is not None:
            instance.categorias.set(categorias)
        return instance


class ProdutoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = ["id", "nome", "preco", "imagem"]


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome"]
