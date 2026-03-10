import pytest

from model_bakery import baker

from apps.vendedor.models import Vendedor
from apps.user.models import User


@pytest.mark.django_db
class TestVendedorViewSet():
    def test_seller_creation(self, api_client):
        endereco = baker.prepare("cliente.Endereco")
        payload = {
            "nome": "Vendedor Teste",
            "email": "vendedor@teste.com",
            "password": "senha123",
            "endereco": {
                "rua": endereco.rua,
                "numero": endereco.numero,
                "bairro": endereco.bairro,
                "complemento": endereco.complemento,
                "cidade": endereco.cidade,
                "estado": endereco.estado,
                "cep": endereco.cep,
            },
        }

        response = api_client.post("/api/vendedores/", payload, format="json")

        assert response.status_code == 201
        vendedor = Vendedor.objects.get(user__email=payload["email"])
        assert vendedor.user.nome == payload["nome"]
        assert vendedor.user.email == payload["email"]
        assert vendedor.endereco.rua == payload["endereco"]["rua"]
        assert vendedor.endereco.numero == payload["endereco"]["numero"]
        assert vendedor.endereco.complemento == payload["endereco"]["complemento"]
        assert vendedor.endereco.bairro == payload["endereco"]["bairro"]
        assert vendedor.endereco.cidade == payload["endereco"]["cidade"]
        assert vendedor.endereco.estado == payload["endereco"]["estado"]
        assert vendedor.endereco.cep == payload["endereco"]["cep"]

    def test_seller_without_address_creation(self, api_client):
        payload = {
            "nome": "Vendedor Sem Endereço",
            "email": "vendedor.sem.endereco@teste.com",
            "password": "senha123",
        }

        response = api_client.post("/api/vendedores/", payload, format="json")

        assert response.status_code == 201
        vendedor = Vendedor.objects.get(user__email=payload["email"])
        assert vendedor.user.nome == payload["nome"]
        assert vendedor.user.email == payload["email"]
        assert vendedor.endereco is None

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

    def test_seller_partial_update(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        new_nome = "Vendedor Teste Atualizado"
        new_email = "vendedor.atualizado@teste.com"

        response = api_client.patch("/api/vendedores/me/", {"nome": new_nome, "email": new_email}, format="json")

        assert response.status_code == 200
        seller_user.refresh_from_db()
        assert seller_user.nome == new_nome
        assert seller_user.email == new_email

    def test_seller_update_address(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        endereco = baker.prepare("cliente.Endereco")
        payload = {
            "endereco": {
                "rua": endereco.rua,
                "numero": endereco.numero,
                "bairro": endereco.bairro,
                "complemento": endereco.complemento,
                "cidade": endereco.cidade,
                "estado": endereco.estado,
                "cep": endereco.cep,
            },
        }

        response = api_client.patch("/api/vendedores/me/", payload, format="json")

        assert response.status_code == 200
        seller_user.refresh_from_db()
        assert seller_user.vendedor.endereco.rua == payload["endereco"]["rua"]
        assert seller_user.vendedor.endereco.numero == payload["endereco"]["numero"]
        assert seller_user.vendedor.endereco.complemento == payload["endereco"]["complemento"]
        assert seller_user.vendedor.endereco.bairro == payload["endereco"]["bairro"]
        assert seller_user.vendedor.endereco.cidade == payload["endereco"]["cidade"]
        assert seller_user.vendedor.endereco.estado == payload["endereco"]["estado"]
        assert seller_user.vendedor.endereco.cep == payload["endereco"]["cep"]

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
        endereco = baker.prepare("cliente.Endereco")
        payload = {
            "nome": "Vendedor Teste Completo",
            "email": "vendedor.completo@teste.com",
            "endereco": {
                "rua": endereco.rua,
                "numero": endereco.numero,
                "complemento": endereco.complemento,
                "bairro": endereco.bairro,
                "cidade": endereco.cidade,
                "estado": endereco.estado,
                "cep": endereco.cep,
            },
        }

        response = api_client.put("/api/vendedores/me/", payload, format="json")

        assert response.status_code == 200
        seller_user.refresh_from_db()
        assert seller_user.nome == payload["nome"]
        assert seller_user.email == payload["email"]
        assert seller_user.vendedor.endereco.rua == payload["endereco"]["rua"]

    def test_seller_destroy(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        nome = seller_user.nome

        response = api_client.delete("/api/vendedores/me/")

        assert response.status_code == 204
        assert not User.objects.filter(nome=nome).exists()
        assert not Vendedor.objects.filter(user__nome=nome).exists()

    def test_list_products_by_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        products = baker.make("produto.Produto", vendedor=seller_user.vendedor, _quantity=3)
        baker.make("produto.Produto", _quantity=2)

        response = api_client.get("/api/vendedores/meus-produtos/")

        assert response.status_code == 200
        assert len(response.data) == 3
        for i in range(3):
            assert response.data[i]["id"] == products[i].id
            assert response.data[i]["nome"] == products[i].nome
