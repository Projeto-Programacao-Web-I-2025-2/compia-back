from rest_framework import serializers

from .models import Categoria, Ebook, Livro, Produto


class ProdutoSerializer(serializers.ModelSerializer):
    tipo = serializers.SerializerMethodField()
    estoque = serializers.SerializerMethodField()
    arquivo = serializers.SerializerMethodField()

    class Meta:
        model = Produto
        fields = "__all__"

    def get_tipo(self, obj):
        if hasattr(obj, "livro"):
            return "livro"
        elif hasattr(obj, "ebook"):
            return "ebook"
        return "produto"

    def get_estoque(self, obj):
        if hasattr(obj, "livro"):
            return obj.livro.estoque
        return None

    def get_arquivo(self, obj):
        if hasattr(obj, "ebook"):
            return obj.ebook.arquivo.url if obj.ebook.arquivo else None
        return None


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome"]


class LivroSerializer(serializers.ModelSerializer):
    vendedor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Livro
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        vendedor = getattr(request.user, "vendedor", None)
        if not vendedor:
            raise serializers.ValidationError("Usuário autenticado não é um vendedor.")

        categorias = validated_data.pop("categorias", [])
        validated_data["vendedor"] = vendedor
        livro = Livro.objects.create(**validated_data)
        livro.categorias.set(categorias)
        return livro


class EbookSerializer(serializers.ModelSerializer):
    vendedor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ebook
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        vendedor = getattr(request.user, "vendedor", None)
        if not vendedor:
            raise serializers.ValidationError("Usuário autenticado não é um vendedor.")

        categorias = validated_data.pop("categorias", [])
        validated_data["vendedor"] = vendedor
        ebook = Ebook.objects.create(**validated_data)
        ebook.categorias.set(categorias)
        return ebook
