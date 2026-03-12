import pytest

from apps.vendedor.models import Vendedor
from apps.user.models import User


@pytest.mark.django_db
class TestVendedorViewSet():
    def test_seller_creation(self, api_client):
        payload = {
            "nome": "Vendedor Teste",
            "email": "vendedor@teste.com",
            "password": "senha123",
        }

        response = api_client.post("/api/vendedores/", payload, format="json")

        assert response.status_code == 201
        vendedor = Vendedor.objects.get(user__email=payload["email"])
        assert vendedor.user.nome == payload["nome"]
        assert vendedor.user.email == payload["email"]
        assert response.data["role"] == User.Role.VENDEDOR

    def test_seller_creation_without_email_fails(self, api_client):
        payload = {
            "nome": "Vendedor Sem Email",
            "password": "senha123",
        }

        response = api_client.post("/api/vendedores/", payload, format="json")

        assert response.status_code == 400
        assert "email" in response.data

    def test_seller_retrieve(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)

        response = api_client.get("/api/vendedores/me/")

        assert response.status_code == 200
        assert response.data["nome"] == seller_user.nome
        assert response.data["email"] == seller_user.email
        assert response.data["role"] == User.Role.VENDEDOR

    def test_seller_partial_update(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        new_nome = "Vendedor Teste Atualizado"
        new_email = "vendedor.atualizado@teste.com"

        response = api_client.patch("/api/vendedores/me/", {"nome": new_nome, "email": new_email}, format="json")

        assert response.status_code == 200
        seller_user.refresh_from_db()
        assert seller_user.nome == new_nome
        assert seller_user.email == new_email
        assert response.data["role"] == User.Role.VENDEDOR

    def test_seller_update_name(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        new_nome = "Vendedor Teste Completo"
        payload = {
            "nome": new_nome,
        }

        response = api_client.patch("/api/vendedores/me/", payload, format="json")

        assert response.status_code == 200
        seller_user.refresh_from_db()
        assert seller_user.nome == new_nome

    def test_seller_update(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        payload = {
            "nome": "Vendedor Teste Completo",
            "email": "vendedor.completo@teste.com",
        }

        response = api_client.put("/api/vendedores/me/", payload, format="json")

        assert response.status_code == 200
        seller_user.refresh_from_db()
        assert seller_user.nome == payload["nome"]
        assert seller_user.email == payload["email"]

    def test_seller_destroy(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        nome = seller_user.nome

        response = api_client.delete("/api/vendedores/me/")

        assert response.status_code == 204
        assert not User.objects.filter(nome=nome).exists()
        assert not Vendedor.objects.filter(user__nome=nome).exists()
