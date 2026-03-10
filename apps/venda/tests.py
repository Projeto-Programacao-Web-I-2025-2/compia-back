import pytest

from model_bakery import baker


@pytest.mark.django_db
class TestVendaViewSet:
    def test_list_vendas_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        venda = baker.make("venda.Venda", vendedor=seller_user.vendedor)

        response = api_client.get("/api/vendas/", format="json")

        assert response.status_code == 200
        assert any(item["id"] == venda.id for item in response.json())

    def test_list_vendas_as_client(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)
        baker.make("venda.Venda", cliente=client_user.cliente)

        response = api_client.get("/api/vendas/", format="json")

        assert response.status_code == 403

    def test_seller_cannot_see_other_sellers_vendas(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        other_seller = baker.make("vendedor.Vendedor")
        venda = baker.make("venda.Venda", vendedor=other_seller)

        response = api_client.get("/api/vendas/", format="json")

        assert response.status_code == 200
        assert len(response.data) == 0
        assert all(item["id"] != venda.id for item in response.json())

    def test_list_venda_after_creating_pedido(self, api_client, client_user, seller_user):
        produto = baker.make("produto.Produto", preco=10.00, vendedor=seller_user.vendedor)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "10.00",
            "itens": [
                {"produto": produto.id, "quantidade": 2},
            ],
        }

        response_pedido = api_client.post("/api/pedidos/", payload, format="json")

        assert response_pedido.status_code == 201

        api_client.force_authenticate(user=seller_user)
        response_vendas = api_client.get("/api/vendas/", format="json")

        assert response_vendas.status_code == 200
        assert len(response_vendas.data) == 1
        assert response_vendas.data[0]["valor_total"] == "20.00"

    def test_list_venda_after_creating_multiple_produtos(self, api_client, client_user, seller_user):
        other_seller = baker.make("vendedor.Vendedor")
        produto_s = baker.make("produto.Produto", preco=15.00, vendedor=seller_user.vendedor)
        produto_os = baker.make("produto.Produto", preco=20.00, vendedor=other_seller)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "5.00",
            "itens": [
                {"produto": produto_s.id, "quantidade": 1},
                {"produto": produto_os.id, "quantidade": 2},
            ],
        }

        response_pedido = api_client.post("/api/pedidos/", payload, format="json")

        assert response_pedido.status_code == 201

        api_client.force_authenticate(user=seller_user)
        response_vendas = api_client.get("/api/vendas/", format="json")

        assert response_vendas.status_code == 200
        assert len(response_vendas.data) == 1
        assert response_vendas.data[0]["valor_total"] == "15.00"

    def test_list_venda_after_creating_multiple_pedidos(self, api_client, client_user, seller_user):
        other_seller = baker.make("vendedor.Vendedor")
        produto_s = baker.make("produto.Produto", preco=15.00, vendedor=seller_user.vendedor)
        produto_os = baker.make("produto.Produto", preco=20.00, vendedor=other_seller)
        api_client.force_authenticate(user=client_user)

        payload1 = {
            "frete": "5.00",
            "itens": [
                {"produto": produto_s.id, "quantidade": 2},
                {"produto": produto_os.id, "quantidade": 1},
            ],
        }
        payload2 = {
            "frete": "5.00",
            "itens": [
                {"produto": produto_s.id, "quantidade": 1},
            ],
        }

        response_pedido1 = api_client.post("/api/pedidos/", payload1, format="json")
        response_pedido2 = api_client.post("/api/pedidos/", payload2, format="json")

        assert response_pedido1.status_code == 201
        assert response_pedido2.status_code == 201

        api_client.force_authenticate(user=seller_user)
        response_vendas = api_client.get("/api/vendas/", format="json")

        assert response_vendas.status_code == 200
        assert len(response_vendas.data) == 2
        assert response_vendas.data[0]["valor_total"] == "30.00"
        assert response_vendas.data[1]["valor_total"] == "15.00"
