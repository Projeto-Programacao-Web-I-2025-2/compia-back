import pytest

from model_bakery import baker


@pytest.mark.django_db
class TestProdutoViewSet:
    def test_list_produtos_as_client(self, api_client, client_user, seller_user):
        baker.make("produto.Produto", _quantity=5, vendedor=seller_user)

        api_client.force_authenticate(user=client_user)
        response = api_client.get("/api/produtos/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 5

    def test_list_produtos_as_seller(self, api_client, seller_user):
        baker.make("produto.Produto", _quantity=3, vendedor=seller_user)

        api_client.force_authenticate(user=seller_user)
        response = api_client.get("/api/produtos/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 3

    def test_list_produtos_as_anonymous(self, api_client, seller_user):
        baker.make("produto.Produto", _quantity=4, vendedor=seller_user)

        response = api_client.get("/api/produtos/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 4

    def test_create_produto_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        payload = {
            "nome": "Produto Teste",
            "descricao": "Descrição do produto teste",
            "preco": 99.99,
            "autor": "Autor Teste",
            "ano_lancamento": 2024,
            "idioma": "PT",
            "tipo_produto": "LIVRO",
            "categorias": []
        }
        response = api_client.post("/api/produtos/", payload, format="json")

        assert response.status_code == 201
        assert response.data["nome"] == payload["nome"]

    def test_create_produto_as_client(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)
        payload = {
            "nome": "Produto Teste",
            "descricao": "Descrição do produto teste",
            "preco": 99.99,
            "autor": "Autor Teste",
            "ano_lancamento": 2024,
            "idioma": "PT",
            "tipo_produto": "LIVRO",
            "categorias": []
        }
        response = api_client.post("/api/produtos/", payload, format="json")

        assert response.status_code == 403

    def test_create_produto_with_categories(self, api_client, seller_user):
        categoria1 = baker.make("produto.Categoria")
        categoria2 = baker.make("produto.Categoria")

        api_client.force_authenticate(user=seller_user)
        payload = {
            "nome": "Produto Teste",
            "descricao": "Descrição do produto teste",
            "preco": 99.99,
            "autor": "Autor Teste",
            "ano_lancamento": 2024,
            "idioma": "PT",
            "tipo_produto": "LIVRO",
            "categorias": [categoria1.id, categoria2.id]
        }
        response = api_client.post("/api/produtos/", payload, format="json")

        assert response.status_code == 201
        assert len(response.data["categorias"]) == 2

    def test_update_produto(self, api_client, seller_user):
        produto = baker.make("produto.Produto", vendedor=seller_user)
        categoria = baker.make("produto.Categoria")

        api_client.force_authenticate(user=seller_user)
        payload = {
            "nome": "Produto Atualizado",
            "descricao": "Descrição atualizada",
            "preco": 149.99,
            "autor": "Autor Atualizado",
            "ano_lancamento": 2025,
            "idioma": "EN",
            "tipo_produto": "EBOOK",
            "categorias": [categoria.id]
        }
        response = api_client.put(f"/api/produtos/{produto.id}/", payload, format="json")

        assert response.status_code == 200
        assert response.data["nome"] == payload["nome"]
