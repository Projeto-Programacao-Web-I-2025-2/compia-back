import pytest

from model_bakery import baker


@pytest.mark.django_db
class TestPedidoViewSet:
    def test_list_pedidos_as_client(self, api_client, client_user):
        baker.make("pedido.Pedido", _quantity=5, cliente=client_user)

        api_client.force_authenticate(user=client_user)
        response = api_client.get("/api/pedidos/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 5
