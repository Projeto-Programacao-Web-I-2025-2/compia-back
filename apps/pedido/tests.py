import pytest

from model_bakery import baker

from apps.cliente.models import Cliente
from apps.pedido.models import Pedido


@pytest.mark.django_db
class TestPedidoViewSet:
    def test_create_pedido(self, api_client, client_user):
        produto = baker.make("produto.Produto", preco=10.00)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "10.00",
            "itens": [
                {"produto": produto.id, "quantidade": 2},
            ],
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 201
        assert response.data["total"] == "30.00"

    def test_create_pedido_many_products(self, api_client, client_user):
        produto1 = baker.make("produto.Produto", preco=15.00)
        produto2 = baker.make("produto.Produto", preco=20.00)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "5.00",
            "itens": [
                {"produto": produto1.id, "quantidade": 1},
                {"produto": produto2.id, "quantidade": 3},
            ],
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 201
        assert response.data["total"] == "80.00"

    def test_list_pedidos_as_client(self, api_client, client_user):
        cliente = Cliente.objects.get(user=client_user)
        baker.make("pedido.Pedido", cliente=cliente)
        baker.make("pedido.Pedido", cliente=cliente)
        api_client.force_authenticate(user=client_user)

        response = api_client.get("/api/pedidos/")

        assert response.status_code == 200
        assert response.data["count"] == 2

    def test_patient_cannot_see_other_clients_pedidos(self, api_client, client_user):
        other_cliente = baker.make("cliente.Cliente")
        baker.make("pedido.Pedido", cliente=other_cliente)
        api_client.force_authenticate(user=client_user)

        response = api_client.get("/api/pedidos/")

        assert response.status_code == 200
        assert response.data["count"] == 0

    def test_cancelar_pedido(self, api_client, client_user):
        cliente = Cliente.objects.get(user=client_user)
        pedido = baker.make("pedido.Pedido", cliente=cliente, status=Pedido.StatusPedido.ABERTO)
        api_client.force_authenticate(user=client_user)

        response = api_client.post(f"/api/pedidos/{pedido.id}/cancelar/")

        assert response.status_code == 200
        assert response.data["detail"] == "Pedido cancelado com sucesso."
        pedido.refresh_from_db()
        assert pedido.status == Pedido.StatusPedido.CANCELADO

    def test_cancelar_pedido_invalid_status(self, api_client, client_user):
        cliente = Cliente.objects.get(user=client_user)
        pedido = baker.make("pedido.Pedido", cliente=cliente, status=Pedido.StatusPedido.ENVIADO)
        api_client.force_authenticate(user=client_user)

        response = api_client.post(f"/api/pedidos/{pedido.id}/cancelar/")

        assert response.status_code == 400
        assert response.data["detail"] == "Não é possível cancelar um pedido já enviado, entregue ou cancelado."
        pedido.refresh_from_db()
        assert pedido.status == Pedido.StatusPedido.ENVIADO

    def test_list_pedidos_with_cancelled_status(self, api_client, client_user):
        cliente = Cliente.objects.get(user=client_user)
        baker.make("pedido.Pedido", cliente=cliente, status=Pedido.StatusPedido.CANCELADO)
        baker.make("pedido.Pedido", cliente=cliente, status=Pedido.StatusPedido.ENTREGUE)
        api_client.force_authenticate(user=client_user)

        response = api_client.get("/api/pedidos/")

        assert response.status_code == 200
        assert response.data["count"] == 2
