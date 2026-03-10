from django.core.files.uploadedfile import SimpleUploadedFile

import pytest
from model_bakery import baker

from apps.produto.models import Ebook, Livro, Produto


@pytest.mark.django_db
class TestProdutoViewSet:
    def test_list_produtos(self, api_client):
        baker.make("produto.Ebook", _quantity=1, arquivo="ebooks/teste.pdf")
        baker.make("produto.Livro", _quantity=2, estoque=10)

        response = api_client.get("/api/produtos/")

        assert response.status_code == 200
        assert response.data["count"] == 3

    def test_list_produtos_livro(self, api_client):
        baker.make("produto.Livro", _quantity=1, estoque=10)

        response = api_client.get("/api/produtos/?tipo=livro")

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["tipo"] == "livro"
        assert response.data["results"][0]["estoque"] is not None
        assert response.data["results"][0]["arquivo"] is None

    def test_list_produtos_ebook(self, api_client):
        baker.make("produto.Ebook", _quantity=1, arquivo="ebooks/teste.pdf")

        response = api_client.get("/api/produtos/?tipo=ebook")

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["tipo"] == "ebook"
        assert response.data["results"][0]["estoque"] is None
        assert response.data["results"][0]["arquivo"] is not None

    def test_retrieve_livro(self, api_client):
        baker.make("produto.Ebook", _quantity=1, arquivo="ebooks/teste.pdf")
        produto = baker.make("produto.Livro", estoque=10)

        response = api_client.get(f"/api/produtos/{produto.id}/")

        assert response.status_code == 200
        assert response.data["id"] == produto.id
        assert response.data["nome"] == produto.nome
        assert response.data["descricao"] == produto.descricao
        assert response.data["preco"] == str(produto.preco)
        assert response.data["autor"] == produto.autor
        assert response.data["ano_lancamento"] == produto.ano_lancamento
        assert response.data["idioma"] == produto.idioma
        assert response.data["estoque"] == produto.estoque
        assert response.data["arquivo"] is None

    def test_retrieve_ebook(self, api_client):
        produto = baker.make("produto.Ebook", arquivo="ebooks/teste.pdf")

        response = api_client.get(f"/api/produtos/{produto.id}/")

        assert response.status_code == 200
        assert response.data["id"] == produto.id
        assert response.data["nome"] == produto.nome
        assert response.data["descricao"] == produto.descricao
        assert response.data["preco"] == str(produto.preco)
        assert response.data["autor"] == produto.autor
        assert response.data["ano_lancamento"] == produto.ano_lancamento
        assert response.data["idioma"] == produto.idioma
        assert response.data["estoque"] is None
        assert response.data["arquivo"] is not None

    def test_list_categorias(self, api_client):
        baker.make("produto.Categoria", _quantity=3)

        response = api_client.get("/api/produtos/categorias/")

        assert response.status_code == 200
        assert len(response.data) == 3

    def test_list_produtos_with_estoque_zero(self, api_client):
        baker.make("produto.Livro", estoque=0, _quantity=1)
        baker.make("produto.Ebook", arquivo="ebooks/teste.pdf", _quantity=1)

        response = api_client.get("/api/produtos/")

        assert response.status_code == 200
        assert response.data["count"] == 1
        assert response.data["results"][0]["tipo"] == "ebook"
        assert response.data["results"][0]["estoque"] is None
        assert response.data["results"][0]["arquivo"] is not None

    def test_list_produtos_filter_by_tipo(self, api_client):
        baker.make("produto.Livro", estoque=10, _quantity=2)
        baker.make("produto.Ebook", arquivo="ebooks/teste.pdf", _quantity=3)

        response = api_client.get("/api/produtos/?tipo=livro")

        assert response.status_code == 200
        assert response.data["count"] == 2
        for result in response.data["results"]:
            assert result["tipo"] == "livro"
            assert result["estoque"] is not None
            assert result["arquivo"] is None

    def test_list_produtos_filter_by_language(self, api_client):
        baker.make("produto.Livro", idioma="PT", estoque=10, _quantity=1)
        baker.make("produto.Livro", idioma="EN", estoque=10, _quantity=1)
        baker.make("produto.Ebook", idioma="PT", arquivo="ebooks/teste.pdf", _quantity=1)

        response = api_client.get("/api/produtos/?idioma=PT")

        assert response.status_code == 200
        assert response.data["count"] == 2
        for result in response.data["results"]:
            assert result["idioma"] == "PT"

    def test_list_produtos_filter_by_categoria(self, api_client):
        categoria1 = baker.make("produto.Categoria")
        categoria2 = baker.make("produto.Categoria")
        livro1 = baker.make("produto.Livro", estoque=10)
        livro2 = baker.make("produto.Livro", estoque=10)
        ebook1 = baker.make("produto.Ebook", arquivo="ebooks/teste.pdf")
        ebook2 = baker.make("produto.Ebook", arquivo="ebooks/teste.pdf")

        livro1.categorias.add(categoria1)
        livro2.categorias.add(categoria2)
        ebook1.categorias.add(categoria1)
        ebook2.categorias.add(categoria1)
        ebook2.categorias.add(categoria2)

        response = api_client.get(f"/api/produtos/?categorias={categoria1.id}")

        assert response.status_code == 200
        assert response.data["count"] == 3
        for result in response.data["results"]:
            assert categoria1.id in result["categorias"]

    def test_list_seller_products(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        products = baker.make("produto.Produto", vendedor=seller_user.vendedor, _quantity=3)
        baker.make("produto.Produto", _quantity=2)

        response = api_client.get("/api/produtos/meus-produtos/")

        assert response.status_code == 200
        assert len(response.data) == 3
        for i in range(3):
            assert response.data[i]["id"] == products[i].id
            assert response.data[i]["nome"] == products[i].nome

    def test_list_seller_products_as_non_seller(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)

        response = api_client.get("/api/produtos/meus-produtos/")

        assert response.status_code == 404

    def test_update_stock_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        livro = baker.make("produto.Livro", vendedor=seller_user.vendedor, estoque=10)

        payload = {
            "estoque": 5,
        }

        response = api_client.patch(f"/api/produtos/livros/{livro.id}/", payload)

        assert response.status_code == 200
        livro.refresh_from_db()
        assert livro.estoque == payload["estoque"]

    def test_update_stock_as_other_seller(self, api_client, seller_user):
        other_user = baker.make("user.User")
        other_seller = baker.make("vendedor.Vendedor", user=other_user)
        livro = baker.make("produto.Livro", estoque=1, vendedor=other_seller)
        api_client.force_authenticate(user=seller_user)
        payload = {
            "estoque": 5,
        }

        response = api_client.patch(f"/api/produtos/livros/{livro.id}/", payload)

        assert response.status_code == 404


@pytest.mark.django_db
class TestLivroViewSet:
    def test_create_livro_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)

        payload = {
            "nome": "Livro de Teste",
            "descricao": "Descrição do livro de teste",
            "preco": "29.90",
            "autor": "Autor de Teste",
            "ano_lancamento": 2020,
            "idioma": "PT",
            "estoque": 10,
        }

        response = api_client.post("/api/produtos/livros/", payload)

        assert response.status_code == 201
        livro = Livro.objects.get(id=response.data["id"])
        produto = Produto.objects.get(id=response.data["id"])
        assert livro.vendedor == seller_user.vendedor
        assert produto.vendedor == seller_user.vendedor

    def test_update_livro_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        livro = baker.make("produto.Livro", vendedor=seller_user.vendedor, estoque=10)

        payload = {
            "nome": "Livro de Teste Atualizado",
            "descricao": "Descrição do livro de teste atualizado",
            "preco": "39.90",
            "autor": "Autor de Teste Atualizado",
            "ano_lancamento": 2021,
            "idioma": "EN",
            "estoque": 5,
        }

        response = api_client.put(f"/api/produtos/livros/{livro.id}/", payload)

        assert response.status_code == 200
        livro.refresh_from_db()
        assert livro.nome == payload["nome"]
        assert livro.descricao == payload["descricao"]
        assert str(livro.preco) == payload["preco"]
        assert livro.autor == payload["autor"]
        assert livro.ano_lancamento == payload["ano_lancamento"]
        assert livro.idioma == payload["idioma"]
        assert livro.estoque == payload["estoque"]

    def test_partial_update_livro_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        livro = baker.make("produto.Livro", vendedor=seller_user.vendedor, estoque=10)

        payload = {
            "preco": "19.90",
            "estoque": 15,
        }

        response = api_client.patch(f"/api/produtos/livros/{livro.id}/", payload)

        assert response.status_code == 200
        livro.refresh_from_db()
        assert str(livro.preco) == payload["preco"]
        assert livro.estoque == payload["estoque"]

    def test_delete_livro_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        livro = baker.make("produto.Livro", vendedor=seller_user.vendedor, estoque=10)

        response = api_client.delete(f"/api/produtos/livros/{livro.id}/")

        assert response.status_code == 204
        assert not Livro.objects.filter(id=livro.id).exists()

    def test_create_livro_as_non_seller(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)

        payload = {
            "nome": "Livro de Teste",
            "descricao": "Descrição do livro de teste",
            "preco": "29.90",
            "autor": "Autor de Teste",
            "ano_lancamento": 2020,
            "idioma": "PT",
            "estoque": 10,
        }

        response = api_client.post("/api/produtos/livros/", payload)

        assert response.status_code == 403


@pytest.mark.django_db
class TestEbookViewSet:
    def test_create_ebook_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        file_data = SimpleUploadedFile("teste.pdf", b"conteudo do arquivo", content_type="application/pdf")

        payload = {
            "nome": "Ebook de Teste",
            "descricao": "Descrição do ebook de teste",
            "preco": "19.90",
            "autor": "Autor de Teste",
            "ano_lancamento": 2022,
            "idioma": "PT",
            "arquivo": file_data,
        }

        response = api_client.post("/api/produtos/ebooks/", payload)

        assert response.status_code == 201
        ebook = Ebook.objects.get(id=response.data["id"])
        produto = Produto.objects.get(id=response.data["id"])
        assert ebook.vendedor == seller_user.vendedor
        assert produto.vendedor == seller_user.vendedor
        assert ebook.arquivo.name == "ebooks/teste.pdf"

    def test_update_ebook_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        ebook = baker.make("produto.Ebook", vendedor=seller_user.vendedor, arquivo="ebooks/teste.pdf")
        new_file = SimpleUploadedFile("novo.pdf", b"conteudo do arquivo", content_type="application/pdf")

        payload = {
            "nome": "Ebook de Teste Atualizado",
            "descricao": "Descrição do ebook de teste atualizado",
            "preco": "29.90",
            "autor": "Autor de Teste Atualizado",
            "ano_lancamento": 2023,
            "idioma": "EN",
            "arquivo": new_file,
        }

        response = api_client.put(f"/api/produtos/ebooks/{ebook.id}/", payload)

        assert response.status_code == 200
        ebook.refresh_from_db()
        assert ebook.nome == payload["nome"]
        assert ebook.descricao == payload["descricao"]
        assert str(ebook.preco) == payload["preco"]
        assert ebook.autor == payload["autor"]
        assert ebook.ano_lancamento == payload["ano_lancamento"]
        assert ebook.idioma == payload["idioma"]
        assert ebook.arquivo.name == "ebooks/novo.pdf"

    def test_partial_update_ebook_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        ebook = baker.make("produto.Ebook", vendedor=seller_user.vendedor, arquivo="ebooks/teste.pdf")
        new_file = SimpleUploadedFile("novo.pdf", b"conteudo do arquivo", content_type="application/pdf")

        payload = {
            "preco": "9.90",
            "arquivo": new_file,
        }

        response = api_client.patch(f"/api/produtos/ebooks/{ebook.id}/", payload)

        assert response.status_code == 200
        ebook.refresh_from_db()
        assert str(ebook.preco) == payload["preco"]
        assert ebook.arquivo.name == "ebooks/novo.pdf"

    def test_delete_ebook_as_seller(self, api_client, seller_user):
        api_client.force_authenticate(user=seller_user)
        from apps.produto.models import Ebook
        ebook = baker.make("produto.Ebook", vendedor=seller_user.vendedor, arquivo="ebooks/teste.pdf")

        response = api_client.delete(f"/api/produtos/ebooks/{ebook.id}/")

        assert response.status_code == 204
        assert not Ebook.objects.filter(id=ebook.id).exists()

    def test_create_ebook_as_non_seller(self, api_client, client_user):
        api_client.force_authenticate(user=client_user)

        payload = {
            "nome": "Ebook de Teste",
            "descricao": "Descrição do ebook de teste",
            "preco": "19.90",
            "autor": "Autor de Teste",
            "ano_lancamento": 2022,
            "idioma": "PT",
            "arquivo": "ebooks/teste.pdf",
        }

        response = api_client.post("/api/produtos/ebooks/", payload)

        assert response.status_code == 403
