import os
import glob
import pytest

from django.conf import settings
from django.contrib.auth import get_user_model

from apps.cliente.models import Cliente
from apps.vendedor.models import Vendedor

User = get_user_model()


@pytest.fixture(autouse=True)
def cleanup_media_files():
    yield
    media_path = os.path.join(settings.MEDIA_ROOT, "ebooks")
    if os.path.exists(media_path):
        for file_path in glob.glob(os.path.join(media_path, "*.pdf")):
            try:
                os.remove(file_path)
            except Exception:
                pass


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def client_user(db):
    user = User.objects.create_user(
        email="client@email.com",
        password="client123",
        nome="Cliente Teste",
        role=User.Role.CLIENTE
    )
    Cliente.objects.create(user=user)
    return user


@pytest.fixture
def seller_user(db):
    user = User.objects.create_user(
        email="seller@email.com",
        password="seller123",
        nome="Vendedor Teste",
        role=User.Role.VENDEDOR
    )
    Vendedor.objects.create(user=user)
    return user
