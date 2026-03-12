from rest_framework import serializers

from .models import Cliente, Endereco
from apps.user.models import User


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = ["rua", "numero", "complemento", "bairro", "cidade", "estado", "cep"]


class ClienteCreateSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    endereco = EnderecoSerializer(required=False)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = Cliente
        fields = ["id", "nome", "email", "password", "endereco", "role"]

    def create(self, validated_data):
        nome = validated_data.pop("nome")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            nome=nome,
            email=email,
            password=password,
            role=User.Role.CLIENTE
        )
        endereco_data = validated_data.pop("endereco", None)
        endereco = Endereco.objects.create(**endereco_data) if endereco_data else None
        cliente = Cliente.objects.create(user=user, endereco=endereco, **validated_data)
        return cliente


class ClienteSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome")
    email = serializers.EmailField(source="user.email")
    endereco = EnderecoSerializer(required=False)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = Cliente
        fields = ["id", "nome", "email", "endereco", "role"]

    def update(self, instance, validated_data):
        endereco_data = validated_data.pop("endereco", None)
        if endereco_data:
            if instance.endereco:
                for attr, value in endereco_data.items():
                    setattr(instance.endereco, attr, value)
                instance.endereco.save()
            else:
                instance.endereco = Endereco.objects.create(**endereco_data)
                instance.save()
        user_data = validated_data.pop("user", {})
        nome = user_data.get("nome")
        if nome:
            instance.user.nome = nome
        email = user_data.get("email")
        if email:
            instance.user.email = email
        if nome or email:
            instance.user.save()
        return instance
