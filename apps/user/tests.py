import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_djoser_user_creation_client(api_client):
    data = {
        "email": "apiuser@example.com",
        "password": "apipass123",
        "nome": "Usuário API",
        "role": User.Role.CLIENTE
    }
    response = api_client.post("/api/auth/users/", data)
    assert response.status_code == 201
    user = User.objects.get(email="apiuser@example.com")
    assert user.nome == "Usuário API"
    assert user.role == User.Role.CLIENTE
    assert user.is_active
    assert user.is_staff is False
    assert user.check_password("apipass123")


@pytest.mark.django_db
def test_djoser_user_creation_seller(api_client):
    data = {
        "email": "seller@example.com",
        "password": "sellerpass123",
        "nome": "Seller User",
        "role": User.Role.VENDEDOR
    }
    response = api_client.post("/api/auth/users/", data)
    assert response.status_code == 201
    user = User.objects.get(email="seller@example.com")
    assert user.nome == "Seller User"
    assert user.role == User.Role.VENDEDOR
    assert user.is_active is True
    assert user.is_staff is False
    assert user.check_password("sellerpass123")
    assert user.is_client is False
    assert user.is_seller is True
    assert user.is_backoffice is False


@pytest.mark.django_db
def test_djoser_user_edit_nome(api_client, client_user):
    api_client.force_authenticate(user=client_user)
    data = {
        "nome": "Nome Editado"
    }
    response = api_client.patch("/api/auth/users/me/", data)
    assert response.status_code in (200, 204)
    client_user.refresh_from_db()
    assert client_user.nome == "Nome Editado"


@pytest.mark.django_db
def test_djoser_user_edit_password_only(api_client, client_user):
    api_client.force_authenticate(user=client_user)
    data = {
        "current_password": "client123",
        "new_password": "newpass456"
    }
    response = api_client.post("/api/auth/users/set_password/", data)
    assert response.status_code in (200, 204, 204)
    client_user.refresh_from_db()
    assert client_user.check_password("newpass456")
