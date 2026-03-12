from rest_framework import serializers

from .models import Vendedor
from apps.user.models import User


class VendedorCreateSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = Vendedor
        fields = ["id", "nome", "email", "password", "role"]

    def create(self, validated_data):
        nome = validated_data.pop("nome")
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        user = User.objects.create_user(
            nome=nome,
            email=email,
            password=password,
            role=User.Role.VENDEDOR
        )
        vendedor = Vendedor.objects.create(user=user, **validated_data)
        return vendedor


class VendedorSerializer(serializers.ModelSerializer):
    nome = serializers.CharField(source="user.nome")
    email = serializers.EmailField(source="user.email")
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = Vendedor
        fields = ["id", "nome", "email", "role"]

    def update(self, instance, validated_data):
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
