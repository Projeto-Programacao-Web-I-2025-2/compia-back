import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def client_user(db):
    return User.objects.create_user(
        email="client@email.com",
        password="client123",
        nome="Cliente Teste",
        role=User.Role.CLIENTE
    )


@pytest.fixture
def seller_user(db):
    return User.objects.create_user(
        email="seller@email.com",
        password="seller123",
        nome="Vendedor Teste",
        role=User.Role.VENDEDOR
    )
