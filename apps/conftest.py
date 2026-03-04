import pytest

from model_bakery import baker

from apps.user.models import User


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def client_user():
    client = baker.make("user.User", email="client@email.com", password="client123", role=User.Role.CLIENTE)
    return client


@pytest.fixture
def seller_user():
    seller = baker.make("user.User", email="seller@email.com", password="seller123", role=User.Role.VENDEDOR)
    return seller
