import pytest

from model_bakery import baker

from apps.cliente.models import Cliente
from apps.user.models import User


@pytest.mark.django_db
class TestClienteViewSet():
    def test_client_creation(self, api_client):
        endereco = baker.prepare("cliente.Endereco")
        payload = {
            "nome": "Cliente Teste",
            "email": "cliente@teste.com",
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

        response = api_client.post("/api/clientes/", payload, format="json")

        assert response.status_code == 201
        client = Cliente.objects.get(user__email=payload["email"])
        assert client.user.nome == payload["nome"]
        assert client.user.email == payload["email"]
        assert client.endereco.rua == payload["endereco"]["rua"]
        assert client.endereco.numero == payload["endereco"]["numero"]
        assert client.endereco.complemento == payload["endereco"]["complemento"]
        assert client.endereco.bairro == payload["endereco"]["bairro"]
        assert client.endereco.cidade == payload["endereco"]["cidade"]
        assert client.endereco.estado == payload["endereco"]["estado"]
        assert client.endereco.cep == payload["endereco"]["cep"]
        assert client.user.role == User.Role.CLIENTE

    def test_client_without_address_creation(self, api_client):
        payload = {
            "nome": "Cliente Sem Endereço",
            "email": "cliente.sem.endereco@teste.com",
            "password": "senha123",
        }

        response = api_client.post("/api/clientes/", payload, format="json")

        assert response.status_code == 201
        client = Cliente.objects.get(user__email=payload["email"])
        assert client.user.nome == payload["nome"]
        assert client.user.email == payload["email"]
        assert client.endereco is None
        assert client.user.role == User.Role.CLIENTE

    def test_client_retrieve(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)

        response = api_client.get("/api/clientes/me/")

        assert response.status_code == 200
        assert response.data["nome"] == client_user.nome
        assert response.data["email"] == client_user.email

    def test_client_partial_update(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)
        new_nome = "Cliente Teste Atualizado"
        new_email = "cliente.atualizado@teste.com"

        response = api_client.patch("/api/clientes/me/", {"nome": new_nome, "email": new_email}, format="json")

        assert response.status_code == 200
        client_user.refresh_from_db()
        assert client_user.nome == new_nome
        assert client_user.email == new_email

    def test_client_update_address(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)
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

        response = api_client.patch("/api/clientes/me/", payload, format="json")

        assert response.status_code == 200
        client_user.refresh_from_db()
        assert client_user.cliente.endereco.rua == payload["endereco"]["rua"]
        assert client_user.cliente.endereco.numero == payload["endereco"]["numero"]
        assert client_user.cliente.endereco.complemento == payload["endereco"]["complemento"]
        assert client_user.cliente.endereco.bairro == payload["endereco"]["bairro"]
        assert client_user.cliente.endereco.cidade == payload["endereco"]["cidade"]
        assert client_user.cliente.endereco.estado == payload["endereco"]["estado"]
        assert client_user.cliente.endereco.cep == payload["endereco"]["cep"]

    def test_client_update(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)
        endereco = baker.prepare("cliente.Endereco")
        payload = {
            "nome": "Cliente Teste Completo",
            "email": "cliente.completo@teste.com",
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

        response = api_client.put("/api/clientes/me/", payload, format="json")

        assert response.status_code == 200
        client_user.refresh_from_db()
        assert client_user.nome == payload["nome"]
        assert client_user.email == payload["email"]
        assert client_user.cliente.endereco.rua == payload["endereco"]["rua"]

    def test_client_destroy(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)
        nome = client_user.nome

        response = api_client.delete("/api/clientes/me/")

        assert response.status_code == 204
        assert not User.objects.filter(nome=nome).exists()
        assert not Cliente.objects.filter(user__nome=nome).exists()
