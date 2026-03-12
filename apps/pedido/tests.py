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
        assert len(response.data) == 2

    def test_client_cannot_see_other_clients_orders(self, api_client, client_user):
        other_cliente = baker.make("cliente.Cliente")
        baker.make("pedido.Pedido", cliente=other_cliente)
        api_client.force_authenticate(user=client_user)

        response = api_client.get("/api/pedidos/")

        assert response.status_code == 200
        assert len(response.data) == 0

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
        assert len(response.data) == 2

    def test_create_pedido_and_decrement_stock(self, api_client, client_user):
        livro = baker.make("produto.Livro", estoque=5)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "0.00",
            "itens": [
                {"produto": livro.id, "quantidade": 3},
            ],
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 201
        livro.refresh_from_db()
        assert livro.estoque == 2

    def test_create_pedido_with_insufficient_stock(self, api_client, client_user):
        livro = baker.make("produto.Livro", estoque=2)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "0.00",
            "itens": [
                {"produto": livro.id, "quantidade": 3},
            ],
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 400
        assert "Estoque insuficiente" in str(response.data)
        livro.refresh_from_db()
        assert livro.estoque == 2

    def test_create_pedido_with_pacote_calculation(self, api_client, client_user):
        livro1 = baker.make("produto.Livro", estoque=5)
        livro2 = baker.make("produto.Livro", estoque=5)
        ebook = baker.make("produto.Ebook")
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "0.00",
            "itens": [
                {"produto": livro1.id, "quantidade": 2},
                {"produto": livro2.id, "quantidade": 3},
                {"produto": ebook.id, "quantidade": 1},
            ],
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 201
        assert response.data["pacote"]["height"] == 15
        assert response.data["pacote"]["width"] == 17
        assert response.data["pacote"]["length"] == 24
        assert response.data["pacote"]["weight"] == 2.6

    def test_create_pedido_with_pacote_calculation_no_books(self, api_client, client_user):
        ebook1 = baker.make("produto.Ebook")
        ebook2 = baker.make("produto.Ebook")
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "0.00",
            "itens": [
                {"produto": ebook1.id, "quantidade": 1},
                {"produto": ebook2.id, "quantidade": 1},
            ],
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 201
        assert response.data["pacote"] is None

    def test_update_pedido_with_frete_information(self, api_client, client_user):
        cliente = client_user.cliente
        pedido = baker.make("pedido.Pedido", cliente=cliente, frete=None, data_entrega=None, total=50.00)
        produto = baker.make("produto.Produto", preco=50.00)
        baker.make("pedido.ItemPedido", pedido=pedido, produto=produto, quantidade=1)
        api_client.force_authenticate(user=client_user)

        payload = {
            "frete": "15.00",
            "data_entrega": "2024-12-31",
        }

        response = api_client.patch(f"/api/pedidos/{pedido.id}/", payload, format="json")

        assert response.status_code == 200
        assert response.data["frete"] == "15.00"
        assert response.data["data_entrega"] == "2024-12-31"
        assert response.data["total"] == "65.00"

    def test_create_pedido_status_aberto(self, api_client, client_user):
        produto = baker.make("produto.Livro", preco=10.00)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "10.00",
            "itens": [
                {"produto": produto.id, "quantidade": 2},
            ],
            "status": "ABERTO"
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 201
        assert response.data["status"] == "ABERTO"

    def test_create_pedido_status_confirmado(self, api_client, client_user):
        produto = baker.make("produto.Livro", preco=10.00)
        api_client.force_authenticate(user=client_user)
        payload = {
            "frete": "10.00",
            "itens": [
                {"produto": produto.id, "quantidade": 2},
            ],
            "status": "CONFIRMADO"
        }

        response = api_client.post("/api/pedidos/", payload, format="json")

        assert response.status_code == 201
        assert response.data["status"] == "CONFIRMADO"

    def test_update_pedido_status_confirmado(self, api_client, client_user):
        cliente = client_user.cliente
        pedido = baker.make("pedido.Pedido", cliente=cliente, status=Pedido.StatusPedido.ABERTO)
        produto = baker.make("produto.Produto", preco=50.00)
        baker.make("pedido.ItemPedido", pedido=pedido, produto=produto, quantidade=1)
        api_client.force_authenticate(user=client_user)

        payload = {
            "status": "CONFIRMADO"
        }

        response = api_client.patch(f"/api/pedidos/{pedido.id}/", payload, format="json")

        assert response.status_code == 200
        assert response.data["status"] == "CONFIRMADO"

    def test_update_produto_status_frete_data_entrega(self, api_client, client_user):
        cliente = client_user.cliente
        pedido = baker.make("pedido.Pedido", cliente=cliente, status=Pedido.StatusPedido.ABERTO)
        produto = baker.make("produto.Produto", preco=50.00)
        baker.make("pedido.ItemPedido", pedido=pedido, produto=produto, quantidade=1)
        api_client.force_authenticate(user=client_user)

        payload = {
            "status": "CONFIRMADO",
            "frete": "20.00",
            "data_entrega": "2024-12-31"
        }

        response = api_client.patch(f"/api/pedidos/{pedido.id}/", payload, format="json")

        assert response.status_code == 200
        assert response.data["id"] == pedido.id
        assert response.data["status"] == "CONFIRMADO"
        assert response.data["frete"] == "20.00"
        assert response.data["data_entrega"] == "2024-12-31"
